from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from os import getcwd, mkdir
from os.path import exists, join
from shutil import rmtree
from android import api_version
from android.permissions import request_permissions, check_permission,\
    Permission
from android.runnable import run_on_ui_thread  
from textwrap import fill
from storage import PrivateStorage, SharedStorage
from picker import Picker

class StorageExample(App):

    def build(self):
        self.calledback = False
        self.start_ready = False
        # create picker listener
        self.picker = Picker(self.picker_callback)
        # Permission required for Picker()
        permissions = [Permission.READ_EXTERNAL_STORAGE]
        if api_version < 29:
            permissions.append(Permission.WRITE_EXTERNAL_STORAGE)
        request_permissions(permissions, self.callback)
        # cleanup if Android didn't
        temp = PrivateStorage().getCacheDir()
        if not temp:
            temp = PrivateStorage().getCacheDir('internal')
        temp = join(temp,"FromSharedStorage")
        if exists(temp):
            rmtree(temp)

        # layout
        self.label = Label(text = 'Greetings Earthlings')
        self.button = Button(text = 'Use Picker to get a Document',
                             on_press = self.picker_start,
                             size_hint=(1, .15))
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        return self.layout

    def on_start(self):
        self.start_ready = True
        if check_permission(Permission.READ_EXTERNAL_STORAGE):
            if api_version > 28 or\
               check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                self.callback(None,None)
               
    def callback(self,permissions,grants):
        if not self.start_ready or self.calledback:
            return
        self.calledback = True
        self.label_lines = []
        self.display()
        # Private Storage operations
        self.append("PRIVATE STORAGE")
        self.append("Install Dir:  " + str(exists(getcwd())))
        self.append("FilesDir:  " + str(exists(PrivateStorage().getFilesDir())))
        self.append("CacheDir:  " + str(exists(PrivateStorage().getCacheDir())))

        # Shared Storage operations
        self.append("PUBLIC STORAGE:")
        res0 = SharedStorage().insert('./test.txt', 'Documents')
        res1 = SharedStorage().insert('./test.txt', sub_dir= 'a/b')
        res2 = SharedStorage().insert('./test.txt', 'Downloads')
        res3 = SharedStorage().insert('./test.jpg', 'Pictures')
        res4 = SharedStorage().insert('./test.mp3')
        res5 = SharedStorage().insert('./test.ogg', 'Music')
        copy_path1 = SharedStorage().retrieve('test.txt')
        copy_path2 = SharedStorage().retrieve('test.txt', 'Documents', 'a/b')
        copy_path3 = SharedStorage().retrieve('10_28_14.jpg', 'DCIM',
                                              '2021_03_12','CameraXF')
        copy_path4 = SharedStorage().retrieve('10_33_48.mp4', 'DCIM',
                                              '2021_03_12','CameraXF')
        res6 = SharedStorage().delete('test.mp3', 'Music')

        self.append("insert test.txt       " + str(res0))
        self.append("insert a/b/test.txt:  " + str(res1))
        self.append("insert test.txt in Downloads:  " + str(res2))
        self.append("insert test.jpg:      " + str(res3))
        self.append("insert test.mp3:      " + str(res4))
        self.append("insert test.ogg:      " + str(res5))
        self.append("retrieve test.txt     " + str(exists(copy_path1)))
        self.append("retrieve a/b/test.txt " + str(exists(copy_path2)))
        self.append("retrieve CameraXF jpg " + str(exists(copy_path3)))
        self.append("retrieve CameraXF mp4 " + str(exists(copy_path4)))
        self.append("deleted test.mp3      " + str(res6))

        self.display()

    # Picker interface
    def picker_start(self,bt):
        self.picker.pick_file("application/*")

    def picker_callback(self,uri):
        try:
            path = SharedStorage().retrieveUri(uri)
            self.append("Retrieved from Picker  " + str(exists(path)))
            self.display()
        except Exception as e:
            print('ERROR StorageExample.picker_callback():\n' + str(e))

    # Label text
    def append(self, name):
        self.label_lines.append(name)

    @run_on_ui_thread
    def display(self):
        if self.label:
            self.label.text = ''
            for r in self.label_lines:
                self.label.text += fill(r, 40) + '\n'

StorageExample().run()
