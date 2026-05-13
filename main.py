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

r=None
joystick_axes_ids=[1,0,4]
joystick_buttons_ids=[13,14,15,16]
joystick_state=[0]*(len(joystick_axes_ids)+len(joystick_buttons_ids))

def get_direction_from_buttons(button_pos,button_neg):
  dir=button_pos != button_neg
  
  if dir:
    dir=button_pos*2-1

  return dir

class MainApp(App):
  def update_ui_buttons_state(self):
    for i in range(len(self.button_widgets)):
      self.buttons_state[i]=self.button_widgets[i].state != "normal"

  def move_robot_if_necessary(self,dt):
    global r
    global joystick_state

    self.update_ui_buttons_state()

    pose=[0,0,0,0,0]
    pose_buttons_indices=[[1,0],[3,2],[4,5],[6,7],[8,9]]

    pose_signs=[-1,1,1,-1,1]

    if joystick_state != [0]*(len(joystick_axes_ids)+len(joystick_buttons_ids)):
      #print(joystick_state)
      for i in range(len(joystick_axes_ids)):
        pose[i]=1*pose_signs[i]*joystick_state[i]
      for i in range(len(pose)-len(joystick_axes_ids)):
        pose_index=len(joystick_axes_ids)+i
        joystick_state_first_index=len(joystick_axes_ids)+2*(pose_index-len(joystick_axes_ids))
        pose[pose_index]=pose_signs[pose_index]*(joystick_state[joystick_state_first_index]-joystick_state[joystick_state_first_index+1])

    else:
      for i in range(len(pose)):
        pose[i]=1*get_direction_from_buttons(self.buttons_state[pose_buttons_indices[i][0]],self.buttons_state[pose_buttons_indices[i][1]])

    if pose != [0,0,0,0,0]:
      r.jog(pose)

    Clock.schedule_once(self.move_robot_if_necessary,0.001)

  def ui(self):
    main_box=BoxLayout(orientation="vertical")
    main_box.add_widget(Camera(play=True))
    
    button_names=["forward","backward","left","right","up","down","pitch +","pitch -","roll +","roll -"]    
    self.button_widgets=[]
    for i in range(len(button_names)):
      self.button_widgets.append(Button(text=button_names[i]))
    buttons_grid_layout=[[None,0,None,None,4,None,None,6,None],[2,None,3,None,None,None,8,None,9],[None,1,None,None,5,None,None,7,None]]
    buttons_grid_widget = GridLayout(cols=len(buttons_grid_layout[0]))
    self.buttons_state=[False]*len(button_names)

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
        
    main_box.add_widget(buttons_grid_widget)

    return main_box

  def build(self):   
    Clock.schedule_once(self.move_robot_if_necessary,0)
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

  r=Robot()
  r.reset()
  r.calibrate()
  r.set_joint_speed(50)
  r.go_to_pose([400,0,150,180,0])
  MainApp().run()

  r.go_to_foetus_pos()
  r.disable_motors()

if __name__ == '__main__':
  main()
