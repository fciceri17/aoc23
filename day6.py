import math
import re
from collections import defaultdict

with open('input/day6.txt', 'r') as f:
     data=f.read().strip().splitlines()


# data = '''Time:      7  15   30
# Distance:  9  40  200'''.splitlines()

times = [int(x) for x in data[0].split()[1:]]
dists = [int(x) for x in data[1].split()[1:]]

# v = t0*1
# d = v(t-t0)
# d = t*t0 - t0^2
# 0 = - x^2 + t*x - d
def solve(times, dists):
     roll = []
     for t,d in zip(times,dists):
          t0 = math.ceil((-t + math.sqrt(t**2 - 4*d))/2)-1
          t1 = math.ceil((t + math.sqrt(t**2 - 4*d))/2)
          roll.append((-t0,t1))
     return math.prod((x[1]-x[0] for x in roll))
print(solve(times, dists))

t = [int(''.join(map(str,(times))))]
d = [int(''.join(map(str,(dists))))]
print(solve(t,d))