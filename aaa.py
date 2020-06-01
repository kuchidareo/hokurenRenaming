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

from PIL import Image

import os,sys
import threading
import csv
import time
import datetime
import numpy

resource_add_path("IPAexfont00301")
LabelBase.register(DEFAULT_FONT, "ipaexg.ttf")

date_today_str = datetime.date.today().strftime('%Y%m%d')

# 監視対象ディレクトリを指定する
target_dir = 'C:\\Users\\kuchida\\Pictures\\Wireless Transmitter Utility\\D810 2019212\\DCIM\\197ND810'

hokuren_dir = 'C:\\Users\\kuchida\\Desktop\\hokuren'
h_today_dir = hokuren_dir + '\\' + date_today_str
resize_image_dir = h_today_dir + '\\resize'

if(not os.path.exists(hokuren_dir)):
    os.mkdir(hokuren_dir)
if(not os.path.exists(h_today_dir)):
    os.mkdir(h_today_dir)
if(not os.path.exists(resize_image_dir)):
    os.mkdir(resize_image_dir)

chikudai_dir = 'C:\\Users\\kuchida\\Desktop\\chikudai'
c_today_dir = chikudai_dir + '\\' + date_today_str

if(not os.path.exists(chikudai_dir)):
    os.mkdir(chikudai_dir)
if(not os.path.exists(c_today_dir)):
    os.mkdir(c_today_dir)

global display_image_path_list
global hokuren_image_path_list
global original_image_path_list

display_image_path_list = []
hokuren_image_path_list = []
original_image_path_list = []


global barcode_list
global body_number_list
global carcass_order_list

barcode_list = []
body_number_list = []
carcass_order_list = []


# FileSystemEventHandler の継承クラスを作成
class FileChangeHandler(FileSystemEventHandler):
     # ファイル作成時のイベント
     def on_created(self, event):
         filepath = event.src_path
         filename = os.path.basename(filepath)
         if 'JPG' in filename:
            image_src_dir = target_dir + "\\" + filename
            resize_and_set_image(image_src_dir)

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
        self.image_src = ''
        Clock.schedule_interval(self.update, 1)
        pass


    def update(self, dt):
        self.image.reload()
        
    def set_image_src(self,src):
        self.image_src = src

    def set_textfocus(self):
        self.ids.barcode_input.text = ''
        self.ids.barcode_input_sub.text = ''
        self.ids.barcode_input.focus = False
        self.ids.barcode_input_sub.focus = False
        self.ids.barcode_input.focus = True

    def okClicked(self):        # ボタンをクリック時
        print(barcode_list)
        print(original_image_path_list)
        print(carcass_order_list)
        if os.path.exists(c_today_dir+'\\帯広'+date_today_str+'_'+self.body_number[5:]+'.jpg'):
            os.remove(c_today_dir+'\\帯広'+date_today_str+'_'+self.body_number[5:]+'.jpg')
        os.rename(original_image_path_list[0],c_today_dir+'\\帯広'+date_today_str+'_'+self.body_number[5:]+'.jpg')
        if os.path.exists(h_today_dir+'\\'+self.carcass_order[4:]+'_'+self.body_number[5:]+'.jpg'):
            os.remove(h_today_dir+'\\'+self.carcass_order[4:]+'_'+self.body_number[5:]+'.jpg')
        os.rename(hokuren_image_path_list[0],h_today_dir+'\\'+self.carcass_order[4:]+'_'+self.body_number[5:]+'.jpg')
        del display_image_path_list[0:1]
        del hokuren_image_path_list[0:1]
        del original_image_path_list[0:1]
        del barcode_list[0:1]
        del body_number_list[0:1]
        del carcass_order_list[0:1]

        if len(display_image_path_list) > 0:
            self.image_src = display_image_path_list[0]
        else:
            self.image_src = ''
        if len(barcode_list)>0 and len(body_number_list)>0 and len(carcass_order_list)>0:
            self.barcode = barcode_list[0]
            self.body_number = '枝肉番号:' + body_number_list[0]
            self.carcass_order = '出場順:' + carcass_order_list[0]
        else:
            self.body_number = '枝肉番号:'
            self.carcass_order = '出場順:'
            self.barcode = ''

        self.set_textfocus()
        

    def cancelClicked(self):        # ボタンをクリック時
        display_image_path_list = []
        original_image_path_list = []
        barcode_list = []
        body_number_list = []
        carcass_order_list = []
        self.body_number = '枝肉番号:'
        self.carcass_order = '出場順:'
        self.barcode = ''
        self.image_src = ''

        self.set_textfocus()

    def barcodeDetected(self,read_barcode):
        if(len(read_barcode) == 48):
            body_number = read_barcode[38:42]
            barcode_list.append(read_barcode)
            body_number_list.append(body_number)
            carcass_order_list.append(str(carcass_list[[d[1] for d in carcass_list].index(body_number)][0]))
            if(self.barcode == ''):
                self.barcode = read_barcode
                self.body_number = '枝肉番号:' + body_number
                self.carcass_order = '出場順:' + str(carcass_list[[d[1] for d in carcass_list].index(body_number)][0])
        self.ids.barcode_input_sub.text = ''
        self.ids.barcode_input_sub.focus = True

    def barcodeDetectedSub(self,read_barcode):
        if(len(read_barcode) == 48):
            body_number = read_barcode[38:42]
            barcode_list.append(read_barcode)
            body_number_list.append(body_number)
            carcass_order_list.append(str(carcass_list[[d[1] for d in carcass_list].index(body_number)][0]))
            if(self.barcode == ''):
                self.barcode = read_barcode
                self.body_number = '枝肉番号:' + body_number
                self.carcass_order = '出場順:' + str(carcass_list[[d[1] for d in carcass_list].index(body_number)][0])
        self.ids.barcode_input.text = ''
        self.ids.barcode_input.focus = True

    
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

    def image_check(self):
        return self.widget.image_src


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
    TestApp().set_image_src(src)

def resize_and_set_image(src):
    img = Image.open(src)
    filename = src[src.rfind('\\')+1:]
    filename = filename[:filename.rfind('.')+1]
    img = Image.open(src)
    ##for hokuren
    img = img.resize((int(img.width / 4), int(img.height / 4)))
    if img.width > img.height:
        ##img = img.rotate(-90)
        img = img.transpose(Image.ROTATE_270)

    img.save(h_today_dir +'\\'+ filename + '.png')
    ##for display
    img.save(resize_image_dir +'\\resized_'+ filename + '.jpg')

    original_image_path_list.append(src)
    hokuren_image_path_list.append(h_today_dir +'\\'+ filename + '.png')
    display_image_path_list.append(resize_image_dir +'\\resized_'+ filename + '.jpg')
    if  TestApp().image_check() == '':       
        set_image_src(resize_image_dir +'\\resized_'+ filename + '.jpg')

    print(original_image_path_list)
    print(display_image_path_list)



def app_run(app, a):
    app.run()

if __name__ == '__main__':
    file_thread = threading.Thread(target=filechangelitener,daemon=True)
    file_thread.start()

    TestApp().run()
    



    


