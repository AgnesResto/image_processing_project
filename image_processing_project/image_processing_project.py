#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
image_processing_project.py
processing of immunofluorescent staining

Handles the primary functions
"""
import os
import glob
import sys
import argparse
#import cv2
#import numpy as np
#import pandas as pd
#from scipy import stats


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def canvas(with_attribution=True):
    """
    Placeholder function to show example docstring (NumPy format)



    Returns
    -------
    quote : str
        Compiled string including quote and optional attribution
    """

    quote = "The code is but a canvas to our imagination."
    if with_attribution:
        quote += "\n\t- Adapted from Henry David Thoreau"
    return quote


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--input_rates", help="The location of the input rates file",
    #                     default=DEF_IRATE_FILE, type=read_input_rates)
    parser.add_argument("-n", "--no_attribution", help="Whether to include attribution",
                        action='store_false')
    args = None
    try:
        args = parser.parse_args(argv)
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, 2

    return args, 0


def get_file_names(path):
    # obtain all of the image names from a folder and create paths to get each of them
    names_images = []
    os.chdir(path)
    for file in glob.glob("*.TIF"):
        names_images.append(file)
    return names_images


def names_dict(files_in_folder):
    # group channels of each image in a dictionary
    dictionary = {}
    for x in files_in_folder:
        group = dictionary.get(x[:11], [])
        group.append(x)
        dictionary[x[:11]] = group
    return dictionary


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret
    print(canvas(args.no_attribution))
    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
