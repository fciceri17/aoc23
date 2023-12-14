import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
with open('input/day14.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....'''.splitlines()


cols = len(data[0])
rows = len(data)
roll_sum = 0
for j in range(cols):
     curr_stack = 0
     curr_head = 0
     for i in range(rows+1):
          if i==rows or data[i][j]=='#':
               roll_sum += sum(rows-curr_head-j for j in range(curr_stack))
               curr_head = i+1
               curr_stack = 0
          elif data[i][j]=='O':
               curr_stack+=1

print(roll_sum)