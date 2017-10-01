# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 16:33:37 2017

@author: guan
"""

import cv2
import os
import sys
import argparse

def blur(img, (minx, miny), (maxx, maxy), beta, flag):
    
    height = img.shape[0]
    width  = img.shape[1]
    if minx == -1 or miny ==-1 or maxx == -1 or maxy == -1:
        minx = 0
        miny = 0
        maxx = width
        maxy = height
    
    if maxy > height or maxx > width or \
            minx >= maxx or miny >= maxy: 
        print 'The region is unlegal！' 
        return 0
        
    kernel_size = (int(20*beta)*2+1, int(20*beta)*2+1)
    sigma = 10*beta
    
    if flag == 0:
        part_of_img = img[miny:maxy, minx:maxx] 
        #cv2.imwrite('part.jpg', part_of_img)    
        img_blur = cv2.GaussianBlur(part_of_img, kernel_size, sigma)
        for i in range(minx, maxx):
            for j in range(miny, maxy):
                img[j][i][0] = img_blur[j-miny][i-minx][0]
                img[j][i][1] = img_blur[j-miny][i-minx][1]
                img[j][i][2] = img_blur[j-miny][i-minx][2]        
        return img
    else:
        copy_im = img.copy()
        blur_copy_im = cv2.GaussianBlur(copy_im, kernel_size, sigma)
        for i in range(minx, maxx):
            for j in range(miny, maxy):
                blur_copy_im[j][i][0] = img[j-miny][i-minx][0]
                blur_copy_im[j][i][1] = img[j-miny][i-minx][1]
                blur_copy_im[j][i][2] = img[j-miny][i-minx][2]        
        return blur_copy_im

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

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Blur the image')
    
    parser.add_argument('--b', dest='beta',
                        help='blur degree',
                        default=0.5, type=float)
    parser.add_argument('--out', dest='outdir',
                        help='output dir',
                        default='output/', type=str)
    parser.add_argument('--imagePath', dest='image_path',
                        help='The path of image',
                        default=None, type=str)
    parser.add_argument('--Xpoint1', dest='minx',
                        help='The X of point1, (if equal -1 then blur the entire image!)',
                        default=None, type=int)
    parser.add_argument('--Ypoint1', dest='miny',
                        help='The Y of point1, (if equal -1 then blur the entire image!)',
                        default=None, type=int)
    parser.add_argument('--Xpoint2', dest='maxx',
                        help='The X of point2, (if equal -1 then blur the entire image!)',
                        default=None, type=int)
    parser.add_argument('--Ypoint2', dest='maxy',
                        help='The Y of point2, (if equal -1 then blur the entire image!)',
                        default=None, type=int)
    parser.add_argument('--isturn', dest='flag',
                        help='If isturn equal 1, the image is blured except the designated areas',
                        default=0, type=int)
                    
    if len(sys.argv) < 5:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
        
    args = parse_args()
    print args
       
    mkdir(args.outdir) 
    
    
    leftup_point = (args.minx, args.miny)
    rightdown_point = (args.maxx, args.maxy)
      
    im = cv2.imread(args.image_path)
    im = blur(im, leftup_point,  rightdown_point, args.beta, args.flag)
    name = os.path.splitext(os.path.split(args.image_path)[1])[0]        
    cv2.imwrite(args.outdir + name + '_blur.jpg', im)
    print 'blur the image: '+ name +'.jpg successfully!'