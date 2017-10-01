# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 17:31:16 2017

@author: guan
"""

from skimage import data, exposure, img_as_float, io
#from skimage import io
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import argparse
import sys

# change the lightness of the image
# alpa = [0:1] -> 变亮
# alpa = [1:~] -> 变暗
def changeLight(imageName, outdir, alpa):
    
    mkdir(outdir)   
    (name, extension) = parseName(imageName)
    image = img_as_float(io.imread(imageName))    
    change_img= exposure.adjust_gamma(image, alpa)
    outPatn = os.path.join(outdir, 'L_'+name+extension)
    plt.imsave(outPatn, change_img)

# move the pixel 
def movePixel(img, dist):
    mv_img = np.copy(img)
    #print mv_img
    for j in range(img.shape[0]-dist):
        for i in range(img.shape[1]-dist):
            mv_img[j+dist, i+dist, 0] = img[j, i, 0]
            mv_img[j+dist, i+dist, 1] = img[j, i, 1]
            mv_img[j+dist, i+dist, 2] = img[j, i, 2]
    #cv2.imwrite('g_test.jpg', mv_img)
    return mv_img
            
# generate the ghost image
def ghost(img):
    
    mv_img = movePixel(img, 8)
    #print type(mv_img), type(img)
    #dest = img
    dest = cv2.addWeighted(img, 0.7, mv_img, 0.3, 0)
    return dest

def addWater(img):
    
    water = cv2.imread('resource//water.jpg')
    #im = cv2.imread('test2.jpeg')
    height,width = img.shape[:2]
    water_re = cv2.resize(water, ( width, height), interpolation=cv2.INTER_AREA)
    #print water_re.shape
    dest = cv2.addWeighted(img, 0.6, water_re, 0.4, 0)
    return dest
    
    
# 创建目录
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部符号
    path = path.rstrip("//")
 
    isExists = os.path.exists(path)
 
    if not isExists:
        os.makedirs(path)
        print path+' 创建成功'
        return True
    else:
        print path+' 目录已存在'
        return False  

def parseName(path):
    
    (dirpath, file_name) = os.path.split(path)
    (name, extension) = os.path.splitext(file_name)
    return (name, extension)

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Blur the image')
    
    parser.add_argument('--a', dest='alpa',
                        help='light degree: alpa = 1 not change || alpa->0 lighter || alpa -> ∞ darker ',
                        default=1, type=float)
    parser.add_argument('--out', dest='outdir',
                        help='output dir (default ''output/'' )',
                        default='output/', type=str)
    parser.add_argument('--imagePath', dest='image_path',
                        help='The path of image',
                        default=None, type=str)
                    
    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    
    
    args = parse_args()

    (name, extension) = parseName(args.image_path)    
    
    changeLight(args.image_path, args.outdir, args.alpa)
    im = cv2.imread(args.image_path)

    ghost_im = ghost(im)
    outpath = os.path.join(args.outdir,'G_'+name+extension)
    cv2.imwrite(outpath, ghost_im)
    
    addW_im = addWater(im)
    outpath = os.path.join(args.outdir,'W_'+name+extension)
    cv2.imwrite(outpath, addW_im)    
    
    
    