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


import test as testerino




#onfig.set('graphics', 'width', '412')
#Config.set('graphics', 'height', '732')

#.kv must be the same, but without App
# Loading Multiple .kv files  
Builder.load_file('Model_User/Main_Model_page.kv') 
Builder.load_file('Model_User/Create_model_page.kv') 
Builder.load_file('Model_User/Filechooser_page.kv') 

class WindowManager(ScreenManager):
    pass

class Main_Model_Page(Screen):
    img = 'default.jpg'
    #popup window for deleting model

    #show the delete model popup
    def Show_delete_popup(self):             
        show = Delete_popup()
        popupWindow = Popup(title="Delete Model?", content=show, size_hint=(0.7,0.7))
        
        #open windows     
        popupWindow.open()
    
    def test(self):
        print('yup')

    #delete the model
    def Delete_model(self):
        App.get_running_app().model = 'default.jpg'
        self.ids.model_image.source = 'default.jpg'
        #closes popup window
        lambda: self.popup_exit.dismiss()

    #updates the preview(image), of the model
    def Update_model_image(self,url):
        App.get_running_app().model = url
        self.ids.model_image.source = url

lol = testerino.Special_specific_screen()

class Filechooser_Page(Screen):    
    mangr = ScreenManager
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
        app = App.get_running_app()
    
        im_ = self.ids.image_show.source
        self.ids.image_show.source = 'default.jpg'
        app.root.get_screen('Create_model_page').ids.create_image.source = im_       
        

class Create_model_page(Screen):
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
   

class Delete_popup(FloatLayout):
    pass

kv = Builder.load_file("main.kv")

class MainApp(App):
    model = 'default.jpg'
    def build(self):
        return kv

if __name__ == '__main__':
    MainApp().run()