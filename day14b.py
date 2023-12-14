import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
with open('input/day14.txt', 'r') as f:
     data=f.read().strip()

# data='''O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....'''

original_grid = data.splitlines()
cols = len(original_grid[0])
rows = len(original_grid)
roll_sum = 0
state = {}

@cache
def tilt_state(curr_state, direction):
     grid = curr_state.splitlines()
     new_state = []
     tilt, perp, up_or_down = {
          (0,1):  (rows, cols, -1),
          (0,-1): (rows, cols, 1),
          (-1,0): (cols, rows, 1),
          (1,0):  (cols, rows, -1)
     }[direction]
     for j in range(tilt):
          curr_stack = 0
          curr_head = 0 if up_or_down == 1 else perp -1
          end=False
          for i in range(0, perp+1):
               if i==perp:
                    end = True
               if up_or_down<0:
                    i=perp-i-1
               r, c = (i, j) if direction[1]==0 else (j, i)
               if end or grid[r][c]=='#':
                    if curr_stack>0:
                         new_state.append((j, curr_head, curr_stack))
                    curr_head = i+up_or_down
                    curr_stack = 0
               elif grid[r][c]=='O':
                    curr_stack+=1
     return state_to_string(new_state, direction)

def state_to_string(state, direction):
     out_data = list(x if x in '#' else '.' for x in data if x!='\n')

     for idx_1, idx_2, stack in state:
          s_i, s_j, up_or_down = {
               (0, 1): (idx_1, idx_2, -1),
               (0, -1): (idx_1, idx_2, 1),
               (-1, 0): (idx_2, idx_1, 1),
               (1, 0): (idx_2, idx_1, -1)
          }[direction]
          for s in range(stack):
               if direction == (-1,0):
                    i=s_i + s
                    j=s_j
               elif direction == (0, -1):
                    i = s_i
                    j = s_j + s
               elif direction == (1, 0):
                    i = s_i - s
                    j = s_j
               else:
                    i = s_i
                    j = s_j - s
               out_data[i * cols + j] = 'O'
     return '\n'.join(''.join(out_data[n:n+cols]) for n in range(0,len(out_data),cols))

def n_beam_weight(state):
     grid=state.splitlines()
     roll_sum = 0
     for j in range(cols):
          for i in range(rows):
               if grid[i][j] == 'O':
                    roll_sum += rows - i
     return roll_sum


dir_rotation = [(-1,0), (0,-1), (1, 0), (0, 1)]

grid = data
iterations = 1000000000
state_previous = {}
for it in range(iterations):
     for direction in dir_rotation:
          grid = tilt_state(grid, direction)
     state_previous[grid]=it
     if it>5000: #enough cycles?
          cycle_length = len([x for x,y in state_previous.items() if y >500])
          end_state = [x for x,y in state_previous.items() if (iterations-y-1)%cycle_length==0 and y>500]
          assert len(end_state)==1
          print(n_beam_weight(end_state[0]))
          break
