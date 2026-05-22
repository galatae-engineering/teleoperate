import sys
sys.path.append('../galatae-api/')

import numpy as np
from threading import Thread
#import keyboard
import math
import time
from datetime import datetime
import random
from pick_and_place import *

def get_roll(x,y):
  return math.atan(float(y)/x)*180*1.03/math.pi

def get_all_stacks_xy_roll():
  x_start=220
  delta_x=220
  delta_y=160
  stacks_per_line=5

  xy_roll=[]
  for i in range(2):
    for j in range(stacks_per_line):
      x=(x_start+i*delta_x)*1.02
      y=4+(((1-stacks_per_line)/2+j)*delta_y)*1.03
      xy_roll+=[[x,y,get_roll(x,y)]]

  return xy_roll

def delete_elements_from_list(indices,list_original):
  new_list=list_original.copy()
  sorted_indices=sorted(indices, reverse=True)
  for i in sorted_indices:
    del new_list[i]
  return new_list

def test_positions(r,all_stacks_xy_rolls):
  safe_height=45
  i=0
  for i in [0,1,2,3,4,5,6,7,8,9]:
    go_at_defined_speed(r,50,all_stacks_xy_rolls[i][:2],safe_height,all_stacks_xy_rolls[i][2])
    probe_at_defined_speed(r,10,all_stacks_xy_rolls[i][:2],all_stacks_xy_rolls[i][2])
    input()
    go_at_defined_speed(r,50,all_stacks_xy_rolls[i][:2],safe_height,all_stacks_xy_rolls[i][2])

def make_notebooks(all_stacks_xy_rolls,pump_pin,r,default_speed,sensor_pin):
  pages_per_book=50
  place_stack_index=2
  separator_stack_index=9
  place_xy_roll=all_stacks_xy_rolls[place_stack_index]
  pick_xy_rolls=delete_elements_from_list([place_stack_index,separator_stack_index],all_stacks_xy_rolls)

  go_on=True
  while go_on:
    t=time.time()
    page=0
    while(page<pages_per_book and go_on):
      random_index=random.randrange(0,len(pick_xy_rolls))
      go_on=pick_and_place_sheet(r,default_speed,pick_xy_rolls[random_index],pump_pin,sensor_pin,place_xy_roll)
      page+=1
    if(go_on):
      go_on=pick_and_place_sheet(r,default_speed,all_stacks_xy_rolls[separator_stack_index],pump_pin,sensor_pin,place_xy_roll)
    print("t:",(time.time()-t)/(pages_per_book+1))