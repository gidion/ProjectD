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

import Home as Home_
import Gallery as Gallery_
import Camera as Camera_
import Model as Model_
import Assortment as Assortment_
import Combine as Combine_

import Detail as Detail_
import numpy as np

import cv2 
import os


RAD_MULT = 0.25  # Blur Radius Multiplier

Window.size = (450, 800)

Builder.load_file('Home.kv') 
Builder.load_file('Gallery.kv') 
Builder.load_file('Camera.kv') 
Builder.load_file('Model.kv') 
Builder.load_file('Assortment.kv') 
Builder.load_file('Detail.kv') 
Builder.load_file('Combine.kv') 

class ImageButton(ButtonBehavior, Image):
    pass


class ShadowWidget(Label):

    shadow_texture1 = props.ObjectProperty(None)
    shadow_pos1 = props.ListProperty([0, 0])
    shadow_size1 = props.ListProperty([0, 0])

    shadow_texture2 = props.ObjectProperty(None)
    shadow_pos2 = props.ListProperty([0, 0])
    shadow_size2 = props.ListProperty([0, 0])

    elevation = props.NumericProperty(1)
    _shadow_clock = None

    _shadows = {
        1: (1, 3, 0.12, 1, 2, 0.24),
        2: (3, 6, 0.16, 3, 6, 0.23),
        3: (10, 20, 0.19, 6, 6, 0.23),
        4: (14, 28, 0.25, 10, 10, 0.22),
        5: (19, 38, 0.30, 15, 12, 0.22)
    }

    # Shadows for each elevation.
    # Each tuple is: (offset_y1, blur_radius1, color_alpha1, offset_y2, blur_radius2, color_alpha2)
    # The values are extracted from the css (box-shadow rule).

    def __init__(self, *args, **kwargs):
        super(ShadowWidget, self).__init__(*args, **kwargs)

        self._update_shadow = Clock.create_trigger(self._create_shadow)

    def on_size(self, *args, **kwargs):
        self._update_shadow()

    def on_pos(self, *args, **kwargs):
        self._update_shadow()

    def on_elevation(self, *args, **kwargs):
        self._update_shadow()

    def _create_shadow(self, *args):
        # print "update shadow"
        ow, oh = self.size[0], self.size[1]

        offset_x = 0

        # Shadow 1
        shadow_data = self._shadows[self.elevation]
        offset_y = shadow_data[0]
        radius = shadow_data[1]
        w, h = ow + radius * 6.0, oh + radius * 6.0
        t1 = self._create_boxshadow(ow, oh, radius, shadow_data[2])
        self.shadow_texture1 = t1
        self.shadow_size1 = w, h
        self.shadow_pos1 = self.x - \
            (w - ow) / 2. + offset_x, self.y - (h - oh) / 2. - offset_y

        # Shadow 2
        shadow_data = self._shadows[self.elevation]
        offset_y = shadow_data[3]
        radius = shadow_data[4]
        w, h = ow + radius * 6.0, oh + radius * 6.0
        t2 = self._create_boxshadow(ow, oh, radius, shadow_data[5])
        self.shadow_texture2 = t2
        self.shadow_size2 = w, h
        self.shadow_pos2 = self.x - \
            (w - ow) / 2. + offset_x, self.y - (h - oh) / 2. - offset_y

    def _create_boxshadow(self, ow, oh, radius, alpha):
        # We need a bigger texture to correctly blur the edges
        w = ow + radius * 6.0
        h = oh + radius * 6.0
        w = int(w)
        h = int(h)
        texture = Texture.create(size=(w, h), colorfmt='rgba')
        im = ImagePIL.new('RGBA', (w, h), color=(1, 1, 1, 0))

        draw = ImageDraw.Draw(im)
        # the rectangle to be rendered needs to be centered on the texture
        x0, y0 = (w - ow) / 2., (h - oh) / 2.
        x1, y1 = x0 + ow - 1, y0 + oh - 1
        draw.rectangle((x0, y0, x1, y1), fill=(0, 0, 0, int(255 * alpha)))
        im = im.filter(ImageFilter.GaussianBlur(radius * RAD_MULT))
        texture.blit_buffer(im.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        return texture


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    target = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class NavDrawerAndScreenManagerApp(MDApp):

    def crop_image_for_tile(self, instance, size, path_to_crop_image):
        if not os.path.exists(os.path.join(self.directory, path_to_crop_image)):
            size = (int(size[0]), int(size[1]))
            path_to_origin_image = path_to_crop_image.replace("_tile_crop", "")
            crop_image(size, path_to_origin_image, path_to_crop_image)
        instance.source = path_to_crop_image

    def build(self):
        return Builder.load_file("main.kv")

    def openScreen(self, itemdrawer):
        self.openScreenName(itemdrawer.target)
        self.root.ids.nav_drawer.set_state("close")

   
    def open_model(self):
        self.root.ids.sm.get_screen("Main_Model_Page")
        

    def openScreenName(self, screenName):
        self.root.ids.sm.current = screenName
        #model check for specific screen(s)
        if(screenName == 'Main_Model_Page'):
            #call Check_existing_model on screen enter
            self.root.ids.sm.get_screen("Main_Model_Page").Check_existing_model()

    def on_start(self):
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="Home", text="Home",
                       icon="home-circle-outline",
                       on_release=self.openScreen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="Gallery", text="Gallery",
                       icon="image-multiple",
                       on_release=self.openScreen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="Main_Model_Page", text="Model",
                       icon="camera",
                       on_release=self.openScreen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="Assortment", text="Assortment",
                       icon="tshirt-v",
                       on_release=self.openScreen)
        )
        self.root.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="Settings", text="Settings",
                       icon="settings-outline",
                       on_release=self.openScreen)
        )


if __name__ == "__main__":
    NavDrawerAndScreenManagerApp().run()
