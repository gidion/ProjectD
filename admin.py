import ntpath
import os

import mysql.connector
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from mysql.connector import Error

imagefile_extensions = {".jpg", "jpeg", ".png", "bmp", "gif"}
image_names = []


# Write database files to local disk
def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


# Database connection / fetch
def read_blob(filename):
    # select table
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

        for row in records:
            # write blob data into a file with 'item_' prefix and '.jpg' file extension
            if row[1][-4:] in imagefile_extensions:
                write_file(row[2], (filename + 'item_' + row[1]))
                image_names.append((+ row[1]))
            else:
                write_file(row[2], (filename + 'item_' + row[1] + '.jpg'))
                image_names.append((row[1] + '.jpg'))

    except Error as error:
        print(error)

    finally:
        cursor.close()
        connection.close()


# Create 'Clothing' Directory if it doesn't exist
if not os.path.exists('Clothing'):
    os.mkdir('Clothing')
    print("Directory", '"Clothing"',  "Created ")

# Write database files into Clothing directory
read_blob("Clothing\\")


class Admin(Screen):
    container = ObjectProperty(None)
    clothing_dict = {}

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.container.bind(minimum_height=self.container.setter('height'))
        self.load_images()

    def edit_item(self, instance):
        # Convert digital data to binary format (Blob)
        def convertToBinaryData(filename):
            with open(filename, 'rb') as file:
                binaryData = file.read()
            return binaryData

        # Update blob image file
        def update_BLOB(photo):
            try:
                connection = mysql.connector.connect(host='localhost',
                                                     database='tashira',
                                                     user='root',
                                                     password='')

                cursor = connection.cursor()

                itemPicture = convertToBinaryData(photo)
                itemName = instance.id[5:-4]

                if "." in isolate_filename(edit_filechooser.selection[0][:-4]):
                    newName = isolate_filename(edit_filechooser.selection[0][:-5])
                else:
                    newName = isolate_filename(edit_filechooser.selection[0][:-4])

                query = "UPDATE clothing " \
                        "SET image = %s " \
                        "WHERE name  = %s"
                query2 = "UPDATE clothing SET name = %s WHERE name = %s"

                args = (itemPicture, itemName)
                args2 = (newName, itemName)


                # Attempt to execute SQL
                try:
                    cursor.execute(query, args)
                    cursor.execute(query2, args2)
                    os.remove("Clothing\\" + str(instance.id))
                # Duplicate found
                except:
                    duplicate_box = BoxLayout()
                    duplicate_cancel = Button(text='Close')

                    duplicate_box.add_widget(duplicate_cancel)

                    duplicate_popup = Popup(content=duplicate_box,
                                            title="This item already exists",
                                            auto_dismiss=True,
                                            size_hint=(None, None),
                                            size=(400, 100))

                    duplicate_cancel.bind(on_release=duplicate_popup.dismiss)
                    duplicate_popup.open()

                connection.commit()

            except Error as error:
                print(error)

            finally:
                cursor.close()
                connection.close()
                self.refresh_page()

        # Isolate the filename from its path
        def isolate_filename(path):
            head, tail = ntpath.split(path)
            return tail or ntpath.basename(head)

        # Update Database and list of items to include the updated entry
        def update_item_list(instance):

            # Nothing selected Error
            if not edit_filechooser.selection:
                none_box = BoxLayout()
                none_cancel = Button(text='Close')
                none_box.add_widget(none_cancel)

                none_popup = Popup(content=none_box,
                              title="Error: Nothing selected",
                              auto_dismiss=True,
                              size_hint=(None, None),
                              size=(400, 100))

                # Bind Cancel button to dismiss popup
                none_cancel.bind(on_release=none_popup.dismiss)
                none_popup.open()

            # Image was selected
            elif isolate_filename(str(edit_filechooser.selection[0][-4:])) in imagefile_extensions:
                # Check if final 4 characters contain period - to separate jpeg from jpg
                if "." in isolate_filename(str(edit_filechooser.selection[0][:-4])):
                    update_BLOB(str(edit_filechooser.selection[0]))
                else:
                    update_BLOB(str(edit_filechooser.selection[0]))

                read_blob("Clothing\\")

                self.refresh_page()
                edit_popup.dismiss()

            # Non-Image was selected
            else:
                error_box = BoxLayout()
                popup_cancel = Button(text='Close')
                error_box.add_widget(popup_cancel)

                error_popup = Popup(content=error_box,
                              title="Error: File is not an Image",
                              auto_dismiss=True,
                              size_hint=(None, None),
                              size=(400, 100))

                # Bind Cancel button to dismiss popup
                popup_cancel.bind(on_release=error_popup.dismiss)
                error_popup.open()

        # create content and add to the popup
        edit_box = GridLayout(rows=3)

        edit_filechooser = FileChooserListView(path=r'C:')
        edit_filechooser.bind(on_selection=lambda x: self.selected(edit_filechooser.selection))
        edit_box.add_widget(edit_filechooser)

        # Open / Cancel buttons
        edit_open_btn = Button(text='Open', size_hint=(None, None), height=40, width=self.width-25)
        edit_open_btn.bind(on_release=update_item_list)

        edit_cancel_btn = Button(text="Cancel", size_hint=(None, None), height=40, width=self.width-25)

        edit_box.add_widget(edit_open_btn)
        edit_box.add_widget(edit_cancel_btn)

        edit_popup = Popup(content=edit_box,
                           title="Choose an image",
                           auto_dismiss=True,
                           )

        edit_cancel_btn.bind(on_release=edit_popup.dismiss)

        # Open the popup
        edit_popup.open()

    def add_item(self, instance):

        # Convert digital data to binary format (Blob)
        def convertToBinaryData(filename):
            with open(filename, 'rb') as file:
                binaryData = file.read()
            return binaryData

        def insert_BLOB(item_id, name, photo):
            try:
                connection = mysql.connector.connect(host='localhost',
                                                     database='tashira',
                                                     user='root',
                                                     password='')

                cursor = connection.cursor()
                query = " INSERT INTO clothing (id, name, image) VALUES (%s,%s,%s)"

                itemPicture = convertToBinaryData(photo)

                # Convert data into tuple format
                insert_blob_tuple = (item_id, name, itemPicture)
                cursor.execute(query, insert_blob_tuple)
                connection.commit()

            except Error as error:

                print(error)

            finally:
                cursor.close()
                connection.close()

        # Isolate the filename from its path
        def isolate_filename(path):
            head, tail = ntpath.split(path)
            return tail or ntpath.basename(head)

        # Insert into Database and update the list of items to include the new entry
        def update_item_list(instance):

            # Nothing selected Error
            if not self.add_filechooser.selection:
                none_box = BoxLayout()
                none_cancel = Button(text='Close')
                none_box.add_widget(none_cancel)

                none_popup = Popup(content=none_box,
                              title="Error: Nothing selected",
                              auto_dismiss=True,
                              size_hint=(None, None),
                              size=(400, 100))

                # Bind Cancel button to dismiss popup
                none_cancel.bind(on_release=none_popup.dismiss)
                none_popup.open()

            # Image was selected
            elif isolate_filename(str(self.add_filechooser.selection[0][-4:])) in imagefile_extensions:

                query_name = isolate_filename(str(self.add_filechooser.selection[0][:-4]))
                if 'item_' in query_name:
                    query_name = query_name[5:]

                query = 'SELECT * FROM clothing WHERE name = "' + query_name + '"'
                try:
                    connection = mysql.connector.connect(host='localhost',
                                                         database='tashira',
                                                         user='root',
                                                         password='')
                    cursor = connection.cursor(buffered=True)
                    cursor.execute(query)
                    result = cursor.rowcount
                except Error as e:
                    print(e)
                finally:
                    cursor.close()
                    connection.close()
                    self.refresh_page()

                if result == 0:
                    # Check if final 4 characters contain period - to separate jpeg from jpg
                    if "." in isolate_filename(str(self.add_filechooser.selection[0][:-4])):
                        insert_BLOB('NULL', isolate_filename(str(self.add_filechooser.selection[0][:-5])), str(self.add_filechooser.selection[0]))
                    else:
                        insert_BLOB('NULL', isolate_filename(str(self.add_filechooser.selection[0][:-4])), str(self.add_filechooser.selection[0]))
                else:
                    add_duplicate_box = BoxLayout()
                    add_duplicate_cancel = Button(text='Close')

                    add_duplicate_box.add_widget(add_duplicate_cancel)

                    add_duplicate_popup = Popup(content=add_duplicate_box,
                                            title="This item already exists",
                                            auto_dismiss=True,
                                            size_hint=(None, None),
                                            size=(400, 100))

                    # Bind Cancel button to dismiss popup
                    add_duplicate_cancel.bind(on_release=add_duplicate_popup.dismiss)
                    add_duplicate_popup.open()

                read_blob("Clothing\\")

                self.refresh_page()
                popup.dismiss()

            # Non-Image was selected
            else:
                error_box = BoxLayout()
                popup_cancel = Button(text='Close')
                error_box.add_widget(popup_cancel)

                error_popup = Popup(content=error_box,
                                    title="Error: File is not an Image",
                                    auto_dismiss=True,
                                    size_hint=(None, None),
                                    size=(400, 100))

                # Bind Cancel button to dismiss popup
                popup_cancel.bind(on_release=error_popup.dismiss)
                error_popup.open()

        # create content and add to the popup
        popup_box = GridLayout(rows=3)

        self.add_filechooser = FileChooserListView(path=r'C:')
        self.add_filechooser.bind(on_selection=lambda x: self.selected(self.add_filechooser.selection))
        popup_box.add_widget(self.add_filechooser)

        # Open / Cancel buttons
        open_btn = Button(text='Open', size_hint=(None, None), height=40, width=self.width-25)
        open_btn.bind(on_release=update_item_list)

        cancel_btn = Button(text="Cancel", size_hint=(None, None), height=40, width=self.width-25)

        popup_box.add_widget(open_btn)
        popup_box.add_widget(cancel_btn)

        popup = Popup(content=popup_box,
                      title="Choose an image",
                      auto_dismiss=True,
                      )

        cancel_btn.bind(on_release=popup.dismiss)

        # Open the popup
        popup.open()

    # Set ID/name to delete
    def delete_setup(self, instance):

        # Popup window for delete button confirmation
        def delete_popup(instance):
            # create content and add to the popup
            popup_box = BoxLayout()
            popup_confirm = Button(text='Confirm')
            popup_cancel = Button(text='Cancel')

            popup_box.add_widget(popup_confirm)
            popup_box.add_widget(popup_cancel)

            popup = Popup(content=popup_box,
                          title="Are you sure you want to delete this item?",
                          auto_dismiss=True,
                          size_hint=(None, None),
                          size=(400, 100))

            # Bind Cancel button to dismiss popup
            popup_cancel.bind(on_release=popup.dismiss)

            # This is to bind the Confirm button to 2 functions - dismiss the popup, then run delete_items()
            def pop_delete(instance):
                popup.dismiss()
                delete_items(instance)
            popup_confirm.bind(on_release=pop_delete)

            popup.open()

        # Delete items locally and in Database
        def delete_items(instance):
            if os.path.exists('Clothing/'+clothing_name_full):
                os.remove('Clothing/'+clothing_name_full)

                query = "DELETE FROM clothing WHERE name = '" + str(clothing_name) + "'"

                try:
                    connection = mysql.connector.connect(host='localhost',
                                                         database='tashira',
                                                         user='root',
                                                         password='')
                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()

                    print(cursor.rowcount, "record(s) deleted from database")
                except Error as e:
                    print(e)
                finally:
                    cursor.close()
                    connection.close()
                    self.refresh_page()
            else:
                print("The file does not exist")

        # Clothing id is used as index in the clothing folder
        clothing_id = instance.id

        # check if final 4 characters in string contains a period, to separate jpg from jpeg
        if "." in os.listdir('Clothing/')[int(clothing_id)-1][-4:]:
            clothing_name = os.listdir('Clothing/')[int(clothing_id)-1][5:-4]
        else:
            clothing_name = os.listdir('Clothing/')[int(clothing_id) - 1][5:-5]
        # Full non-sliced file name
        clothing_name_full = os.listdir('Clothing/')[int(clothing_id)-1]
        # Run delete_popup()
        delete_popup(instance)



    # Create a dictionary with the images / buttons to display on the page, then add them to the page
    def load_images(self):
        dir_name = 'Clothing/'
        file_count = sum([len(files) for r, d, files in os.walk(dir_name)])

        self.add_item_button.bind(on_release=self.add_item)

        # For every file in the Clothing directory
        for x in range(file_count):

            # Add an image from Clothing/ and its Edit/Delete buttons to self.clothing_dict at index[x] as a tuple
            self.clothing_dict[x] = (ImageButton(
                           source="Clothing\\" + os.listdir(dir_name)[x],
                           size_hint_y=None,
                           height=200,
                           id=str(x+1)),
                       Button(
                           text='Edit',
                           id=str(os.listdir(dir_name)[x]),
                           size=(80, 60),
                           size_hint=(None, None)),
                       Button(
                           text='Delete',
                           id=str(x+1),
                           size=(80, 60),
                           size_hint=(None, None))
                       )

        # Bind the buttons from dictionary
        for x in range(len(self.clothing_dict)):
            self.clothing_dict[x][1].bind(on_release=self.edit_item)
            self.clothing_dict[x][2].bind(on_release=self.delete_setup)

        # Add stuff from the dictionary into the page container
        for x in range(len(self.clothing_dict)):
            for y in range(len(self.clothing_dict[x])):
                self.container.add_widget(self.clothing_dict[x][y])

    def refresh_page(self):
        self.clothing_dict.clear()      # clear dictionary to rebuild it in load_images() without deleted item
        self.container.clear_widgets()  # clear all widgets from container
        self.load_images()              # re-add widgets without deleted item
        #print('Refreshed')


class ImageButton(ButtonBehavior, Image):
    pass
