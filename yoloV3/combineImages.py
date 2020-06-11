"""Yolo v3 detection script.

Saves the detections in the `detection` folder.

Usage:
    python detect.py <images/video> <iou threshold> <confidence threshold> <filenames>

Example:
    python detect.py images 0.5 0.5 data/images/dog.jpg data/images/office.jpg
    python detect.py video 0.5 0.5 data/video/shinjuku.mp4

Note that only one video can be processed at one run.
"""
## TODO:
    # add dress path in the input
    # add in the application
            # detect if img or video
            # set dress path
            # call main(images/video, personPath)


## billboard TODO:
    # try with video input
    # cut video in pictures


import tensorflow as tf
import sys
import cv2

# from yoloV3.yolo_v3 import Yolo_v3
# from yoloV3.utils import load_images, load_class_names, draw_boxes, draw_frame

from yoloV3.yolo_v3 import Yolo_v3
from yoloV3.utils import load_images, load_class_names, draw_boxes, draw_frame

sys.version

import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image,ImageOps

import itertools


tf.compat.v1.disable_eager_execution()

_MODEL_SIZE = (416, 416)
_CLASS_NAMES_FILE = './yoloV3/data/labels/obj.names'
_MAX_OUTPUT_SIZE = 20

class videoConverter:
    inPath = ''
    outPath = ''
    picAmt = 0

    def countFrames():
        FPS = 25
        cap = cv2.VideoCapture(videoConverter.inPath)
        cap.set(cv2.CAP_PROP_FPS, FPS)

        currentFrame = 0
        while (True):
            ret, frame = cap.read()
            if (not ret): 
                break
            else:
                currentFrame += 1
        cap.release()
        cv2.destroyAllWindows()
        return currentFrame


    def splitVid():
        framesN = videoConverter.countFrames() // videoConverter.picAmt
        framesAdd = 0
        ImgName = 1
        currentFrame = 0

        FPS = 25
        cap = cv2.VideoCapture(videoConverter.inPath)
        cap.set(cv2.CAP_PROP_FPS, FPS)

        while (True):
            ret, frame = cap.read()
            if (not ret): 
                break
            else:
                if(currentFrame == framesAdd):
                    name = videoConverter.outPath + str(ImgName) + '.png'
                    cv2.imwrite(name, frame)
                    framesAdd += framesN
                    ImgName += 1  
                    currentFrame += 1 
        cap.release()
        cv2.destroyAllWindows()


    def videoList():
        videoConverter.splitVid()
        imageList = []
        for picture in range(videoConverter.picAmt):
            imageList.append(videoConverter.outPath + str(picture + 1) + '.png')
        return imageList



    def preparelists(picAmt, cInput, cOutput, pInput, pOutput):
        videoConverter.picAmt = picAmt

        print('converting clothing video into images...')

        videoConverter.inPath = cInput
        videoConverter.outPath = cOutput
        clothList = videoConverter.videoList()

        print('converting your video into images...')

        videoConverter.inPath = pInput
        videoConverter.outPath = pOutput
        personList = videoConverter.videoList()

        return clothList, personList


