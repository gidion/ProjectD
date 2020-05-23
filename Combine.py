import os
import time

import kivy.properties as props
from PIL import Image as ImagePIL, ImageDraw, ImageFilter
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.utils.cropimage import crop_image

from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup

import webbrowser
import numpy as np
import cv2 
import os

class Combine_page(Screen):

    def To_store(self,url):
        webbrowser.open(url)

    def Update_Page(self,product,sm):
        self.sm = sm
        self.ids.image_product.source = product.img_url
        self.ids.image_product.reload()
        self.ids.Product_name.text = product.product_name
        self.product = product

        #update model  
        #check if a model exists
        if os.path.exists("Model.png"):
            #remove model image
            self.ids.model.source = "Model.png"
        #self.image_product = url 
        #lines that change detail properties
        pass 

    def Temp_Combine(self):
        #reloads/refreshes the image 
        #opencv reads image from preview, by reading the image url, from the preview image
        img_product = cv2.imread(self.ids.image_product.source)
        img_person = cv2.imread(self.ids.model.source)
        #new img url
        img_combined = "temp_combination.png"
        #Image Processing steps, placeholder
        hsv_product = cv2.cvtColor(img_product, cv2.COLOR_BGR2HSV)
        #rgb colors
        l_b = np.array([0, 32, 0])
        #hue
        u_b = np.array([255, 255, 255])
        mask = cv2.inRange(hsv_product, l_b, u_b)
 
        #create image from processed image
        img_product = cv2.bitwise_and(img_product, img_product, mask=mask)

        #cropt images
        img_product = cv2.resize(img_product, (512,512) )
        img_person = cv2.resize(img_person,(512,512))

        #calculates the per element sum of 2 arrays or an array and a scalar
        #dst_image = cv2.add(img,img2)

        #add with weighted          img alpha  img2 alpha  gamma
        result_img = cv2.addWeighted(img_product, 1, img_person, 1, 0)
        #save new processed image copy
        cv2.imwrite(img_combined, result_img )
        #show processed image
        self.ids.combined.source = img_combined
        #reloads/refreshes the image
        self.ids.combined.reload()
        pass
    pass