# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 20:33:28 2017

@author: guan mingyang
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from math import *
from PIL import Image,ImageFont,ImageDraw 
import random 


# create black background
def createBlackBG(bg):
   
    blackBG = np.zeros((bg.shape[0], bg.shape[1], bg.shape[2]),dtype=bg.dtype )
    
    return blackBG
    
# create the label
def createLable(img, line_width):
    
    # height width passway
    height = img.shape[0]
    width = img.shape[1]
    passway = img.shape[2]
    label_img = np.zeros((img.shape[0], img.shape[1], img.shape[2]),dtype=img.dtype )  
        
    for i in range(width):
        for j in range(line_width):
            label_img[j,i,0] = 255
            label_img[j,i,1] = 255
            label_img[j,i,2] = 255
    
    for i in range(width):
        for j in range(height-line_width,height):
            label_img[j,i,0] = 255
            label_img[j,i,1] = 255
            label_img[j,i,2] = 255
    
    for i in range(line_width):
        for j in range(height):
            label_img[j,i,0] = 255
            label_img[j,i,1] = 255
            label_img[j,i,2] = 255
    
    for i in range(width-line_width,width):
        for j in range(height):
            label_img[j,i,0] = 255
            label_img[j,i,1] = 255
            label_img[j,i,2] = 255
    
    return label_img
# rotate the img (antialockwise) 
def rotate(img, degree):
    
    height,width=img.shape[:2]

    #旋转后的尺寸
    heightNew=int(width*fabs(sin(radians(degree)))+height*fabs(cos(radians(degree))))
    widthNew=int(height*fabs(sin(radians(degree)))+width*fabs(cos(radians(degree))))
    
    matRotation=cv2.getRotationMatrix2D((width/2,height/2),degree,1)
    
    matRotation[0,2] +=(widthNew-width)/2  
    matRotation[1,2] +=(heightNew-height)/2  
    
    imgRotation = cv2.warpAffine(img, matRotation, (widthNew,heightNew), borderValue=(0,0,0))
    #print imgRotation.shape 
    #np.savetxt("rotate.txt", imgRotation)
    '''
    cv2.imshow("img",img)
    cv2.imshow("imgRotation",imgRotation)
    cv2.waitKey(0)
    '''
    return imgRotation

# affine the img
def Affine(img, point1, point2, point3):
  
    height = img.shape[0] 
    width  = img.shape[1]
    
    SrcPointsA = np.float32([[0,0], [0,height], [width,0]])
    CanvasPointsA = np.float32([point1, point2, point3])
    
    AffineMatrix = cv2.getAffineTransform(SrcPointsA, CanvasPointsA)
    AffineImg = cv2.warpAffine(img, AffineMatrix, (int(7*width/6), int(7*height/6)), borderValue=(0,0,0))
         
    return AffineImg

