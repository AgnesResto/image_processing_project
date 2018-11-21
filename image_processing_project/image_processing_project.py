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
from argparse import ArgumentParser
import cv2
import numpy as np
import pandas as pd
from scipy import stats
import errno
import csv


SUCCESS = 0
INVALID_DATA = 1
IO_ERROR = 2
ENNOENT = 3
DEFAULT_PATH_NAME = 'C:/Users/Agnes Resto Irizarry/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/aresto/image_processing_project/image_processing_project/data/foxa2-localized/'
#DEFAULT_PATH_NAME = 'C:/Users/Agnes Resto Irizarry/Desktop/DataSci/foxa2-localized/'


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def image_analysis(folder_path):
    """
    Finds the average intensity in grayscale images
    
    Parameters
    -------
    folder_path : directory path of images of interest

    Returns
    -------
    fluorescent_intensity : numpy array

    """
    file_names = get_file_names(folder_path)
    print(file_names)
    grouped_images = names_dict(file_names)

    # specify the number of channels
    num_channels = 4

    f1_intensity = []
    f2_intensity = []
    f1_normalized_intensity = []
    f2_normalized_intensity = []
    for k, v in grouped_images.items():
        names = pd.Series(v)
        # process images only if you have the images from all of the channels
        if len(names) == num_channels:
            # read each channel of interest as a grayscale image
            dapi = cv2.imread(folder_path + names[1], 0)
            nkx2 = cv2.imread(folder_path + names[2], 0)
            foxa3 = cv2.imread(folder_path + names[3], 0)
            # normalize the fluorescent channels using dapi
            normalized_nkx2 = cv2.divide(nkx2, dapi)
            normalized_foxa3 = cv2.divide(foxa3, dapi)
            # analyze fluorescent intensity of each channel of interest
            # nkx2_hist = cv2.calcHist([normalized_nkx2], [0], None, [256], [0, 256])
            # foxa3_hist = cv2.calcHist([normalized_foxa3], [0], None, [256], [0, 256])
            # plt.plot(nkx2_hist)
            # plt.plot(foxa3_hist)
            # plt.show()
            f1_intensity.append(np.mean(nkx2))
            f2_intensity.append(np.mean(foxa3))
            f1_normalized_intensity.append(np.mean(normalized_nkx2))
            f2_normalized_intensity.append(np.mean(normalized_foxa3))

    return f1_intensity, f2_intensity, f1_normalized_intensity, f2_normalized_intensity



def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = ArgumentParser(description='Reads images with fluorescent staining and analyzes fluorescent intensity of '
                                        'each channel and morphology of each cell cluster. Additionally, it computes '
                                        'the p-value of the fluorescent intensity of each channel.')
    parser.add_argument("-p", "--path_data_file", help="The location (directory path) of the csv file with the images"
                                                       "data to analyze",
                        default=DEFAULT_PATH_NAME)
    args = None
    try:
        args = parser.parse_args(argv)
        a = os.path.exists(args.path_data_file)
        if a != 1:
            print("path does not exist")
    except errno.ENOENT as e:
        print("No such directory:", e)
        parser.print_help()
        return args, ENNOENT
    return args.path_data_file, SUCCESS


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


def pvalue_analysis2(intensity_data1, intensity_data2):
    # analyze differences in fluorescent intensity between different conditions by getting the pvalue
    t, p = stats.ttest_ind(intensity_data1, intensity_data2)
    return t, p


def main(argv=None):
    path1, ret = parse_cmdline(argv)
    print("This is the path: ", path1)
    if ret != 0:
        return ret
    nkx2, foxa3, normalized_nkx2, normalized_foxa3 = image_analysis(path1)
    print(normalized_nkx2, normalized_foxa3)
    base_out_fname = path1 + '_averages2'
    out_fname = base_out_fname + '.csv'
    np.savetxt(out_fname, normalized_nkx2, delimiter=',')
    np.savetxt(out_fname, np.row_stack((normalized_nkx2, normalized_foxa3)), delimiter=',')
    print("Wrote file: {}".format(out_fname))

    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)

