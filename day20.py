import copy
import json
import math
from itertools import chain
import re
from collections import defaultdict
from functools import cache

with open('input/day20.txt', 'r') as f:
     data=f.read().strip().splitlines()

FLIP = 'FLIP'
CONJ = 'CONJ'

# data='''broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output'''.splitlines()

links = {}
types = {}
for row in data:
     link = row.split(' -> ')
     to = link[1].split(', ')
     base_node = link[0]
     if base_node.startswith('%'):
          base_node=base_node[1:]
          types[base_node]=FLIP
     elif base_node.startswith('&'):
          base_node = base_node[1:]
          types[base_node]=CONJ
     else:
          types[base_node]=None

     links[base_node] = to


def _init_state(type, source):
     if type==FLIP:
          return 0
     return {l: 0 for l,v in links.items() if source in v}

initial_state = {l:_init_state(type, l) for l, type in types.items()}
hits = defaultdict(list)

def step(state, reset_steps=0):
     queue = ['broadcaster']
     lows, highs = 0, 0
     while queue:
          pulsing = queue.pop(0)
          pinged = links[pulsing]
          ping_type = types[pulsing]
          if ping_type == FLIP:
               curr_signal = state[pulsing]
          elif ping_type == CONJ:
               curr_signal = 0 if all(v == 1 for v in state[pulsing].values()) else 1
               if pulsing == 'dd' and sum(state['dd'].values()) > 0:
                    flipped = [x for x, s in state["dd"].items() if s == 1]
                    for up in flipped:
                         if reset_steps not in hits[up]:
                              hits[up].append(reset_steps)
          else:
               curr_signal = 0
               lows+=1
          for node in pinged:
               if curr_signal:
                    highs+=1
               else:
                    lows+=1
               if types.get(node)==FLIP and curr_signal==0:
                    state[node] = 1 - state[node]
                    queue.append(node)
               elif types.get(node) == CONJ:
                    state[node] = {k: v if k != pulsing else curr_signal for k, v in state[node].items()}
                    queue.append(node)
     return lows, highs

def pulse(state, check_rx=False):
     new_state = json.loads(json.dumps(state))
     low, high = step(new_state)
     reset_steps = 1
     if not check_rx:
          while any(s for n,s in new_state.items() if types[n] and types[n]==FLIP) and reset_steps<1000:
               reset_steps+=1
               new_low, new_high = step(new_state, 0)
               low+=new_low
               high+=new_high
     else:
          while len(hits.keys())<len(new_state['dd']):
               reset_steps+=1
               step(new_state, reset_steps)
     return new_state, low, high, reset_steps

next_state, lows, highs, reset = pulse(initial_state)
lows_at_1k = lows*1000//reset
highs_at_1k = highs*1000//reset
print(lows_at_1k*highs_at_1k)

state=initial_state
hits.clear()
pulse(state, True)
print(math.lcm(*[x[0] for x in hits.values()]))