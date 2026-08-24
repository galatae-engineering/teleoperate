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
from kivy.core.window import Window
import RPi.GPIO as GPIO
from shuffle_sheets import *

r=None

joystick_axes_ids=[1,0,4]
joystick_buttons_ids=[13,14,15,16,0,2]
joystick_state=[0]*(len(joystick_axes_ids)+len(joystick_buttons_ids))
pump_pin=5

def start_pump(instance):
  GPIO.output(pump_pin,GPIO.HIGH)

def stop_pump(instance):
  GPIO.output(pump_pin,GPIO.LOW)
  
def set_limits(value,limits):
  if limits != None:
    if len(limits)==1:
      limits=[-limits[0],limits[0]]
    value=min(max(limits[0],value),limits[1])

  return value

def get_pose_from_joystick_state():
  pose_length=5
  pose=[0]*pose_length
  pose_signs=[-1,1,1,-1,1]

  for i in range(len(joystick_axes_ids)):
    pose[i]=1*pose_signs[i]*joystick_state[i]

  for i in range(pose_length-len(joystick_axes_ids)):
    pose_index=len(joystick_axes_ids)+i
    joystick_state_first_index=len(joystick_axes_ids)+2*(pose_index-len(joystick_axes_ids))
    pose[pose_index]=pose_signs[pose_index]*(joystick_state[joystick_state_first_index]-joystick_state[joystick_state_first_index+1])

  return pose

def shuffle_sheets(instance):
  default_speed=50

  all_stacks_xy_rolls=get_all_stacks_xy_roll()
  print(all_stacks_xy_rolls)

  sensor_pin=6
  GPIO.setup(sensor_pin,GPIO.IN)

  print(datetime.now())

  make_notebooks(all_stacks_xy_rolls,pump_pin,r,default_speed,sensor_pin)

  GPIO.output(pump_pin,GPIO.LOW)
  r.set_joint_speed(default_speed)
  r.go_to_foetus_pos()
  r.disable_motors()

class MainApp(App):
  def get_ui_buttons_state(self):
    buttons_state=[False]*len(self.button_widgets)

    for i in range(len(self.button_widgets)):
      buttons_state[i]=self.button_widgets[i].state != "normal"
    return buttons_state
  
  def get_pose_from_buttons(self):
    pose_buttons_indices=[[1,0],[3,2],[4,5],[6,7],[8,9]]
    pose=[0]*5
    buttons_state=self.get_ui_buttons_state()
    for i in range(len(pose)):
      pose[i]=1*(buttons_state[pose_buttons_indices[i][0]]-buttons_state[pose_buttons_indices[i][1]])

    return pose

  def move_robot_if_necessary(self,dt):
    global r
    global joystick_state    
    pose_limits=[None,None,None,None,[10]]

    if joystick_state != [0]*(len(joystick_axes_ids)+len(joystick_buttons_ids)):
      pose=get_pose_from_joystick_state()
    else:
      pose=self.get_pose_from_buttons()

    if pose != [0,0,0,0,0]:
      r.jog(pose)

    if joystick_state[len(joystick_axes_ids)+len(joystick_buttons_ids)-1] == True:
      GPIO.output(pump_pin,GPIO.LOW)
    elif joystick_state[len(joystick_axes_ids)+len(joystick_buttons_ids)-2] == True:
      GPIO.output(pump_pin,GPIO.HIGH)

    Clock.schedule_once(self.move_robot_if_necessary,0)
    
  def ui(self):
    root=BoxLayout(orientation="vertical")
    try:
      root.add_widget(Camera(play=True))
    except:
      root.add_widget(Label(text="Camera not detected."))
    
    button_names=["forward","backward","left","right","up","down","pitch +","pitch -","roll +","roll -","start pump","stop pump","shuffle"]    
    self.button_widgets=[]
    for i in range(len(button_names)):
      self.button_widgets.append(Button(text=button_names[i]))
    
    self.button_widgets[10].bind(on_press=start_pump)
    self.button_widgets[11].bind(on_press=stop_pump)
    self.button_widgets[12].bind(on_press=shuffle_sheets)
    
    buttons_grid_layout=[[None,0,None,None,4,None,None,7,None,None,10],[2,None,3,None,None,None,8,None,9,None,None],[None,1,None,None,5,None,None,6,None,None,11]]
    buttons_grid_widget = GridLayout(cols=len(buttons_grid_layout[0]))

    for i in range(len(buttons_grid_layout)):
      for j in range(len(buttons_grid_layout[0])):
        button_index=buttons_grid_layout[i][j]
        if(button_index != None):
          widget=self.button_widgets[button_index]
          pass
        else:
          widget=Label()
          pass 
        buttons_grid_widget.add_widget(widget)
        
    root.add_widget(buttons_grid_widget)

    return root

  def prepare_robot(self,dt):
    r.calibrate()
    r.go_to_pose([400,0,150,180,0])
    Clock.schedule_once(self.move_robot_if_necessary,0)

  def build(self):
    Clock.schedule_once(self.prepare_robot,5)
    return self.ui()

def find_index(list,value):
  try:
    index=list.index(value)
  except:
    index=None
  return index

def joystick_axe_moved(win, stickid, axisid,value):
    value=round(value/32767.0,3)
    index=find_index(joystick_axes_ids,axisid)

    if index != None:
      if 0.5 < abs(value):
        if index==0 or index==2:
          joystick_state[index]=-value
        else:
          joystick_state[index]=value
      else:
        joystick_state[index]=0

def joystick_button_change(id,value):
  index=find_index(joystick_buttons_ids,id)
  if index != None:
    joystick_state[len(joystick_axes_ids)+index]=value

def joystick_button_down(win,stickid,button_id):
  joystick_button_change(button_id,1)

def joystick_button_up(win,stickid,button_id):
  joystick_button_change(button_id,0)  

def main():
  global r
  Window.bind(on_joy_axis=joystick_axe_moved)
  Window.bind(on_joy_button_down=joystick_button_down)
  Window.bind(on_joy_button_up=joystick_button_up)

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pump_pin,GPIO.OUT)
  GPIO.output(pump_pin,GPIO.LOW)

  r=Robot()
  r.reset()
  r.set_joint_speed(50)

  MainApp().run()

  r.go_to_foetus_pos()
  r.disable_motors()

if __name__ == '__main__':
  main()
