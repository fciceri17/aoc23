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

for i, v in enumerate(data):
     for j, c in enumerate(v):
          if c=='#':
              continue
          if i==0 and c=='.':
              start=(i,j)
          if i==rows-1 and c=='.':
              end = (i,j)
          reachable = {}
          for _dir in directions:
               potential_r, potential_c = i+_dir[0], j+_dir[1]
               if potential_r>=rows or potential_r<0:
                   continue
               if potential_c>=cols or potential_c<0:
                   continue
               if data[potential_r][potential_c]!='#':
                    reachable[potential_r, potential_c]=1
          graph[(i,j)]=reachable

def prune_connected_twice(graph):
    for node, linked in graph.items():
        if len(linked)==2:
            linked_1, linked_2 = list(linked)
            graph[linked_1][linked_2]=graph[linked_1][node]+linked[linked_2]
            graph[linked_2][linked_1]=graph[linked_2][node]+linked[linked_1]
            del graph[node]
            del graph[linked_1][node]
            del graph[linked_2][node]
            return True
    return False

while prune_connected_twice(graph):
    continue

queue = [(start, {start}, 0)]
max_l = 0
while queue:
    node, visited, travel = queue.pop()
    visited = visited.union({node})
    if end in graph[node]:
        if travel+graph[node][end] > max_l:
            max_l = travel+graph[node][end]
            print(max_l)
    else:
        for goto, a_bit in graph[node].items():
            if goto not in visited:
                queue.append((goto, visited, travel+a_bit))

print(max_l)