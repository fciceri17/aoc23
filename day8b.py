import math
import re
from collections import defaultdict

with open('input/day8.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''LR
#
# 11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)'''.splitlines()

instr = [0 if x=='L' else 1 for x in data[0]]

nodes = [x.split(' = ') for x in data[2:]]

paths = {x[0]:x[1][1:-1].split(', ') for x in nodes}

stat = [x[0] for x in nodes if x[0][-1]=='A']

def find_moves(instr, stat):
     min_cycles = [math.inf for _ in range(len(stat))]
     moves=0
     while True:
          for i in instr:
               moves += 1
               stat = [paths[s][i] for s in stat]
               for p, node in enumerate(stat):
                    if node[-1]=='Z':
                         min_cycles[p]=min(min_cycles[p], moves)
               if all(x!=math.inf for x in min_cycles):
                    return min_cycles

min_c = find_moves(instr, stat)
print(math.lcm(*min_c))