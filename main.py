from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard

---- YOUR LOGIC ----

digits = (
["1","2","3","4","5","6","7","8","9","0"] +
[chr(ord('a')+i) for i in range(26)] +
[" "] +
[chr(ord('A')+i) for i in range(26)]
)

rev = {c:i+1 for i,c in enumerate(digits)}

def CODE(text):
return "".join(
"." if b == "1" else "_"
for n in [rev[c] for c in text]
for b in format(n, "06b")
)

def DECODE(pattern):
bits = pattern.replace(".", "1").replace("_", "0")
arr = [int(bits[i:i+6], 2) for i in range(0, len(bits), 6)]
return "".join(digits[n-1] for n in arr)

---- GUI ----

class MainApp(App):
def build(self):
layout = BoxLayout(
orientation='vertical',
spacing=10,
padding=10
)

self.input_text = TextInput(  
        hint_text="Enter text or pattern",  
        multiline=True,  
        size_hint_y=0.2  
    )  

    self.output_text = TextInput(  
        text="Output will appear here",  
        readonly=True,  
        multiline=True,  
        size_hint_y=0.6  
    )  

    btn_convert = Button(  
        text="Convert",  
        size_hint_y=0.1  
    )  
    btn_convert.bind(on_press=self.convert)  

    # Copy and Paste buttons side by side  
    button_row = BoxLayout(  
        orientation='horizontal',  
        size_hint_y=0.1,  
        spacing=10  
    )  

    btn_copy = Button(text="Copy")  
    btn_paste = Button(text="Paste")  

    btn_copy.bind(on_press=self.copy_output)  
    btn_paste.bind(on_press=self.paste_input)  

    button_row.add_widget(btn_copy)  
    button_row.add_widget(btn_paste)  

    layout.add_widget(self.input_text)  
    layout.add_widget(btn_convert)  
    layout.add_widget(button_row)  
    layout.add_widget(self.output_text)  

    return layout  

def convert(self, instance):  
    try:  
        text = self.input_text.text.strip()  

        if text and all(c in "._" for c in text):  
            self.output_text.text = DECODE(text)  
        else:  
            self.output_text.text = CODE(text)  

    except Exception as e:  
        self.output_text.text = str(e)  

def copy_output(self, instance):  
    Clipboard.copy(self.output_text.text)  

def paste_input(self, instance):  
    self.input_text.text = Clipboard.paste()

MainApp().run()
