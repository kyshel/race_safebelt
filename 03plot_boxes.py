# plot boxes to images, save to disk
# todo: add seePLOT, see PIL
from  _lib1 import *

import json
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt


# settings
map={0:'ground',1:'guard',2:'belt',3:'sky'}

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)



def see(fp,resize=(960, 540)):
    # see image by filepath, use opencv (stupid but simple)
    img = cv2.imread(fp)
    if resize:
        # img = cv2.resize(img, resize)
        img = ResizeWithAspectRatio(img,resize[0],resize[1])
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_im(dst,im):
    # save image by dst path, use opencv
    if os.path.exists(dst):
        cv2.imwrite(dst, im)
        return True
    else:
        raise Exception('dst not exist!', dst)



def main():
    # read single picture
    test_src = '3_test_imagesa/'
    test_dst = 'test_dst/'

    fn = 'ffe7193f_50d5_4edd_8bd8_2f9766dc171c.JPG'
    fp_src = test_src + fn
    fp_dst = test_dst + fn

    # see(fp_src)
    im = cv2.imread(fp_src)
    save_im(fp_dst, im)


    # add label

    # save it to dir

    # read pics
    # add labels
    # save them to dst

    # auto_increment

    pass





















# with open('best_predictions_for02.json') as f:
#     submit_list = json.load(f)
#
#
#
#
# test_src = '3_test_imagesa/'
# test_dst = 'test_imgs_dst/'
#
#
#
#
# test_paths_list = []
# for subdir, dirs, files in os.walk(test_ds_dir):
#     for file in files:
#
#         image_path = os.path.join(subdir, file)
#         test_paths_list += image_path
#
#
# for path in test_paths_list:






if __name__ == '__main__':
    main()