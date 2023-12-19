import copy
import json
import math
from itertools import chain
import re
from collections import defaultdict
from functools import cache

with open('input/day19.txt', 'r') as f:
     data=f.read().strip()

# data='''px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}
#
# {x=787,m=2655,a=1222,s=2876}
# {x=1679,m=44,a=2067,s=496}
# {x=2036,m=264,a=79,s=2244}
# {x=2461,m=1339,a=466,s=291}
# {x=2127,m=1623,a=2188,s=1013}'''

data=data.split('\n\n')
workflows = data[0].splitlines()
inputs = data[1].splitlines()


wfs = {}
mappings = {}
for row in workflows:
     name, rest = row.split('{')
     instructions = rest[:-1]

     mappings[name]=[]
     for instr in instructions.split(','):
          if ':' in instr:
               condition = instr.split(':')
               symbol, comparison, value = re.match('([xmas])([<>])(\d+)', condition[0]).groups()
               dest = condition[1]
               mappings[name].append((lambda x, symbol=symbol, value=value, comparison=comparison: x[symbol] > int(value) if comparison =='>' else x[symbol] < int(value), dest, (symbol, comparison, value)))
          else:
               mappings[name].append((lambda x: True, instr, 'default'))
     pass
     def fn(data, n = name):
          for func, dest, debug in mappings[n]:
               v = func(data)
               if v:
                    if dest in ('A', 'R'):
                         return dest
                    else:
                        return wfs[dest](data, dest)
     wfs[name]=fn

entries = [ent[1:-1].split(',') for ent in inputs]
iterable_entries = [dict((lambda x: (x[0], int(x[1])))(e.split('=')) for e in en) for en in entries]


roll=0
for e in iterable_entries:
     v = wfs['in'](e)
     if v=='A':
          roll+=sum(e.values())
print(roll)

# for p2, we define a stop_at_A function that iterates through the debug statements to find valid ranges, exploring all possible branches

vmin, vmax = 1, 4000

ranges = {l:(vmin, vmax) for l in 'xmas'}

def stop_at_a(value_ranges, wf):
     if wf=='A':
          yield value_ranges
     elif wf=='R':
          pass
     else:
          next_range = dict(value_ranges)
          for _, dest, condition in mappings[wf]:
               if condition == 'default':
                         yield from stop_at_a(next_range, dest)
               else:
                    symbol, comparison, value = condition
                    if comparison == '>':
                         new_range = (int(value)+1, next_range[symbol][1])
                         complement = (next_range[symbol][0], int(value))
                    else:
                         new_range = (next_range[symbol][0], int(value)-1)
                         complement = (int(value), next_range[symbol][1])
                    if new_range[0]>new_range[1]:
                         continue
                    else:
                         next_range[symbol]=new_range
                         yield from stop_at_a(dict(next_range), dest)
                         next_range[symbol]=complement

v_ranges = list(stop_at_a(ranges,'in'))
print(v_ranges)
print(roll)
print(sum(math.prod(m2-m1+1 for m1, m2 in valid_range.values()) for valid_range in v_ranges if valid_range))