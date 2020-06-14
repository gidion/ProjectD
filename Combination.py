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
    link = 'www.google.com'
    def __init__(self, id, product_name,img_url,link):
        self.id = id
        self.product_name = product_name
        self.img_url = img_url
        self.link = link

#popup window for deleting combination
class Delete_popup_combination(FloatLayout):
    #screen manager reference
    sm = None    
    windw = None

class Combination_page(Screen):

    def To_store(self,url):
        webbrowser.open(url)

    def Update_Page(self,product,sm,comb_id):
        self.sm = sm
        self.id
        self.ids.image_product.source = product.img_url
        self.ids.image_product.reload()
        self.ids.Product_name.text = product.product_name
        self.product = product
        self.comb_id = comb_id
        #self.image_product = url 
        #lines that change detail properties


    #shows delete popu[]
    def Show_delete_popup_combination(self):    
        #if there is a model to delete         
        
        #create popup
        show = Delete_popup_combination()
        #add screen manager reference, to popup
        show.sm = self.sm
        #create popup window
        popupWindow = Popup(title="Delete combination: ", content=show, size_hint=(0.7,0.7))
        #assign popupWindow as reference, in order to close it via the button
        show.windw = popupWindow
        #open window    
        popupWindow.open()

    def Delete_Combination(self,product,combined_url,combination_id):
        #combinations list
        combinations = []
        #load combinations from file
        combinations = self.Load_combinations(True)
        #for each combination in combinations
        for comb in combinations:
            #if combinaiton id == id of current combination page id
            if comb["id"] == combination_id:
                #delete image, if it exists
                try:
                    if(comb["img_url"] != "default.jpg"):
                        os.remove(comb["img_url"]) 
                #image isn't found
                except:
                    pass
                #delete combination
                combinations.remove(comb)
                
        #call save function
        self.Save_Combinations(combinations)
        #go back to gallery
        self.sm.current = 'Gallery'

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