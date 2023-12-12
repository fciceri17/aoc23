import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
with open('input/day12.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1'''.splitlines()

rows, counts = zip(*[x.split() for x in data])
counts = [tuple([int(x) for x in y.split(',')]) for y in counts]

rows_p2 = ['?'.join([x]*5) for x in rows]
counts_p2 = [x*5 for x in counts]

def smart_variations(input_string, expect):
     @cache
     def dyn_score(i, ex, blength):
          if i==len(input_string):
               if (ex == len(expect) and blength == 0) or (ex==len(expect)-1 and expect[ex]==blength):
                    return 1
               else:
                    return 0
          v = 0
          # dot on empty block
          def missing_block():
               return dyn_score(i+1, ex, 0)
          # dot on non-empty block but within limits
          def finish_block():
               return dyn_score(i+1, ex+1, 0)
          # broken block
          def continue_block():
               return dyn_score(i+1, ex, blength+1)

          if input_string[i] in ('.','?') and blength==0:
               v+= missing_block()
          if input_string[i] in ('.','?') and ex<len(expect) and expect[ex]==blength:
               v+= finish_block()
          if input_string[i] in ('#', '?'):
               v+= continue_block()
          return v
     return dyn_score(0,0,0)

p2 = 0
for i, row in enumerate(rows_p2):
     variations = smart_variations(row, counts_p2[i])
     p2+=variations
     print(i)
print(p2)