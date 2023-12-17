import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
with open('input/day16.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''.|...\....
# |.-.\.....
# .....|-...
# ........|.
# ..........
# .........\\
# ..../.\\\\..
# .-.-/..|..
# .|....-|.\\
# ..//.|....'''.splitlines()

rows = len(data)
cols = len(data[0])

def get_en(starting_point):
     queue = set()
     visited = defaultdict(set)

     queue.add(starting_point)

     while queue:
          visit = queue.pop()
          r,c,dr,dc = visit
          if r>=rows or r<0 or c>=cols or c<0:
               continue
          if (dr,dc) in visited[(r,c)]:
               continue
          visited[(r,c)].add((dr,dc))
          if data[r][c]== '.' or (data[r][c] == '|' and abs(dr) == 1) or (data[r][c] == '-' and abs(dc) == 1):
               queue.add((r+dr, c+dc, dr, dc))
          elif data[r][c]== '-':
               queue.add((r, c-1, 0, -1))
               queue.add((r, c+1, 0, 1))
          elif data[r][c] == '|':
               queue.add((r-1, c, -1, 0))
               queue.add((r+1, c, 1, 0))
          elif data[r][c] == '/':
               if dr==-1:
                    queue.add((r, c+1, 0, 1))
               elif dr==1:
                    queue.add((r, c-1, 0, -1))
               elif dc==1:
                    queue.add((r-1, c, -1, 0))
               elif dc==-1:
                    queue.add((r+1, c, 1, 0))
          elif data[r][c] == '\\':
               if dr==-1:
                    queue.add((r, c-1, 0, -1))
               elif dr==1:
                    queue.add((r, c+1, 0, 1))
               elif dc==1:
                    queue.add((r+1, c, 1, 0))
               elif dc==-1:
                    queue.add((r-1, c, -1, 0))

     return len(visited)

print(get_en((0,0,0,1)))
print(max(get_en((x,y,dx,dy)) for x in range(rows) for y in range(cols) for dx,dy in [(-1,0), (1,0), (0,1), (0,-1)]))