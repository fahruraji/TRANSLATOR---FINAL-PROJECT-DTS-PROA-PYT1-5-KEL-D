from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.core.text import LabelBase

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton

from googletrans import Translator
import arabic_reshaper
import bidi.algorithm

Window.size = (350, 600)

class MainApp(MDApp):
    global screen_manager
    screen_manager = ScreenManager()
    
    selected_language = StringProperty('Bahasa Indonesia')
    result_text = StringProperty('')
    languages = {
            'Bahasa Arab': 'ar',
            'Bahasa China Sdr': 'zh-CN',
            'Bahasa China Trd': 'zh-TW',
            'Bahasa India': 'hi',
            'Bahasa Indonesia': 'id',
            'Bahasa Inggris': 'en',
            'Bahasa Italia': 'it',
            'Bahasa Jawa': 'jw',
            'Bahasa Jepang': 'ja',
            'Bahasa Jerman': 'de',
            'Bahasa Korea': 'ko',
            'Bahasa Latin': 'la',
            'Bahasa Prancis': 'fr',
            'Bahasa Rusia': 'ru',
            'Bahasa Spanyol': 'es',
            'Bahasa Sunda': 'su',
            'Bahasa Thailand': 'th',
        }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("mainScreen.kv")
        menu_items = [
            {
                "text": f"{lang}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{lang}": self.set_item(x),
            } for lang in self.languages.keys()
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )

    def set_item(self, text_item):
        self.selected_language = text_item
        self.menu.dismiss()
        
    
    def build(self):
        self.title="PENTERJEMAH MULTIBAHASA"
        self.theme_cls.primary_palette = "Blue"
        
        screen_manager.add_widget(Builder.load_file("splashScreen.kv"))
        screen_manager.add_widget(Builder.load_file("mainScreen.kv"))
        
        return screen_manager
    
    def on_start(self):
        Clock.schedule_once(self.change_screen, 5)
        
    def change_screen(self, *args):
        screen_manager.current = "MainScreen"
        
    def trans(self, input, dst):
        try:
            translation = Translator()
            
            assert len(input) != 0
            
            result = translation.translate(input, dest=dst).text
        
            if (dst == 'ar'):
                result = arabic_reshaper.reshape(result)
                result = bidi.algorithm.get_display(result)
                
            self.result_text = result
            
        except AssertionError:
            title = 'Kotak input masih kosong!'
            err_msg = "Masukkan dulu teks yang ingin diterjemahkan..."
            self.show_dialog(title, err_msg)
            
    def about(self):
        title = 'Tentang Aplikasi'
        text = """
Aplikasi ini adalah Final Project dari Kelompok D Kelas PYT1-5 pada Program Digital Talent Scholarship untuk kelas Python Professional Academy tahun 2022 yang diselenggarakan oleh Kementerian Komunikasi dan Informatika Republik Indonesia.

Dibuat menggunakan bahasa pemrograman PYTHON, dengan antar muka menggunakan Framework KIVY, dan library GOOGLETRANS sebagai penghubung dengan Google Translate API untuk proses penterjemahan bahasa.
"""
        self.show_dialog(title, text)
        
    def show_dialog(self, title, msg):
        self.dialog = MDDialog(title=title,
                               text=msg, size_hint=(0.8, 1),
                               buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)])
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        # do stuff after closing the dialog
        
LabelBase.register(name='Arial',fn_regular='assets/fonts/ArialUnicodeMS.ttf')


if __name__=="__main__":
    MainApp().run()