import sys
sys.path.append('../galatae-api/')

import numpy as np
import cv2 as cv
from threading import Thread
from robot import Robot

r=Robot(False)


def show_video():
  cap = cv.VideoCapture(0)
  if not cap.isOpened():
      print("Cannot open camera")
      exit()
  while True:
      # Capture frame-by-frame
      ret, frame = cap.read()
  
      # if frame is read correctly ret is True
      if not ret:
          print("Can't receive frame (stream end?). Exiting ...")
          break
      # Our operations on the frame come here
      gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
      # Display the resulting frame
      cv.imshow('frame', gray)
      if cv.waitKey(1) == ord('q'):
          break
  
  # When everything done, release the capture
  cap.release()
  cv.destroyAllWindows()

def print_serial_messages():
  while(True):
    print(r._wait_for_message())

def main():
  thread1=Thread(target=print_serial_messages)
  thread1.start()
  thread2=Thread(target=show_video)
  thread2.start()
  
  try:
    while(True):
      message=input()
      r.send_message(message)
  except:
    print(traceback.format_exc())
    
  r.go_to_foetus_pos()
  r.disable_motors()


if __name__ == "__main__":
  main()