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

SUCCESS = 0
INVALID_DATA = 1
IO_ERROR = 2
ENNOENT = 3
DEFAULT_PATH_NAME = 'C:/Users/Agnes Resto Irizarry/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_' \
                    '79rhkp1fndgsc/LocalState/rootfs/home/aresto/datasci_project_/data/external/foxa2-localized/'
#DEFAULT_PATH_NAME = 'C:/Users/Agnes Resto Irizarry/Desktop/DataSci/foxa2-localized/'


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
    except IOError as e:
        print("Invalid path name:", e)
        parser.print_help()
        return args, IO_ERROR

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


def enhance_contrast(image):
    # enhance the contrast of an image
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    # cdf_normalized = cdf * hist.max()/ cdf.max()
    # plt.plot(cdf_normalized, color = 'b')
    # plt.hist(image.flatten(), 256, [0, 256], color = 'r')
    # plt.xlim([0, 256])
    # plt.show()
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    enhanced_image = cdf[image]
    return enhanced_image


def make_mask(im):
    # make a binary mask of an image
    (thresh, im_bw) = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = np.ones((6, 6), np.uint8)
    img_erosion = cv2.erode(im_bw, kernel, iterations=2)
    dilated_img = cv2.dilate(img_erosion, kernel, iterations=2)
    img_erosion2 = cv2.erode(dilated_img, kernel, iterations=3)
    binary_img = cv2.dilate(img_erosion2, kernel, iterations=3)
    return binary_img


def pvalue_analysis2(intensity_data1, intensity_data2):
    # analyze differences in fluorescent intensity between different conditions by getting the pvalue
    t, p = stats.ttest_ind(intensity_data1, intensity_data2)
    return t, p


def main(argv=None):
    path1, ret = parse_cmdline(argv)
    print("This is the path: ", path1)
    if ret != 0:
        return ret
    file_names = get_file_names(path1)
    print(file_names)
    grouped_images = names_dict(file_names)

    # specify the number of channels
    num_channels = 4

    nkx2_intensity = []
    foxa3_intensity = []
    for k, v in grouped_images.items():
        names = pd.Series(v)
        # process images only if you have the images from all of the channels
        if len(names) == num_channels:
            # read each channel of interest as a grayscale image
            dapi = cv2.imread(path1 + names[1], 0)
            nkx2 = cv2.imread(path1 + names[2], 0)
            foxa3 = cv2.imread(path1 + names[3], 0)
            # normalize the fluorescent channels using dapi
            normalized_nkx2 = cv2.divide(nkx2, dapi)
            normalized_foxa3 = cv2.divide(foxa3, dapi)
            # analyze fluorescent intensity of each channel of interest
            # nkx2_hist = cv2.calcHist([normalized_nkx2], [0], None, [256], [0, 256])
            # foxa3_hist = cv2.calcHist([normalized_foxa3], [0], None, [256], [0, 256])
            # plt.plot(nkx2_hist)
            # plt.plot(foxa3_hist)
            # plt.show()
            nkx2_intensity.append(np.mean(normalized_nkx2))
            foxa3_intensity.append(np.mean(normalized_foxa3))
            # analyze cyst properties
            enhanced_dapi = enhance_contrast(dapi)
            cyst_binary = make_mask(enhanced_dapi)


        else:
            print('You do not have all the channels')

    print('nkx2_intensity', nkx2_intensity)

    # print(canvas(args.no_attribution))
    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)

