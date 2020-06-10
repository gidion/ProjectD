from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class ImageButton(ButtonBehavior, Image):
    pass

class Assortment_page(Screen):
    container = ObjectProperty(None)
