"""
Unit and regression test for data_proc.py
"""
import errno
import os
import sys
import unittest
from contextlib import contextmanager
from io import StringIO
import numpy as np
import logging
from image_processing_project import main

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)

CURRENT_DIR = os.path.dirname(__file__)
MAIN_DIR = os.path.join(CURRENT_DIR, '..')
TEST_DATA_DIR = os.path.join(CURRENT_DIR, 'image_processing_project')
PROJ_DIR = os.path.join(MAIN_DIR, 'image_processing_project')
DATA_DIR = os.path.join(PROJ_DIR, 'data')
SAMPLE_DATA_FOLDER = os.path.join(DATA_DIR, 'sample_data')
SAMPLE_DATA_FILE_LOC = os.path.join(DATA_DIR, 'sample_data')

