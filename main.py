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
from kivy.uix.camera import Camera

r=None

def init_array(N,v):
  array=[]
  for i in range(N):
    array.append(v)
  return array

def get_direction_from_buttons(button_pos,button_neg):
  dir=button_pos != button_neg
  
  if dir:
    dir=button_pos*2-1

  return dir

class MainApp(App):
  def build(self):   
    Clock.schedule_once(self.move_robot_if_necessary,0)

    main_box=BoxLayout(orientation="vertical")
    main_box.add_widget(Camera(play=True))
    
    buttons_grid = GridLayout(cols=3)
    button_names=["forward","backward","left","right","up","down","pitch +","pitch -","roll +","roll -"]
    self.buttons_state=init_array(len(button_names),False)
    self.buttons=[]

    for i in range(len(button_names)):
      button=Button(text=button_names[i])
      buttons_grid.add_widget(button)
      self.buttons.append(button)

    main_box.add_widget(buttons_grid)

    return main_box

  def move_robot_if_necessary(self,dt):
    global r

    for i in range(len(self.buttons)):
      self.buttons_state[i]=self.buttons[i].state is not "normal"

    pose=[0,0,0,0,0]
    pose_buttons_indices=[[1,0],[3,2],[4,5],[6,7],[8,9]]

    for i in range(len(pose)):
      pose[i]=1*get_direction_from_buttons(self.buttons_state[pose_buttons_indices[i][0]],self.buttons_state[pose_buttons_indices[i][1]])
    if pose != [0,0,0,0,0]:
      r.jog(pose)

    Clock.schedule_once(self.move_robot_if_necessary,0.001)

def main():
  global r

  r=Robot()
  r.reset_and_home_joints()
  r.set_joint_speed(50)
  r.go_to_pose([400,0,150,180,0])
  MainApp().run()
  r.go_to_foetus_pos()
  r.disable_motors()

if __name__ == '__main__':
  main()
