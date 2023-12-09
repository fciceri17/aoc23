import json
import math
import re
from collections import defaultdict

with open('input/day9.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45'''.splitlines()

data=[[int(x) for x in y.strip().split()] for y in data]
orig_data=json.loads(json.dumps(data))
endings = []
begs = []

for seq in data:
     steps = [seq]
     while any(x!=0 for x in steps[-1]):
          steps.append([steps[-1][i]-steps[-1][i-1] for i in range(1,len(steps[-1]))])
          pass
     rev_steps = steps[::-1]
     for i, step in enumerate(rev_steps):
          if i>0:
               step.append(step[-1]+rev_steps[i-1][-1])
               step.insert(0, step[0] - rev_steps[i - 1][0])

          if i==len(steps)-1:
               endings.append(step[-1])
               begs.append(step[0])
print(sum(endings))
print(sum(begs))