"""
Unit and regression test for image_processing_project.py
"""
import errno
import os
import sys
import unittest
from contextlib import contextmanager
from io import StringIO
import numpy as np
import logging
from image_processing_project import main, image_analysis, parse_cmdline
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)

CURRENT_DIR = os.path.dirname(__file__)
MAIN_DIR = os.path.join(CURRENT_DIR, '..')
TEST_DATA_DIR = os.path.join(CURRENT_DIR, 'image_processing_project')
PROJ_DIR = os.path.join(MAIN_DIR, 'image_processing_project')
DATA_DIR = os.path.join(PROJ_DIR, 'data')
SAMPLE_DATA_FILE_LOC = os.path.join(DATA_DIR, 'foxa2-localized/')
print('This is your sample data path: ', SAMPLE_DATA_FILE_LOC)
DEF_CVS_OUT = os.path.join(MAIN_DIR, 'sample_data_stats.csv')


DEF_CSV_OUT = os.path.join(MAIN_DIR, '_averages3.csv')


def silent_remove(filename, disable=False):
    """
    Removes the target file name, catching and ignoring errors that indicate that the
    file does not exist.
    @param filename: The file to remove.
    @param disable: boolean to flag if want to disable removal
    """
    if not disable:
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise


class TestMain(unittest.TestCase):
    # These tests make sure that the program can run properly from main
    def testSampleDataOutput(self):
        test_input = ["-p", SAMPLE_DATA_FILE_LOC]
        # Checks that runs with defaults and that files are created
        try:
            if logger.isEnabledFor(logging.DEBUG):
                main(test_input)
            # checks that the expected message is sent to standard out
            with capture_stdout(main, test_input) as output:
                self.assertTrue("averages3.csv" in output)

            print("output path: ", SAMPLE_DATA_FILE_LOC + "_averages3.csv")
            self.assertTrue(os.path.isfile(SAMPLE_DATA_FILE_LOC + "/_averages3.csv"))
        finally:
            silent_remove(DEF_CSV_OUT, disable=DISABLE_REMOVE)


class TestMainFailWell(unittest.TestCase):
    def test_wrongpath(self):
        # test if the folder path does not exist
        test_input2 = ["-p", 'example.csv']
        if logger.isEnabledFor(logging.DEBUG):
            main(test_input2)
        with capture_stderr(main, test_input2) as output:
            self.assertTrue("No such directory" in output)


class TestDataAnalysis(unittest.TestCase):
    def test__Normalization(self):
        # test if the images are being properly normalized by comparing the intensity of a
        # normalized image with the original intensity
        nkx2, foxa3, normalized_nkx2, normalized_foxa3 = image_analysis(SAMPLE_DATA_FILE_LOC)
        print(nkx2, normalized_nkx2)
        self.assertGreater(nkx2, normalized_nkx2)
        self.assertGreater(foxa3, normalized_foxa3)


@contextmanager
def capture_stdout(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out

@contextmanager
def capture_stderr(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    err, sys.stderr = sys.stderr, StringIO()
    command(*args, **kwargs)
    sys.stderr.seek(0)
    yield sys.stderr.read()
    sys.stderr = err

if __name__ == '__main__':
    unittest.main()