import json

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.imagelist import SmartTileWithLabel


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

class Gallery_page(Screen):
    sm: None
    def on_enter(self):
        #load saved combinations from file
        temp_list = self.Load_combinations(False)
        #refresh/show gallery items
        self.Show_combinations(self.ids.Items_Grid,temp_list)
    
    def Show_combinations(self,Item_Grid,combinations):     
        #remove previous gallery items from grid layout
        Item_Grid.clear_widgets()

        #loop through each combinations
        for item in combinations:
            #combine the products text into the widgets text
            main_text =  '[size=20][color=#ffffff]' + str(item.product_name) + '[/color][/size]\n[size=10]2020_09_07_1842.jpg[/size]'
            #create widget MySmartTileWithLabel
            
            temp = Create_gallery_widget(self.sm, item, item.id, Item_Grid)                 
        
        

    def Load_combinations(self,in_json):
        #combinations in dict/json
        loaded_combinations = {}
        #combinations as class objects
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

def Create_gallery_widget(screen_manager, _item, _id, _itemgrid):
    temp = CombSmartTileWithLabel(id = str(_item.id))
    #assign screen manager to CombSmartTileWithLabel widget, without using the init
    temp.sm = screen_manager
    #assign the product info to the CombSmartTileWithLabel
    temp.product = _item
    #assign combination id
    temp.comb_id = _id
    #add the widget to the gridlayout
    _itemgrid.add_widget(temp) 
    #crop the image for the gallery
    try:
        App.get_running_app().crop_image_for_tile(temp, temp.size, \
        _item.img_url)
        #combination image is not found/missing
    except:
        App.get_running_app().crop_image_for_tile(temp, temp.size, \
        'default.jpg'  )
    temp.reload()    


        
class CombSmartTileWithLabel(SmartTileWithLabel):
    pass

