import math
import re
from collections import defaultdict

with open('input/day8.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''RL
#
# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)'''.splitlines()

instr = data[0]

nodes = [x.split(' = ') for x in data[2:]]

paths = {x[0]:x[1][1:-1].split(', ') for x in nodes}

stat = 'AAA'
moves = 0
while stat!='ZZZ':
     for i in instr:
          moves += 1
          if i=='L':
               stat=paths[stat][0]
          else:
               stat=paths[stat][1]
print(moves)