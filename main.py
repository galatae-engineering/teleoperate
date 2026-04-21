import sys
sys.path.append('../galatae-api/')

import numpy as np
import cv2 as cv
from threading import Thread
from robot import Robot
import keyboard
import math

r=Robot(False)

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

def print_serial_messages():
  while(True):
    print(r._wait_for_message())

def main():
  """
  thread1=Thread(target=print_serial_messages)
  thread1.start()
  thread2=Thread(target=show_video)
  thread2.start()
  """
  while(True):
    key=keyboard.read_key()
    dir_number=["down","up","right","left"].index(key)
    pose=[0,0,0,0,0]
    pose[math.floor(dir_number/2)]=[1,-1][dir_number%2]*10
    print(pose)
    r.jog(pose)

  #r.go_to_foetus_pos()
  #r.disable_motors()

if __name__ == "__main__":
  main()