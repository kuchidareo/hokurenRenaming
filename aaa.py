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

import os,sys
import csv
import numpy

resource_add_path("IPAexfont00301")
LabelBase.register(DEFAULT_FONT, "ipaexg.ttf")

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
    carcass_list = []

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.body_number = '枝肉番号:'
        self.carcass_order = '出場順:'
        self.barcode = ''
        self.filepath = ''
    

    def okClicked(self):        # ボタンをクリック時
        print("hello world")

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
    

    '''def sansyoClicked(self):
        print("sansyo")
        fTyp = [("","*.csv")]
        iDir = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"
        load_filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        print(load_filepath)
        self.filepath = load_filepath

        load_carcass_list = numpy.loadtxt(fname=load_filepath,skiprows=0,delimiter=",",dtype="U20")[:,0:2]
        for line in load_carcass_list:
            carcass_list.append([line[0],line[1]])
        print(carcass_list)
        self.ids.barcode_input.focus = True'''
    
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
        return TextWidget()

if __name__ == '__main__':
    TestApp().run()

