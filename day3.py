import math
import re
from collections import defaultdict

with open('input/day3.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..'''.splitlines()

parts = {}
def search_nearby(i, j):
     found = defaultdict(set)
     for i_near in range(max(i-1, 0), min(i+2, len(data))):
          for j_near in range(max(j-1, 0), min(j+2, len(data[0]))):
               if found[i_near]:
                    if any(j_near in range(e[0], e[1]+1) for e in found[i_near]):
                         continue
               if data[i_near][j_near].isnumeric():
                    # check backward
                    curr_j = j_near
                    for var_j in range(len(data[0])):
                         new_j = curr_j-var_j
                         if not data[i_near][new_j].isnumeric() or new_j==-1:
                              break
                    start_j = curr_j-var_j+1
                    for var_j in range(len(data[0])):
                         new_j = curr_j+var_j
                         if new_j==len(data) or not data[i_near][new_j].isnumeric():
                              break
                    end_j = curr_j+var_j-1
                    found[i_near].add((start_j,end_j))
     return found

sum_ratio = 0
for i, row in enumerate(data):
     for j, col in enumerate(row):
          if col != '.' and not col.isnumeric():
               parts[i,j] = (search_nearby(i, j))
          if data[i][j]=='*':
               gear_parts = [int(data[i_found][start:end+1]) for i_found in parts[i,j] for start,end in parts[i,j][i_found]]
               if len(gear_parts)==2:
                    sum_ratio+=math.prod(gear_parts)

all_parts = defaultdict(set)
for elems in parts.values():
     for i in elems:
          all_parts[i].update(elems[i])

print(sum(int(data[i][start:end+1]) for i in all_parts for start,end in all_parts[i]))
print(sum_ratio)