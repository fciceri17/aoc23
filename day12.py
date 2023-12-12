import copy
import json
import math
import re
from collections import defaultdict

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

def enumerate_variations(input_string, expect):
     max_g = sum(expect)
     queue = [input_string]
     output = 0

     while queue:
          elem = queue.pop()
          low_bound = elem.count('#')
          var = elem.count('?')
          if low_bound<=max_g:
               if '?' in elem:
                    if low_bound+var>max_g:
                         candidate = elem.replace('?','.',1)
                         if complete_groups(candidate, expect):
                              queue.append(candidate)
                    if low_bound < max_g:
                         candidate = elem.replace('?','#',1)
                         if complete_groups(candidate, expect):
                              queue.append(candidate)

               else:
                    # v = count_groups_faster(elem)
                    # if v==expect:
                    if count_groups(elem, expect):
                         output+=1

     return output

def complete_groups(candidate, expected):
     roll = 0
     i=0
     for c in candidate:
          if c=='?':
               return True
          if c=='.':
               if roll>0:
                    if roll != expected[i]:
                         return False
                    i+=1
                    if i==len(expected):
                         return True
               roll=0
          if c=='#':
               roll+=1
     return i==len(expected) or roll==expected[i]


def count_groups(input_string, expect):
     i=0
     roll=0
     for char in input_string:
          if char=='.':
               if roll>0:
                    if roll!=expect[i]:
                         return False
                    i+=1
               roll=0
          else:
               roll+=1
     if i<len(expect)-1:
          return False
     if roll>0:
          if roll != expect[i]:
               return False
     return expect


p1 = 0
for i, row in enumerate(rows):
     variations = enumerate_variations(row, counts[i])
     p1+=variations
print(p1)
p2 = 0
for i, row in enumerate(rows_p2):
     variations = enumerate_variations(row, counts_p2[i])
     p2+=variations
print(p2)