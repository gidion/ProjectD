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
from kivy.uix.button import ButtonBehavior

#.kv must be the same, but without App

#default model name/string
default_model = 'default.jpg'  
#model png name/string
model_png = "Model.png"
#processed png name/string
processed_png = "processed.png"


class ImageButton(ButtonBehavior, Image):
    def on_press(self):  
        print ('pressed')


#old screenmanager
class WindowManager(ScreenManager):
    pass

#popup window for deleting model
class Delete_popup(FloatLayout):
    #screen manager reference
    sm = None    
    windw = None

class Main_Model_Page(Screen):

    #show the image preview model popup
    def Show_image_popup(self,sourcee):    
        #if there is a model to delete         
        show = Image_popup()
        #add screen manager reference, to popup
        show.sm = self.sm
        #assign preview image to popup image
        show.ids.model_image.source = sourcee
        #create popup window
        popupWindow = Popup(title="Model Preview?", content=show, size_hint=(0.2,0.2))
        #assign popupWindow as reference, in order to close it via the button
        show.windw = popupWindow
        #open window     
        popupWindow.open()


    #checks for a saved model in the files
    def Check_existing_model(self):
        #check if a model is already created
        if os.path.exists("Model.png"):
            #show model image in preview
            self.ids.model_image.source = "Model.png"
        else:
            #show default image
            self.ids.model_image.source = "default.jpg"

    #show the delete model popup
    def Show_delete_popup(self):    
        #if there is a model to delete         
        if os.path.exists("Model.png"):
            #create popup
            show = Delete_popup()
            #add screen manager reference, to popup
            show.sm = self.sm
            #create popup window
            popupWindow = Popup(title="Preview Model: ", content=show, size_hint=(0.7,0.7))
            #assign popupWindow as reference, in order to close it via the button
            show.windw = popupWindow
            #open window    
            popupWindow.open()

    #delete the model
    def Delete_model(self):
        #check if a model exists
        if os.path.exists("Model.png"):
            #remove model image
            os.remove("Model.png")
        #remove model from app image preview
        self.ids.model_image.source = "default.jpg"
        
    #updates the preview(image), of the model
    def Update_model_image(self,url):
        #updates the model image
        self.ids.model_image.source = url
        #reloads/refreshes the image
        self.ids.model_image.reload()


class Filechooser_Page(Screen):    

    #on selecting a item
    def selected(self, filename):
        print(filename)
        try:
            self.ids.image_show.source = filename[0]
        except: 
            pass
    #open a selected path/folder
    def open(self, path, filename):
       with open(os.path.join(path, filename[0])) as filee:
            print(filee.read())
    
    #submit choosen image
    def submit(self):
        #get current selected image, by selecting img url, from the file chooser preview
        im_ = self.ids.image_show.source
        #assign image to create model page, image preview
        self.sm.get_screen('Create_model_page').ids.create_image.source = im_
        #reloads/refreshes the create model page image 
        self.sm.get_screen('Create_model_page').ids.create_image.reload()      
        
#popup window for image preview model
class Image_popup(FloatLayout):
    #screen manager reference
    sm = None    
    windw = None

class Create_model_page(Screen):

    #show the image preview model popup
    def Show_image_popup(self,sourcee):    
        #if there is a model to delete         
        show = Image_popup()
        #add screen manager reference, to popup
        show.sm = self.sm
        #assign preview image to popup image
        show.ids.model_image.source = sourcee
        #create popup window
        popupWindow = Popup(title="Model Preview:", content=show, size_hint=(0.2,0.2))
        #assign popupWindow as reference, in order to close it via the button
        show.windw = popupWindow
        #open window     
        popupWindow.open()

    #update the main model page/preview/image
    def create_model(self):     
        #get process img 
        img = cv2.imread(self.ids.create_image.source)
        #model file name
        new_model = "Model.png"
        #create new model png
        cv2.imwrite(new_model, img )
        #assign new model img to 
        self.sm.get_screen('Main_Model_Page').Update_model_image(new_model)

    def process(self):
        #reloads/refreshes the image 
        self.ids.create_image.reload()
        #opencv reads image from preview, by reading the image url, from the preview image
        img = cv2.imread(self.ids.create_image.source)
        #new img url
        img_pros_url = "processed.png"
        #Image Processing steps, placeholder
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #rgb colors
        l_b = np.array([0, 32, 0])
        #hue
        u_b = np.array([255, 255, 255])
        mask = cv2.inRange(hsv, l_b, u_b)
        #create image from processed image
        res = cv2.bitwise_and(img, img, mask=mask)

        #save new processed image copy
        cv2.imwrite(img_pros_url, res )
        #show processed image
        self.ids.create_image.source = img_pros_url
        #reloads/refreshes the image
        self.ids.create_image.reload()
        


