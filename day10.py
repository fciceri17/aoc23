import copy
import json
import math
import re
from collections import defaultdict

with open('input/day10.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''
# FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L'''.strip().splitlines()

d_map = {
     (-1,0): '|7F',
     (1,0): '|LJ',
     (0,1): '-7J',
     (0,-1): '-FL'
}

def next_dir(dir, segment):
     if segment=='F':
          return (0,1) if dir == (-1,0) else (1,0)
     if segment=='|':
          return (-1,0) if dir == (-1,0) else (1,0)
     if segment == 'L':
          return (-1, 0) if dir != (1, 0) else (0, 1)
     if segment == 'J':
          return (-1, 0) if dir != (1, 0) else (0, -1)
     if segment == '7':
          return (0, -1) if dir != (0, 1) else (1, 0)
     if segment == '-':
          return (0, 1) if dir == (0, 1) else (0, -1)


def connected(i, j, exclude = None):
     r = []
     segment=data[i][j]
     for direction, acc in d_map.items():
          if direction==exclude:
               continue
          if i+direction[0] < len(data) and i+direction[0] >= 0 and j+direction[1] >= 0 and j+direction[1] < len(data[0]):
               acc = set(acc)-{'|' if segment=='-' else '-' if segment=='|' else None}
               if data[i+direction[0]][j+direction[1]] in acc:
                    r.append(direction)
     return r


def find_start(data):
     for i,row in enumerate(data):
          for j,col in enumerate(row):
               if col=='S':
                    return i, j, connected(i,j)

def reverse_dir(dir):
     candidates = set('-|7JLF')
     if (0,1) in dir:
          candidates.discard('|')
          candidates.discard('J')
          candidates.discard('7')
     if (0,-1) in dir:
          candidates.discard('|')
          candidates.discard('L')
          candidates.discard('F')
     if (1, 0) in dir:
          candidates.discard('-')
          candidates.discard('L')
          candidates.discard('J')
     if (-1, 0) in dir:
          candidates.discard('-')
          candidates.discard('F')
          candidates.discard('7')
     assert len(candidates)==1
     return candidates.pop()

def loop_l(data):
     pos_i, pos_j, dir = find_start(data)
     data[pos_i] = ''.join([x if j!=pos_j else reverse_dir(dir) for j,x in enumerate(data[pos_i])])
     dir = dir[0]
     curr_pos = (pos_i+dir[0], pos_j+dir[1])
     path = {(pos_i, pos_j), curr_pos}
     while curr_pos!=(pos_i, pos_j):
          dir = next_dir(dir, data[curr_pos[0]][curr_pos[1]])
          curr_pos = (curr_pos[0] + dir[0], curr_pos[1] + dir[1])
          path.add(curr_pos)
     return path

path = loop_l(data)
d = len(path)
print(d/2)



def is_outside(pos_i, pos_j, path):
     counter=0
     evaluating = ''
     for i in range(pos_i):
          if (i, pos_j) in path:
               if data[i][pos_j] == '-':
                    counter+=1
               if data[i][pos_j] == '7':
                    assert not evaluating
                    evaluating = '7'
               if data[i][pos_j] == 'F':
                    assert not evaluating
                    evaluating = 'F'
               if data[i][pos_j] == 'J':
                    if evaluating == 'F':
                         counter+=1
                    evaluating = ''
               if data[i][pos_j] == 'L':
                    if evaluating == '7':
                         counter+=1
                    evaluating = ''

     return counter%2

def draw_path(data, path):
     out = [
          ''.join([
               '.' if (i,j) not in path else data[i][j]
               for j, row in enumerate(col)
          ])
          for i, col in enumerate(data)
     ]
     return '\n'.join(out)

roll = 0
for i, _ in enumerate(data):
     for j, _ in enumerate(data[0]):
          if (i,j) not in path:
               roll+=is_outside(i,j,path)

print(roll)
