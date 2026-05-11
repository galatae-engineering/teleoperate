import sys
sys.path.append('../galatae-api/')
from robot import Robot
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.clock import Clock
from threading import Thread
import time
from robot_control import *

buttons_state=[False,False,False,False,False,False,False,False,False,False]
window_is_open=True

class DirButton(Button):
  def change_buttons_state(self,is_button_pressed):
    global buttons_state
    index=["forward","backward","left","right","up","down","pitch +","pitch -","roll +","roll -"].index(self.text)
    buttons_state[index]=is_button_pressed
    print(is_button_pressed)

  def on_press(self):
    self.change_buttons_state(True)
    
  def on_release(self):
    self.change_buttons_state(False)

class FourButtons(GridLayout):
  names = ListProperty(["","","",""])
  for name in names:
    Label()
    DirButton(Button)
  pass

class TwoButtons(GridLayout):
  names = ListProperty(["",""])
  pass

class Window(GridLayout):
  pass

class MainApp(App):
  def build(self):
    return Window()

def main():
  global window_is_open

  thread=Thread(target=control_robot)
  thread.start()
  MainApp().run()
  window_is_open=False

if __name__ == "__main__":
  main()
