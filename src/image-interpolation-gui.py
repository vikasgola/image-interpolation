#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================== Vikas Gola 2016UCS0023 =============================
#                       Add input images to 'input' named folder in the same directory
#                 You will get output images in output folder that has been predicted by code

import numpy as np
import math,cv2,glob
import tkinter
import os
from os.path import expanduser
from tkinter.filedialog import askopenfilename

inputFile = None
var = None


def improveImage():
    var.set("Creating Image")
    # input = inputFile
    ori256 = cv2.cvtColor(cv2.imread(inputFile),cv2.COLOR_BGR2GRAY) 

    if ori256.max() > 1:
        ori256 = ori256/255

    (ow,oh) = ori256.shape
    ow = ow*2
    oh = oh*2
    (iw,ih) = ori256.shape
    (w_s,h_s) = (ori256.shape[0],ori256.shape[1])


    pred = np.zeros((ow,oh))

    for i in range(ih):
        for j in range(iw):
            pred[i*2,j*2] = ori256[i,j]

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
    fileName, file_extension = os.path.split(inputFile)

    if not os.path.exists(expanduser("~") + "/output_images/"):
        os.makedirs(expanduser("~") + "/output_images/")

    if cv2.imwrite( expanduser("~") + "/output_images/"+file_extension,pred*255):
        var.set("Successfully created image \n" + "~/output_images/"+ file_extension)
    else:
        var.set("Failed to save image \n" + "~/output_images/"+ file_extension)

    makeBigger.pack_forget()


def getFile():
    global inputFile
    var.set("adding an image...!")
    inputFile = askopenfilename()
    if inputFile:
        var.set("added an image :-)")
        makeBigger.pack()
    else:
        var.set("Image has not been added. \n Please add an image.")


if __name__=="__main__":
    window = tkinter.Tk()
    window.title("Make Your Image Bigger and Better")
    window.geometry("600x400")

    var = tkinter.StringVar(window)
    label = tkinter.Label( window, textvariable=var,height="7")
    var.set("output image will be stored \n at /home/your_username/output_images/image_name")
    label.pack()

    addImage = tkinter.Button(window,text='Add Image',width="25",height="5",command=getFile)
    addImage.pack()

    makeBigger = tkinter.Button(window,text='Start Image Interpolation\n Click Me!',width="25",height="5",command=improveImage)
    # makeBigger.pack()


    window.mainloop()
