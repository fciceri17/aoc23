import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
from queue import PriorityQueue

with open('input/day21.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........'''.splitlines()


graph = {}
rows = len(data)
cols = len(data[0])
directions = [(0,1), (0,-1), (1,0), (-1,0)]

for i, v in enumerate(data):
     for j, c in enumerate(v):
          if c=='S':
              start=(i,j)
          reachable = {}
          for _dir in directions:
               potential_r, potential_c = i+_dir[0], j+_dir[1]
               actual_r, actual_c = potential_r, potential_c
               if potential_r>=rows or potential_r<0:
                   potential_r=(rows+potential_r)%rows
               if potential_c>=cols or potential_c<0:
                   potential_c = (cols + potential_c) % cols
               if data[potential_r][potential_c]!='#':
                    reachable[(actual_r, actual_c)]=1
          graph[(i,j)]=reachable


positions = [start]
def step(positions):
    new_positions = set()
    for node in positions:
        node_for_search = (node[0]+rows)%rows, (node[1]+cols)%cols
        for connected in graph[node_for_search]:
            if node!=node_for_search:
                offset = node[0]-node_for_search[0], node[1]-node_for_search[1]
                connected = connected[0]+offset[0], connected[1]+offset[1]
            new_positions.add(connected)
    return new_positions

cycles = 26501365
remainder = cycles%rows
states = {}
for stepping in range(1,max(50,rows*2+remainder)+1):
    positions=step(positions)
    states[stepping]=len(positions)
points = [states[remainder], states[remainder+rows], states[remainder+rows*2]]
c = points[0]
a = (points[2] + c)/2 - points[1]
b = points[1] - c - a
print(states[64])
print((lambda x: c + a*x**2 + b*x)(cycles//rows))