# resize the image
def resize(image, new_width=None, new_height=None, inter=cv2.INTER_AREA):
    
    dim = None
    (h, w) = image.shape[:2]

    if new_width is None and new_height is None:
        return image

    if new_width is None:
        # 则根据高度计算缩放比例
        r = new_height / float(h)
        dim = (int(w * r), new_height)

    else:
        # 根据宽度计算缩放比例
        r = new_width / float(w)
        dim = (new_width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized

# paste image on the background
def paste(background, upimg, black_bg, label):
    
    copy_background = background.copy()
    copy_black_bg = black_bg.copy()    
    
    bg_height, bg_width = background.shape[:2]
    upimg_height, upimg_width = upimg.shape[:2]
    
    
    alpa = 0.95
    temp = 1
    while temp*upimg_height > 0.8*bg_height or temp*upimg_width > 0.8*bg_width:
        temp = temp*alpa
        
    upimg = resize(upimg, new_width=int(upimg_width*temp))
    label = resize(label, new_width=int(upimg_width*temp))
    upimg_height, upimg_width = upimg.shape[:2]
      
    #cv2.imwrite("la_.png", label)
    
    m = random.randint(1, bg_width-upimg_width)    
    n = random.randint(1, bg_height-upimg_height)
    
    upimg = rmblack(upimg)    
    
    for i in range(upimg_width):
        for j in range(upimg_height):
            if upimg[j, i, 0] == 0 and upimg[j, i, 1] == 0 and upimg[j, i, 2] == 0:
                continue
            else:
                copy_background[j+n, i+m, 0] = upimg[j, i, 0] 
                copy_background[j+n, i+m, 1] = upimg[j, i, 1] 
                copy_background[j+n, i+m, 2] = upimg[j, i, 2]

    for i in range(upimg_width):
        for j in range(upimg_height):                
                copy_black_bg[j+n, i+m, 0] = label[j, i, 0] 
                copy_black_bg[j+n, i+m, 1] = label[j, i, 1] 
                copy_black_bg[j+n, i+m, 2] = label[j, i, 2] 
    
    return (copy_background, copy_black_bg)

def GetFileNameAndExt(filename):
 
     (filepath,tempfilename) = os.path.split(filename)
     (shotname,extension) = os.path.splitext(tempfilename)
     return (shotname,extension)    

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("//")
 
    isExists = os.path.exists(path)
 
    if not isExists:
        os.makedirs(path)
        print path+' 创建成功'
        return True
    else:
        print path+' 目录已存在'
        return False       

# create square black background
def createSquareBG(background):
    
    height, width = background.shape[:2]
    if height > width :
        return background[0:width-1, 0:width-1]
    else: 
        return background[0:height-1, 0:height-1]

# do not rotate, affine and perspective the image        
def pasteNormal(background, upimg, black_bg, label):
    
    copy_background = background.copy()
    copy_black_bg = black_bg.copy()    
    
    bg_height, bg_width = background.shape[:2]
    upimg_height, upimg_width = upimg.shape[:2]
    
    while bg_height*0.7 < upimg_height or bg_width*0.7 < upimg_width :
        upimg = resize(upimg, new_width=int(upimg_width*0.95))
        label = resize(label, new_width=int(upimg_width*0.95))
        upimg_height, upimg_width = upimg.shape[:2]
    
    m = random.randint(1, bg_width-upimg_width)    
    n = random.randint(1, bg_height-upimg_height)
        
    for i in range(upimg_width):
        for j in range(upimg_height):
                copy_background[j+n, i+m, 0] = upimg[j, i, 0] 
                copy_background[j+n, i+m, 1] = upimg[j, i, 1] 
                copy_background[j+n, i+m, 2] = upimg[j, i, 2]
                
                copy_black_bg[j+n, i+m, 0] = label[j, i, 0] 
                copy_black_bg[j+n, i+m, 1] = label[j, i, 1] 
                copy_black_bg[j+n, i+m, 2] = label[j, i, 2] 
    
    return (copy_background, copy_black_bg)

#smooth the image
def smooth(img):
    
    img1 = np.float32(img) 
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img1,-1,kernel)
    
    return dst

