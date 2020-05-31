#-*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.widget import Widget

from kivy.properties import StringProperty 
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import os,sys
import threading
import csv
import time
import numpy

resource_add_path("IPAexfont00301")
LabelBase.register(DEFAULT_FONT, "ipaexg.ttf")

# 監視対象ディレクトリを指定する
target_dir = 'C:\\Users\\kuchida\\Pictures\\Wireless Transmitter Utility\\D810 2019212\\DCIM\\197ND810'

# FileSystemEventHandler の継承クラスを作成
class FileChangeHandler(FileSystemEventHandler):
     # ファイル作成時のイベント
     def on_created(self, event):
         filepath = event.src_path
         filename = os.path.basename(filepath)
         image_src_dir = target_dir + "\\" + filename
         print(image_src_dir)
         set_image_src(image_src_dir)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class TextWidget(Widget):
    global carcass_list
    carcass_order = StringProperty()    # プロパティの追加
    body_number = StringProperty()
    barcode = StringProperty()
    filepath = StringProperty()
    barcode_input = TextInput()
    image = ObjectProperty(None)
    image_src = StringProperty('')
    carcass_list = []


    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.body_number = '枝肉番号:'
        self.carcass_order = '出場順:'
        self.barcode = ''
        self.filepath = ''
        self.image_src = 'C:\\Users\\kuchida\\Pictures\\_DSC4656 (2).JPG'
        Clock.schedule_interval(self.update, 1)
        pass


    def update(self, dt):
        self.image.reload()
        
    def set_image_src(self,src):
        self.image_src = src

    def okClicked(self):        # ボタンをクリック時
        print("hello")

    def cancelClicked(self):        # ボタンをクリック時
        print("cancel")

    def barcodeDetected(self,read_barcode):
        print(read_barcode)
        print("barcode detected")
        if(len(read_barcode) == 13):
            print(read_barcode[0:4])
            body_number = read_barcode[0:4]
            self.barcode = read_barcode
            self.body_number = '枝肉番号:' + body_number
            self.ids.barcode_input_sub.focus = True
            self.ids.barcode_input_sub.text = ''
            #出場順検索
            print(carcass_list)
            self.carcass_order = '出場順:' + str(carcass_list[[d[1] for d in carcass_list].index(body_number)][0])
        
    
    def barcodeDetectedSub(self,read_barcode):
        print(read_barcode)
        print("barcode detected")
        if(len(read_barcode) == 13):
            print(read_barcode[0:4])
            body_number = read_barcode[0:4]
            self.barcode = read_barcode
            self.body_number = '枝肉番号:' + body_number  
            self.ids.barcode_input.focus = True
            self.ids.barcode_input.text = ''

    
    def sansyoClicked(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
 
    def dismiss_popup(self):
        self._popup.dismiss()
 
    def load(self, path, filename):
        load_filepath = str(filename[0])  #filenameは配列で返ってくる
        self.dismiss_popup()
        load_carcass_list = numpy.loadtxt(fname=load_filepath,skiprows=0,delimiter=",",dtype="U20")[:,0:2]
        for line in load_carcass_list:
            carcass_list.append([line[0],line[1]])
        print(carcass_list)
        self.ids.barcode_input.focus = True

        
        
class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = 'greeting'

    def build(self):
        TestApp.widget = TextWidget()
        return TestApp.widget

    def set_image_src(self,src):
        self.widget.set_image_src(src)


def filechangelitener():
    # ファイル監視の開始
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()
    # 処理が終了しないようスリープを挟んで無限ループ
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def set_image_src(src):
    print("1")
    TestApp().set_image_src(src)


def app_run(app, a):
    app.run()

if __name__ == '__main__':


    
    file_thread = threading.Thread(target=filechangelitener,daemon=True)
    file_thread.start()

    TestApp().run()
    



    


