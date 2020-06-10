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
import json

class Combination_item():
    id = -1
    product_name = ''
    #file path to image
    img_url =  ''
    #web link to product on webshop
    link = 'https://www.tashira.nl/'
    def __init__(self, id, product_name,img_url,link):
        self.id = id
        self.product_name = product_name
        self.img_url = img_url
        self.link = link


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
            self.ids.model.reload()
        else:
            self.ids.model.source = "default.jpg"
            self.ids.model.reload()
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
        #add with weighted          img alpha  img2 alpha  gamma
        result_img = cv2.addWeighted(img_product, 1, img_person, 1, 0)
        #save new processed image copy
        cv2.imwrite(img_combined, result_img )
        #show processed image
        self.ids.combined.source = img_combined
        #reloads/refreshes the image
        self.ids.combined.reload()
        pass
    #save and add a new combination to the user combinations, by loading the current combinations, add the new combination to the list, and then save the updated combinations 
    def Save_Combination(self,product,combined_url):
        if combined_url != 'default.jpg':
            combinations = []
            #try to load 
            combinations = self.Load_combinations(True)
            
            #assign id value
            new_id = 0
            #if previous combinations exist
            if len(combinations) >= 1:
                #get new id from previous combination id + 1
                new_id = combinations[len(combinations) -1]["id"] + 1

            #save combined image to file, as a separate file
            img_product = cv2.imread(combined_url)
            #get time 
            timestr = time.strftime("%Y%m%d_%H%M%S")
            #set file name for combination file
            img_name = ("Combination_{}.png".format(timestr))
            #create image file
            cv2.imwrite(img_name, img_product )

            #create dict
            combinations_dict = {
                "id" : new_id,
                "product_name" : product.product_name,
                "img_url" : img_name,
                "link" : product.link
                }
            #add new combination to existing combination list
            combinations.append(combinations_dict)    
            #call save function
            self.Save_Combinations(combinations)
            #change product img to combination img 
            product.img_url = combinations_dict["img_url"]
            #go to new combination page
            self.sm.get_screen("Combination_page").Update_Page(product,self.sm,combinations_dict["id"])
            self.sm.current = 'Combination_page'



    def Save_Combinations(self,combinations_app):
        #save all combinations
        with open('Combinations.json', 'w') as file_combinations:
            json.dump(combinations_app, file_combinations)
        file_combinations.close()

    def Load_combinations(self,in_json):
        #combinations dict
        loaded_combinations = {}
        #list combinations
        Combinations = []
        #try to open combinations file
        try:
            with open('Combinations.json', 'r') as file_combinations:  
                loaded_combinations = json.load(file_combinations)
            file_combinations.close()
        #if there is no file
        except:
            loaded_combinations = []
        #return class list of combinations
        if in_json:
            return loaded_combinations
        #return json dict of combinations
        for combination in loaded_combinations:
            new_combination = Combination_item(
                combination['id'],
                combination['product_name'],
                combination['img_url'],
                combination['link'])
            Combinations.append(new_combination)       
        return Combinations