class combineImages:
    clothingImg  = ''
    imagePath = ''
    err_mar = 0

    def makeBlack(clothingImg, row, p):
        clothingImg[row][p][0] = 0.
        clothingImg[row][p][1] = 0.
        clothingImg[row][p][2] = 0.
        clothingImg[row][p][3] = 1.
        return clothingImg


    def colorCheck(rgb, clothingImgp):
        for x in range(4):
            if clothingImgp[x] >= rgb[x] - 1*combineImages.err_mar and  clothingImgp[x] <= rgb[x] + 1*combineImages.err_mar:
                return True
            else:
                return False


    def blackPixelCheck(row, p):
        if combineImages.clothingImg[row][p][0] == 0. and combineImages.clothingImg[row][p][1] == 0. and combineImages.clothingImg[row][p][2] == 0. and combineImages.clothingImg[row][p][3] == 1.:
            return True
        else:
            return False


    def prepClothingImg(clothingImg):

        plt.imshow(clothingImg)

        r = clothingImg[0][0][0]
        g = clothingImg[0][0][1]
        b = clothingImg[0][0][2]
        a = clothingImg[0][0][3]

        rgb = [r, g, b, a]

        clothingImg[0][0][0] = 0.
        clothingImg[0][0][1] = 0.
        clothingImg[0][0][2] = 0.
        clothingImg[0][0][3] = 0.

        rown = -1
        ppcounter = -1

        top = 1000000000
        right = 0
        left = 1000000000
        bottom = 0
        topCon = True

        for row in range(len(clothingImg)):
            for p in range(len(clothingImg[row])):
                if p != 0:
                    if combineImages.blackPixelCheck(row - 1, p) or combineImages.blackPixelCheck(row, p - 1):
                        if combineImages.colorCheck(rgb, clothingImg[row][p]):
                            clothingImg = combineImages.makeBlack(clothingImg, row, p)
                else:
                    if row != 0:
                        if combineImages.blackPixelCheck(row - 1, p):
                            if combineImages.colorCheck(rgb, clothingImg[row][p]):
                                clothingImg = combineImages.makeBlack(clothingImg, row, p)

            for p in range(len(clothingImg[row])):
                if combineImages.colorCheck(rgb, clothingImg[row][p]):
                    if not(combineImages.blackPixelCheck(row, p) and combineImages.blackPixelCheck(row, p + 1)):
                        clothingImg = combineImages.makeBlack(clothingImg, row, p)
                        for pn in range(p, 0, -1):
                            if not(combineImages.blackPixelCheck(row, p)) and combineImages.blackPixelCheck(row, p + 1):
                                clothingImg = combineImages.makeBlack(clothingImg, row, p)

        for row in range(len(clothingImg)):
            for p in range(len(clothingImg[row])):
                try:
                    if row != 0:
                        if not(combineImages.blackPixelCheck(row, p)) and combineImages.blackPixelCheck(row - 1, p):
                            if row < top:
                                top = row
                    if row != 0:
                        if not(combineImages.blackPixelCheck(row, p)) and combineImages.blackPixelCheck(row, p - 1):
                            if p < left:
                                left = p
                    if not(combineImages.blackPixelCheck(row, p)) and combineImages.blackPixelCheck(row, p + 1):
                        if p > right:
                            right = p
                    if not(combineImages.blackPixelCheck(row, p)) and combineImages.blackPixelCheck(row + 1, p):
                        if row > bottom:
                            bottom = row
                except:
                    pass
                
        croppedclothingImg = clothingImg[top:bottom, left:right, :] 

        fig = plt.imshow(croppedclothingImg)
        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.savefig(combineImages.imagePath + 'steps/dressTest.png', bbox_inches='tight', pad_inches = 0)


    def combineImg(input_names, clothList):
        print('detecting body...')
        iou_threshold = 0.5
        confidence_threshold = 0.1
        class_names = load_class_names(_CLASS_NAMES_FILE)
        n_classes = len(class_names)

        model = Yolo_v3(n_classes=n_classes, model_size=_MODEL_SIZE,
                        max_output_size=_MAX_OUTPUT_SIZE,
                        iou_threshold=iou_threshold,
                        confidence_threshold=confidence_threshold)

        batch_size = len(input_names)
        batch = load_images(input_names, model_size=_MODEL_SIZE)
        inputs = tf.compat.v1.placeholder(tf.float32, [batch_size, *_MODEL_SIZE, 3])
        detections = model(inputs, training=False)
        saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables(scope='yolo_v3_model'))

        with tf.compat.v1.Session() as sess:
            saver.restore(sess, './yoloV3/weights/model.ckpt')

            detection_result = sess.run(detections, feed_dict={inputs: batch})
        draw_boxes(input_names, detection_result, class_names, _MODEL_SIZE)
        personArr = draw_boxes(input_names, detection_result, class_names, _MODEL_SIZE)


        nameCounter = 1
        imgResultList = []
        print('combining images...')
        for x in range(len(personArr)):

            combineImages.clothingImg = plt.imread(clothList[x])
            combineImages.prepClothingImg(combineImages.clothingImg)

            personImg = Image.open(input_names[x])
            preppedClothingImg = Image.open(combineImages.imagePath + 'steps/dressTest.png')

            preppedClothingImg = preppedClothingImg.convert("RGBA")
            datas = preppedClothingImg.getdata()

            newData = []
            for item in datas:
                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    newData.append((1, 1, 1, 0))
                else:
                    newData.append(item)

            preppedClothingImg.putdata(newData)


            try:
                # person=0 body=1 legs=2 head=3
                bodyLeft = (personArr[x][1][0] - personArr[x][0][0]) // 3
                bodyRight = (personArr[x][0][2] - personArr[x][1][2]) // 3

                height = (personArr[x][1][3] - personArr[x][1][1]) * 2
                width = (personArr[x][1][2] - personArr[x][1][0])

                PreppedClothingImg = preppedClothingImg.resize((int(width), int(height)))

                left = personArr[x][1][0]

                try:
                    top = personArr[x][1][1] - ((personArr[x][1][1] - personArr[x][3][3]))
                except:
                    top = personArr[x][1][1] - ((personArr[x][1][3] - personArr[x][1][1]) // 20)

                backimg = personImg.copy()
                backimg.paste(PreppedClothingImg, (int(left), int(top)), mask=PreppedClothingImg)
                returnPath = combineImages.imagePath + 'result/combinedImg' + str(nameCounter) + '.png'
                backimg.save(returnPath)
                nameCounter += 1
                return returnPath
            except:
                print('could not locate body')
        print('saved')
        


    def getCombination(pInp, cInp):
        q, ext = pInp.split('.')
        if ext == 'mp4':
            # inputs = amt of wanted pictures out of vid/ video paths for clothing(c) and person(p)/ output path for images
            picAmt = 10
            cInpath = cInp
            cOutPath = combineImages.imagePath + 'dress/'
            pInPath = pInp
            pOutPath = combineImages.imagePath + 'person/'

            cList, pList = videoConverter.preparelists(picAmt, cInpath, cOutPath, pInPath, pOutPath)
            # outputs = output of all clothing images (cList)/ output for all person images (pList)
        else:
            im_rgb = Image.open(cInp)
            im_rgba = im_rgb.copy()
            im_rgba.putalpha(255)
            im_rgba.save('./images/steps/transformed.png')

            pList = [pInp]
            cList = ['./images/steps/transformed.png']

        combineImages.imagePath = './images/'
        combineImages.err_mar = 0.055
        return combineImages.combineImg(pList, cList)




























#white
