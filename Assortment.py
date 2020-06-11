import mysql.connector
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.uix.imagelist import SmartTileWithLabel
from mysql.connector import Error

from admin import image_names

assortment_list = []


Builder.load_file('Assortment.kv')


class Product_item():
    id = -1
    product_name = ''
    # file path to image
    img_url = ''
    # web link to product on webshop
    link = 'www.google.com'
    # description or summary of the product
    text = ''

    def __init__(self, id, product_name, img_url, link, text):
        self.id = id
        self.product_name = product_name
        self.img_url = img_url
        self.link = link
        self.text = text


class MySmartTileWithLabel(SmartTileWithLabel):
    pass


class Assortment_page(Screen):
    sm: None

    def on_enter(self):
        if(not(App.get_running_app().done_assortment)):

            ############# DB

            query = "SELECT * FROM clothing"

            try:
                # query blob data form the clothing table
                connection = mysql.connector.connect(host='localhost',
                                                     database='tashira',
                                                     user='root',
                                                     password='')
                cursor = connection.cursor()
                cursor.execute(query)
                records = cursor.fetchall()

                row_counter = 0

                for row in records:
                    assortment_list.append(Product_item(str(row_counter), row[1], 'Clothing\\item_'+image_names[row_counter], "https://www.tashira.nl/", 'Image'+str(row_counter)))
                    row_counter += 1

            except Error as error:
                print(error)

            finally:
                cursor.close()
                connection.close()

            ########### DB

            for item in assortment_list:
                #combine the products text into the widgets text
                main_text = '[size=20][color=#ffffff]' + str(item.product_name) + '[/color][/size]\n[size=10]2020_09_07_1842.jpg[/size]'
                #create widget MySmartTileWithLabel
                temp = MySmartTileWithLabel(id=item.id, text=main_text)
                #assign screen manager to MySmartTileWithLabel widget, without using the init
                temp.sm = self.sm
                #assign the product info to the MySmartTileWithLabel
                temp.product = item
                #add the widget to the gridlayout
                self.ids.Items_Grid.add_widget(temp)
                #crop the image for the gallery
                App.get_running_app().crop_image_for_tile(temp, temp.size, item.img_url)
        App.get_running_app().done_assortment = True
    pass

class Assortment_page(Screen):
    container = ObjectProperty(None)

class ImageButton(ButtonBehavior, Image):
    pass