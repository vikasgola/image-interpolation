#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================== Vikas Gola 2016UCS0023 =============================
#                       Add input images to 'input' named folder in the same directory
#                 You will get output images in output folder

import numpy as np
import math,cv2,glob

def improveImage(fileName):
    ori512 = cv2.cvtColor(cv2.imread(fileName),cv2.COLOR_BGR2GRAY) 

    print(ori512.shape)

    if ori512.max() > 1:
        ori512 = ori512/255

    (ow,oh) = ori512.shape
    (w_s,h_s) = ori512.shape/4


    # keepsafe the original 512 size image
    pred = ori512.copy()
    # remove pixels
    pred[1::2] = 0
    pred[::2,1::2] = 0


    # created 256*256 image
    ori256 = pred[::2,::2].copy()
    (iw,ih) = ori256.shape

    nrow = ih//h_s
    ncol = iw//w_s
    for i in range(nrow):
        for j in range(ncol):
            l = (w_s)*(h_s)

            X = np.zeros( (l,5))
            X[:,:] = 0.5
            X[:,0] = 1
            Y = np.zeros( (l,1))
            X1 = np.zeros( (l,5))
            X1[:,:] = 0.5
            X1[:,0] = 1

            for a in range(h_s):
                for b in range(w_s):
                    if j*w_s + b - 1 > -1 and i*h_s + a - 1 > -1:
                        X[a*w_s + b,1] = ori256[j*w_s + b - 1 , i*h_s + a - 1  ]
                    if j*w_s + b - 1 > -1 and i*h_s + a + 1 < ih:
                        X[a*w_s + b,2] = ori256[j*w_s + b - 1 , i*h_s + a + 1 ]
                    if j*w_s + b + 1 < iw and i*h_s + a + 1 < ih:
                        X[a*w_s + b,3] = ori256[j*w_s + b + 1 , i*h_s + a + 1 ]
                    if j*w_s + b + 1 < iw and i*h_s + a - 1 > -1:
                        X[a*w_s + b,4] = ori256[j*w_s + b + 1 , i*h_s + a - 1 ]
                    
                    Y[a*w_s + b,0] = ori256[j*w_s + b , i*h_s + a ]


                    X1[a*w_s + b,1] = ori256[j*w_s + b , i*h_s + a ]
                    if i*h_s + a + 1 < ih:
                        X1[a*w_s + b,2] = ori256[j*w_s + b , i*h_s + a + 1 ]
                    if j*w_s + b + 1 < iw:
                        X1[a*w_s + b,3] = ori256[j*w_s + b + 1 , i*h_s + a ]
                    if j*w_s + b + 1 < iw and i*h_s + a + 1 < ih:
                        X1[a*w_s + b,4] = ori256[j*w_s + b + 1 , i*h_s + a + 1 ]


            B = np.linalg.inv(X.T @ X) @ X.T @ Y
            Y1 = X1 @ B

            pred[j*w_s*2+1:(j+1)*w_s*2+1:2, i*h_s*2+1:(i+1)*h_s*2+1:2] = Y1.reshape((w_s,h_s)).T


    for i in range(oh):
        for j in range(ow):
            if (i%2 == 0 and j%2 == 0) or (i%2 == 1 and j%2 == 1):
                continue
            neighbours = 0
            a = 0
            if i-1 > -1:
                neighbours += 1
                a  += pred[i-1 , j ]
            if j+1 < ow:
                neighbours += 1
                a  += pred[i , j+1 ]
            if i+1 < oh:
                neighbours += 1
                a  += pred[i+1 , j ]
            if j-1 > -1:
                neighbours += 1
                a  += pred[i , j-1 ]
            pred[i,j] = a/neighbours

    pred[ow-1] = pred[ow-2]  
    pred[:,oh-1] = pred[:,oh-2] 

    pred = np.clip(pred,0,1)
    E = pred - ori512
    E = E*255

    MSE = np.square(E).sum()/(oh*ow)

    PSNR = 10*math.log10(255*255/MSE)
    
    
    print("================ "+fileName+" =================")
    fileName = "../output/" + fileName[6:]
    cv2.imwrite(fileName,pred*255)
    print("Mean Squared Error:" ,MSE)
    print("PSNR:",PSNR)
    print()

    return PSNR


if __name__=="__main__":
    averagePSNR = 0
    n = 0
    for img in glob.glob("../input/*.tif"):
        averagePSNR += improveImage(img)
        n += 1

    print("AVERAGE PSNR =====>",averagePSNR/n)
