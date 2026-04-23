import sys
sys.path.append('../galatae-api/')

import numpy as np
import cv2 as cv
from threading import Thread
from robot import Robot
import keyboard
import math
import time
import traceback
import curses

screen = curses.initscr()
keyboard_state=[0,0,0,0,0]

def show_video():
  cap = cv.VideoCapture(0)
  if not cap.isOpened():
      print("Cannot open camera")
      exit()
  while True:
      ret, frame = cap.read()
  
      if not ret:
          print("Can't receive frame (stream end?). Exiting ...")
          break
      gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
      cv.imshow('frame', gray)
      if cv.waitKey(1) == ord('q'):
          break

  cap.release()
  cv.destroyAllWindows()

def update_keys_state():
  keyboard_numbers=[260,261,259,258,27]
  while(True):
    char = screen.getch()
    if char in keyboard_numbers:
        keyboard_state[keyboard_numbers.index(char)]=1

def get_direction_from_keys(key_pos,key_neg):
  dir=0
  if(key_pos and not key_neg):
    dir=1
  elif(key_neg and not key_pos):
    dir=-1
  return dir

def main():
  #video_thread=Thread(target=show_video)
  #video_thread.start()
  
  curses.noecho()
  curses.cbreak()
  screen.keypad(True)

  keys_thread=Thread(target=update_keys_state)
  default_speed=50
  #
  pose_key_indices=[[3,2],[1,0]]

  keys_thread.start()
  
  r=Robot(False)
  r.reset_and_home_joints()
  r.set_joint_speed(default_speed)
  r.go_to_pose([400,0,150,180,0])
  r.set_joint_speed(20)

  current_state=keyboard_state.copy()

  try:
    while(not current_state[4]):
      pose=[0,0,0,0,0]
      for i in range(2):
        pose[i]=10*get_direction_from_keys(current_state[pose_key_indices[i][0]],current_state[pose_key_indices[i][1]])
      
      if pose != [0,0,0,0,0]:
        #print(pose)
        r.jog(pose)
        for i in range(len(keyboard_state)):
          keyboard_state[i]=0

      current_state=keyboard_state.copy()
  except:
    print(traceback.format_exc())


  r.set_joint_speed(default_speed)
  r.go_to_foetus_pos()
  r.disable_motors()

if __name__ == "__main__":
  main()
  #test()