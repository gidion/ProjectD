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
from kivymd.uix.imagelist import SmartTileWithLabel
import numpy as np
import cv2 
import os
Builder.load_file('Assortment.kv')

class Product_item():
    id = -1
    product_name = ''
    img_url =  ''
    link = 'www.google.com'
    text = ''
    def __init__(self, id, product_name,img_url,link,text):
        self.id = id
        self.product_name = product_name
        self.img_url = img_url
        self.link = link
        self.text = text

class MySmartTileWithLabel(SmartTileWithLabel):
    pass
#temp products list, to be replaced with a list made from the database
temp_list = [Product_item('0','dress1','dress1.jpg',"http://google.com/",'Image 1'),Product_item('1','dress2','dress2.jpg',"http://google.com/",'Image 2'),Product_item('2','dress3','dress3.jpg','www.google.com','Image 3'),Product_item('3','dress4','dress4.jpg','www.google.com','Image 4')]

class Assortment_page(Screen):
    sm: None
    def on_enter(self):
        for item in temp_list:
            #combine the products text into the widgets text
            main_text =  '[size=20][color=#ffffff]' + str(item.product_name) + '[/color][/size]\n[size=10]2020_09_07_1842.jpg[/size]'
            #create widget MySmartTileWithLabel
            temp = MySmartTileWithLabel(id = item.id, text = main_text)
            #assign screen manager to MySmartTileWithLabel widget, without using the init
            temp.sm = self.sm
            #assign the product info to the MySmartTileWithLabel
            temp.product = item
            #add the widget to the gridlayout
            self.ids.Items_Grid.add_widget(temp)
            #crop the image for the gallery
            App.get_running_app().crop_image_for_tile(temp, temp.size, \
            item.img_url)
    pass