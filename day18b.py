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

m_d = {
     '0': 'R',
     '1': 'D',
     '2': 'L',
     '3': 'U'
}
vertices = [(0,0)]
for entry in data:
     _ ,_ , color = entry.split()
     hex_dist = color[2:-2]
     move = int(hex_dist, 16)
     direction = m_d[color[-2]]

     if direction=='R':
          c += move
     elif direction == 'L':
          c -= move
     elif direction == 'U':
          r -= move
     else:
          r += move
     vertices.append((r,c))

def shoelace_area(vertices):
     fl = 0
     trench=0
     for i, (vx,vy) in enumerate(vertices[:-1]):
          vx2, vy2= vertices[i+1]
          fl+=vx*vy2-vy*vx2
          trench+=abs(vx2-vx)+abs(vy2-vy)
     return abs(fl)//2+trench//2+1

print(shoelace_area(vertices))