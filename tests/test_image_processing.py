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
from image_processing_project import main, image_analysis, parse_cmdline, get_file_names, names_dict, pvalue_analysis2
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


class TestParser(unittest.TestCase):
    def test_SampleData(self):
        test_input = SAMPLE_DATA_FILE_LOC
        try:
            if logger.isEnabledFor(logging.DEBUG):
                parse_cmdline(test_input)
            with capture_stdout(main, test_input) as output:
                self.assertTrue(os.path.isfile('C:/Users/Agnes Resto Irizarry/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/aresto/image_processing_project/image_processing_project/data/foxa2-localized'))

            self.assertTrue(os.path.isdir('C:/Users/Agnes Resto Irizarry/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/aresto/image_processing_project/data/foxa2-localized'))
        finally:
            silent_remove(DEF_CVS_OUT, disable=DISABLE_REMOVE)


class TestDataAnalysis(unittest.TestCase):
    def test__Normalization(self):
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


if __name__ == '__main__':
    unittest.main()