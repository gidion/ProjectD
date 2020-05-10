from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import cv2 
import os
from kivy.uix.boxlayout import BoxLayout
import numpy as np


class Special_specific_screen(Screen):
    #update the main model page/preview/image
    def create_model(self):      
        app = App.get_running_app()
        app.root.get_screen('Main_Model_Page').Update_model_image(self.ids.create_image.source)
    def process(self):
        img = cv2.imread(self.ids.create_image.source)
        self.ids.create_image.source = 'default.jpg'
        #new img url
        #img_pros_url = old_url[:-4] + 'processed' + '.png'
        img_pros_url = 'processed.png'

        #Processing
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #rgb colors
        l_b = np.array([0, 32, 0])
        #hue
        u_b = np.array([255, 255, 255])
        mask = cv2.inRange(hsv, l_b, u_b)
        res = cv2.bitwise_and(img, img, mask=mask)



        #save new processed image copy
        cv2.imwrite(img_pros_url, res )
        #show processed image
        self.ids.create_image.source = img_pros_url
   
