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
from kivy.clock import Clock

import test as testerino




#onfig.set('graphics', 'width', '412')
#Config.set('graphics', 'height', '732')

#.kv must be the same, but without App
# Loading Multiple .kv files  

#old screenmanager
class WindowManager(ScreenManager):
    pass

#popup window for deleting model
class Delete_popup(FloatLayout):
    sm = None    
    windw = None

class Main_Model_Page(Screen):
    img = 'default.jpg'
    #on screen enter, 
    #def on_enter(self):
        #after said screen is loaded
    #    Clock.schedule_once(self.Check_existing_model, 1)

    #checks for a saved model in the files
    def Check_existing_model(self):
        print("called")
        if os.path.exists("processed.png"):
            self.ids.model_image.source = "processed.png"

    #show the delete model popup
    def Show_delete_popup(self):    
        #if there is a model to delete         
        if os.path.exists("processed.png"):
            show = Delete_popup()
            show.sm = self.sm
            popupWindow = Popup(title="Delete Model?", content=show, size_hint=(0.7,0.7))
            show.windw = popupWindow
            #open windows     
            popupWindow.open()

    #delete the model
    def Delete_model(self):
        #check if a model exists
        if os.path.exists("processed.png"):
            os.remove("processed.png")
        #remove model from app image preview
        App.get_running_app().model = 'default.jpg'
        self.ids.model_image.source = 'default.jpg'
        
    #updates the preview(image), of the model
    def Update_model_image(self,url):
        App.get_running_app().model = url
        self.ids.model_image.source = url



class Filechooser_Page(Screen):    
    
    #on selecting a item
    def selected(self, filename):
        print(filename)
        try:
            self.ids.image_show.source = filename[0]
        except: 
            pass

    def open(self, path, filename):
       with open(os.path.join(path, filename[0])) as filee:
            print(filee.read())
    
    #submit choosen image
    def submit(self):
        
        #app = App.get_running_app()
    
        im_ = self.ids.image_show.source
        self.ids.image_show.source = 'default.jpg'
        self.sm.get_screen('Create_model_page').ids.create_image.source = im_       
    

class Create_model_page(Screen):
    #update the main model page/preview/image
    def create_model(self):     
        
        #app = App.get_running_app()
        self.sm.get_screen('Main_Model_Page').Update_model_image(self.ids.create_image.source)
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
   