# perspective the image    
def perspective(img):
    
    height = img.shape[0]
    width = img.shape[1]
    pts1 = np.float32([[0, 0],[width, 0],[0, height],[width, height]])
    pts2 = np.float32([[0, 0],[random.randint(5*width/6, width), random.randint(0, height/6)], \
                       [random.randint(0, width/6), random.randint(5*height/6, height)], \
                        [random.randint(5*width/6, width), random.randint(5*height/6, height)]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(img.shape[1], img.shape[0]))
    
    return dst

# remove the black border
def rmblack(im):
    
    height, width = im.shape[:2]
    
    num = 7
    for j in range(0, height):
        for i in range(width-1, -1, -1):
            if im[j][i][0] == 0 and im[j][i][1] == 0 and im[j][i][2] == 0:
                continue
            else:
                for num in range(0, 4):
                    im[j][i][0] = 0
                    im[j][i][1] = 0
                    im[j][i][2] = 0
                    i = i -1
                break;
        for i in range(0, width):
            if im[j][i][0] == 0 and im[j][i][1] == 0 and im[j][i][2] == 0:
                continue
            else:
                for num in range(0, 4):
                    im[j][i][0] = 0
                    im[j][i][1] = 0
                    im[j][i][2] = 0
                    i = i + 1
                break;   
    #print 'remove black border!'
    return im            

if __name__ == "__main__":
         
    image = []
    background = []  
    
    image_path = 'image'
    bg_path = 'background'
    
    Loutdir = './/merge//label//'
    Ioutdir = './/merge//image//'
    
    mkdir(Loutdir)
    mkdir(Ioutdir)    
    
    for root, sub_dirs, files in os.walk(image_path):
        for afile in files:
                image.append(os.path.join(root,afile))    
    
    for root, sub_dirs, files in os.walk(bg_path):
        for afile in files:
                background.append(os.path.join(root,afile))
     
    i = 0     
     
    for forward in image:
        for back in background:
                   
            
            (shotname_f,extension) = GetFileNameAndExt(forward)
            (shotname_b,extension) = GetFileNameAndExt(back)
            
            
            im = cv2.imread(forward)
            bg = cv2.imread(back)

            bg = createSquareBG(bg)            
            
            if bg.shape[1] > 1000 :
                bg = resize(bg, new_width= 1000)
            
            
            blackBG = createBlackBG(bg)
            label = createLable(im, 5)
                
            (height, width) = im.shape[:2]
        
            
            (normal_img, normal_label) = pasteNormal(bg, im, blackBG, label)
            cv2.imwrite(Ioutdir+str(i)+".jpg" , normal_img)
            cv2.imwrite(Loutdir+str(i)+".png", normal_label)            
            print "generate new image and label:\n" + Ioutdir+str(i)+".jpg\n" \
            + Loutdir+str(i)+".png"
            
            # affine
            #point1 = [random.randint(0, int(width/6)), random.randint(0, int(width/6))]
            point1 = [0, 0]
            point2 = [random.randint(0, int(width/6)), random.randint(int(5*height/6), height)]
            point3 = [random.randint(int(5*width/6), width),random.randint(0, int(height/6))]    
                
            af_img = Affine(im, point1, point2, point3)
            af_lable = Affine(label, point1, point2, point3)
           
            (paste_img, paste_label) = paste(bg, af_img, blackBG, af_lable)
            
            paste_img = resize(paste_img, new_width = 800)  
            paste_label = resize(paste_label, new_width = 800)   
            
            cv2.imwrite(Ioutdir+"affine_"+str(i)+".jpg" , paste_img)
            cv2.imwrite(Loutdir+"affine_"+str(i)+".png", paste_label)            
            print "generate affine image and label:\n" + Ioutdir+"affine_"+str(i)+".jpg\n" \
            + Loutdir+"affine_"+str(i)+".png"
           
            
            # rotate
            degree = random.randint(0,360)    
            Rimg = rotate(im, degree) 
            Rlable = rotate(label, degree)
            
            (final_img, final_label) = paste(bg, Rimg, blackBG, Rlable)
            
            final_img = resize(final_img, new_width= 800)
            final_label = resize(final_label, new_width= 800)            
            
            cv2.imwrite(Ioutdir+"rotate_"+str(i)+".jpg", final_img)
            cv2.imwrite(Loutdir+"rotate_"+str(i)+".png", final_label)
            print "generate rotate image and label:\n" + Ioutdir+"rotate_"+str(i)+".jpg\n" \
            + Loutdir+"rotate_"+str(i)+".png"
            
            #makeB = cv2.copyMakeBorder(final_img,10, 10, 10, 10, borderType=1)
            #cv2.imwrite(Ioutdir+"makeB_"+str(i)+".jpg", makeB)
            
            #perspective
            per_im = perspective(im)
            per_lable = perspective(label)
            
            (per_final_img, per_final_label) = paste(bg, per_im, blackBG, per_lable) 
            cv2.imwrite(Loutdir+"per_"+str(i)+".png", per_final_label)
            cv2.imwrite(Ioutdir+"per_"+str(i)+".jpg", per_final_img)
            print "generate perspective image and label:\n" + Ioutdir+"per_"+str(i)+".jpg\n" \
            + Loutdir+"per_"+str(i)+".png"
            
            i = i + 1
    
    
    
    
    
    
