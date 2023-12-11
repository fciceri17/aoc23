import copy
import json
import math
import re
from collections import defaultdict

with open('input/day11.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''...#......
# .......#..
# #.........
# ..........
# ......#...
# .#........
# .........#
# ..........
# .......#..
# #...#.....'''.splitlines()

row_g = set()
col_g = set()
gs = []

for i, row in enumerate(data):
     for j, col in enumerate(row):
          if col=='#':
               gs.append((i,j))
               row_g.add(i)
               col_g.add(j)

empty_rows = [i for i, _ in enumerate(data) if i not in row_g]
empty_cols = [j for j, _ in enumerate(data[0]) if j not in col_g]
print(empty_rows, empty_cols)

roll = 0
roll2 = 0
factor = 1000000
for i, galaxy in enumerate(gs):
     for j in range(i+1, len(gs)):
          other_galaxy = gs[j]
          base_distance = abs(galaxy[0]-other_galaxy[0]) + abs(galaxy[1]-other_galaxy[1])
          row_add = sum(1 if k in empty_rows else 0 for k in range(*sorted([galaxy[0], other_galaxy[0]])))
          col_add = sum(1 if k in empty_cols else 0 for k in range(*sorted([galaxy[1], other_galaxy[1]])))
          roll+=base_distance+row_add+col_add
          roll2+=base_distance+row_add*(factor-1)+col_add*(factor-1)
print(roll)
print(roll2)
