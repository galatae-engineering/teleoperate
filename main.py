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
  pass

class TwoButtons(GridLayout):
  names = ListProperty(["",""])
  pass

class Teleoperate(GridLayout):
  pass

def get_direction_from_buttons(button_pos,button_neg):
  dir=button_pos != button_neg
  
  if dir:
    dir=button_pos*2-1

  return dir

def move_robot_if_necessary(r):
  pose=[0,0,0,0,0]
  pose_buttons_indices=[[1,0],[3,2],[4,5],[6,7],[8,9]]

  for i in range(len(pose)):
    pose[i]=1*get_direction_from_buttons(buttons_state[pose_buttons_indices[i][0]],buttons_state[pose_buttons_indices[i][1]])
  if pose != [0,0,0,0,0]:
    r.jog(pose)

def control_robot():
  global window_is_open
  r=Robot()
  r.reset_and_home_joints()
  r.set_joint_speed(50)
  r.go_to_pose([400,0,150,180,0])

  while(window_is_open):
    move_robot_if_necessary(r)
    time.sleep(0.001)
  
  r.go_to_foetus_pos()
  r.disable_motors()

class MainApp(App):
  def build(self):
    return Teleoperate()

def main():
  global window_is_open

  thread=Thread(target=control_robot)
  thread.start()
  MainApp().run()
  window_is_open=False

if __name__ == "__main__":
  main()
