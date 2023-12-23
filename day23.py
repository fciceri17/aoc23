import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
from queue import PriorityQueue

with open('input/day23.txt', 'r') as f:
     data=f.read().strip().splitlines()


# data = '''#.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#'''.splitlines()

graph = {}
rows = len(data)
cols = len(data[0])
directions = [(0,1), (0,-1), (1,0), (-1,0)]

def get_connected(i, j, symbol):
    if symbol == '>':
        return i, j+1
    if symbol == '<':
        return i, j-1
    if symbol == '^':
        return i-1, j
    return i+1, j

for i, v in enumerate(data):
     for j, c in enumerate(v):
          if i==0 and c=='.':
              start=(i,j)
          if i==rows-1 and c=='.':
              end = (i,j)
          reachable = {}
          if c in '^><v':
              reachable = {get_connected(i, j, c): 1}
          else:
              for _dir in directions:
                   potential_r, potential_c = i+_dir[0], j+_dir[1]
                   if potential_r>=rows or potential_r<0:
                       continue
                   if potential_c>=cols or potential_c<0:
                       continue
                   if data[potential_r][potential_c]!='#':
                        reachable[(potential_r, potential_c)]=1
          graph[(i,j)]=reachable

queue = [(start, {start})]
max_l = 0
while queue:
    node, visited = queue.pop()
    visited = visited.union({node})
    for goto in graph[node]:
        if goto == end:
            max_l = max(len(visited), max_l)
        elif goto not in visited:
            queue.append((goto, visited))

print(max_l)