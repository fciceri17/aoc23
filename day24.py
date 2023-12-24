import copy
import json
import numpy as np
import math
import re
from collections import defaultdict
from functools import cache

with open('input/day24.txt', 'r') as f:
     data=f.read().strip().splitlines()


# data='''19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3'''.splitlines()

stones = {}

for i,row in enumerate(data):
    coords, speed = row.split('@')
    stones[i]={'coords': tuple(int(x) for x in coords.split(', ')), 'speed': tuple(int(x) for x in speed.split(', '))}

def solve_intersection_xy(stone1, stone2, indexes = [0,1]):
    # stone: x = x1+at
    # stone: y = y1+bt
    # x1+a*t=x2+c*l
    # y1+b*t=y2+d*l
    # cl-at = x1-x2
    # dl-bt = y1-y2
    # l = (x1-x2+at)/c
    # d(x1-x2+at)/c - bt = y1-y2
    # x1-x2+at - bt*c/d = (y1-y2)*c/d
    # (a - bc/d)t = (y1-y2)*c/d + x2-x1
    # t = ((y1-y2)*c/d +x2-x1)/(a-bc/d)
    denominator = (stone1['speed'][indexes[0]]-stone1['speed'][indexes[1]]*stone2['speed'][indexes[0]]/stone2['speed'][indexes[1]])
    if denominator==0:
        return False
    t = ((stone1['coords'][indexes[1]]-stone2['coords'][indexes[1]])*stone2['speed'][indexes[0]]/stone2['speed'][indexes[1]] + stone2['coords'][indexes[0]]-stone1['coords'][indexes[0]])/denominator
    l = (stone1['coords'][indexes[0]]-stone2['coords'][indexes[0]]+stone1['speed'][indexes[0]]*t)/stone2['speed'][indexes[0]]
    if t<0:
        return False
    if l<0:
        return False
    x,y = stone1['coords'][indexes[0]]+stone1['speed'][indexes[0]]*t, stone1['coords'][indexes[1]]+stone1['speed'][indexes[1]]*t

    return x,y

v_min = 200000000000000 if len(data)>100 else 7
v_max = 400000000000000 if len(data)>100 else 27
roll=0
for i in range(len(stones)):
    for j in range(i+1, len(stones)):
        res = solve_intersection_xy(stones[i], stones[j])
        if res:
            x,y=res
            if v_min<=x<=v_max and v_min<=y<=v_max:
                roll+=1

print(roll)


# magical stone
# x = speed0x*t+x0
# y = speed0y*t+y0
# z = speed0z*t+z0
# for some t
# x = speed1x *t + x1
# y = speed1y *t + y1
# z = speed1z *t + z1
# speed0x*t1+x0 = speed1x *t1 + x1
# t1(speed1x-speed0x) = x0-x1
# t1 = (x0-x1)/(speed1x-speed0x)
# t1 = (y0-y1)/(speed1y-speed0y)
# t1 = (z0-z1)/(speed1z-speed0z)
# (y0-yN)/(speedNy-b) = (x0-xN)/(speedNx-a)
# (y0-yN)/(speedNy-b) = (x0-xN)/(speedNx-a)
from sympy import symbols, Eq, solve
t1, t2, t3, x0, y0, z0, sx, sy, sz = symbols('t1 t2 t3 x0 y0 z0 sx sy sz')
eqs = [[Eq(t*(stones[i]['speed'][v]-velocity), stones[i]['coords'][v]-coord) for v, coord, velocity in [(0, x0, sx), (1, y0, sy), (2,z0, sz)]] for t, i in zip((t1,t2,t3), range(3))]

solution = solve([x for y in eqs for x in y], (t1,t2,t3,x0,y0,z0,sx,sy,sz))
print(sum(solution[0][3:6]))
