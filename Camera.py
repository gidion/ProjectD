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
import numpy as np
import cv2 
import os

class Camera_page(Screen):
    def capture(self):
        #get camera widget
        camera = self.ids['camera']
        #timestr = time.strftime("%Y%m%d_%H%M%S")
        #export image from camera to png
        camera.export_to_png("PIC_1.png")
        #assign camera image, to create model page preview
        self.sm.get_screen('Create_model_page').ids.create_image.source = "PIC_1.png"
        #reloads/refreshes the create model page image preview
        self.sm.get_screen('Create_model_page').ids.create_image.reload()
        #redirect back to create model page
        self.sm.current = 'Create_model_page'
        #print("Captured2")

class CameraClick(BoxLayout):
    pass


class TestCamera(App):

    def build(self):
        return CameraClick()


class CameraWindow(Screen):
    pass
