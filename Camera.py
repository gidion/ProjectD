import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


class Camera_page(Screen):
    def on_pre_enter(self):
        try:
            camera = self.ids['camera']
            camera.pos_hint = {'left':0, 'center_y': 0.6}
            camera.resolution = (640, 480)
            camera.play = True
        except:
            pass
    def check_camera(self):
        try:
            camera = self.ids['camera']
            camera.pos_hint = {'left':0, 'center_y': 0.6}
            camera.resolution = (640, 480)
            camera.play = True
            return True
        except:
            return False
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
    def Countdown_camera(self):
        time.sleep(5)

        self.capture()



class CameraClick(BoxLayout):
    pass


class TestCamera(App):

    def build(self):
        return CameraClick()


class CameraWindow(Screen):
    pass
