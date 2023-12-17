import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
with open('input/day15.txt', 'r') as f:
     data=f.read().strip()

# data='''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''

instr = data.split(',')

def hash_it(s):
     curr_hash = 0
     for char in s:
          o = ord(char)
          curr_hash += o
          curr_hash *= 17
          curr_hash %= 256
     return curr_hash

hashes = []
boxes = [list() for _ in range(256)]
for i in instr:
     label = i.split('-')[0].split('=')[0]
     hashes.append(hash_it(i))
     box_hash = hash_it(label)
     if '-' in i:
          boxes[box_hash]=[x for x in boxes[box_hash] if x[0]!=label]
     else:
          ld = i.split('=')[-1]
          new_box = []
          found=False
          for x in boxes[box_hash]:
               if label!=x[0]:
                    new_box.append(x)
               else:
                    found=True
                    new_box.append((label, ld))
          if not found: new_box.append((label, ld))
          boxes[box_hash]=new_box

def score_box(box_num, box):
     roll=0
     for i,lens in enumerate(box):
          v = box_num+1
          v *= i+1
          v *= int(lens[1])
          roll+=v
     return roll
print(sum(hashes))
print(sum(score_box(*v) for v in enumerate(boxes)))
