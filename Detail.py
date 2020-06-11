import webbrowser

from kivy.uix.screenmanager import Screen


class Detail_page(Screen):

    def To_store(self,url):
        webbrowser.open(url)

    def Update_Page(self,product,sm):
        self.sm = sm
        self.ids.image_product.source = product.img_url
        self.ids.image_product.reload()
        self.ids.Product_name.text = product.product_name
        self.ids.Product_name.Product_text = product.text
        self.product = product
        #self.image_product = url 
        #lines that change detail properties
    
