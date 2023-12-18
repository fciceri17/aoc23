import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
with open('input/day18.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)'''.splitlines()


r_dict = defaultdict(set)

r = 0
c = 0

for entry in data:
     direction, cubes, color = entry.split()
     move = int(cubes)
     if direction=='R':
          for c_v in range(0, move+1):
               r_dict[r].add(c+c_v)
          c += move
     elif direction == 'L':
          for c_v in range(0, move + 1):
               r_dict[r].add(c-c_v)
          c -= move
     elif direction == 'U':
          for r_v in range(0, move+1):
               r_dict[r-r_v].add(c)
          r -= move
     else:
          for r_v in range(0, move+1):
               r_dict[r+r_v].add(c)
          r += move

dug = len([_ for x in r_dict.values() for _ in x])
# find a starting point? assume first block in corner has to be filled
start_r = min(r_dict)+1
start_c = min(r_dict[start_r])+1
assert start_c not in r_dict[start_r]

# flood fill
queue = [(start_r, start_c)]


directions = [(0,1), (0,-1), (1,0), (-1,0)]

visited = set()
filled = set()
while queue:
     pixel = queue.pop()
     if pixel in visited:
          continue
     visited.add(pixel)
     r,c = pixel
     # hit a wall
     if c in r_dict[r]:
          continue
     # fill it in
     filled.add(pixel)
     # explore neighbors
     for d_r, d_c in directions:
          queue.append((r+d_r, c+d_c))
print(len(filled)+dug)
