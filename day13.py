import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
with open('input/day13.txt', 'r') as f:
     data=f.read().strip()

# data='''#.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.
#
# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#'''

grids = data.split('\n\n')

def get_col_symmetry(grid, skip=None):
     rows = len(grid)
     cols = len(grid[0])
     for symmetry in range(1, cols):
          if skip==symmetry:
               continue
          proceed=True
          for i in range(rows):
               for j in range(symmetry):
                    if symmetry+j+1>cols or symmetry-j<1:
                         continue
                    if grid[i][symmetry-j-1]!=grid[i][symmetry+j]:
                         proceed=False
                         break
               if not proceed:
                    break
          else:
               # we found symmetry
               return symmetry
     return False

def get_row_symmetry(grid, skip=None):
     rows = len(grid)
     cols = len(grid[0])
     for symmetry in range(1, rows):
          if skip==symmetry:
               continue
          proceed=True
          for j in range(cols):
               for i in range(symmetry):
                    if symmetry+i+1>rows or symmetry-i<1:
                         continue
                    if grid[symmetry-i-1][j]!=grid[symmetry+i][j]:
                         proceed=False
                         break
               if not proceed:
                    break
          else:
               # we found symmetry
               return symmetry
     return False

roll=0
p2=0
for grid in grids:
     g = grid.splitlines()
     s = get_row_symmetry(g)
     if not s:
          s = get_col_symmetry(g)
          skip_row = None
          skip_col = s
     else:
          skip_row = s
          skip_col = None
          s*=100
     roll += s
     for i,c in enumerate(grid):
          if c!='\n':
               smudged = ''.join(x if j!=i else '#' if x=='.' else '.' for j,x in enumerate(grid))
               new_g = smudged.splitlines()
               s = get_row_symmetry(new_g, skip=skip_row)
               if not s:
                    s = get_col_symmetry(new_g, skip=skip_col)
               else:
                    s *= 100
               if s:
                    p2 += s
                    break

print(roll, p2)