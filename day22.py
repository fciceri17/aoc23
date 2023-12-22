import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
from queue import PriorityQueue

with open('input/day22.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9'''.splitlines()

bricks = [[[int(v) for v in  y.split(',')] for y in x.split('~')] for x in data]
z_bricks = defaultdict(list)
for i,brick in enumerate(bricks):
    for z_v in range(brick[0][-1], brick[1][-1]+1):
        z_bricks[z_v].append(i)

def touching(brick1, brick2):
    x1,y1,_ = brick1[0]
    x2,y2,_ = brick1[1]
    x3,y3,_ = brick2[0]
    x4,y4,_ = brick2[1]

    assert x1<=x2
    assert x3<=x4
    assert y1<=y2
    assert y3<=y4

    if y1==y2: # horizontal
        if y3<=y1<=y4 and (x1<=x3<=x2 or x1<=x4<=x2 or x3<=x1<=x4 or x3<=x2<=x4):
            return True
    else:
        if x3<=x1<=x4 and (y1<=y3<=y2 or y1<=y4<=y2 or y3<=y1<=y4 or y3<=y2<=y4):
            return True
    return False

def fall(z_bricks):
    moved = set()
    new_z_bricks = defaultdict(list)
    new_z_bricks[1]=copy.copy(z_bricks[1])
    for z_axis in sorted(z_bricks):
        if z_axis>1:
            for brick_index in z_bricks[z_axis]:
                brick = bricks[brick_index]
                if not any(b==brick_index or touching(brick, bricks[b]) for b in new_z_bricks[z_axis-1]):
                    moved.add(brick_index)
                    new_z_bricks[z_axis-1].append(brick_index)
                else:
                    new_z_bricks[z_axis].append(brick_index)
    return new_z_bricks, moved

z_bricks, fallen = fall(z_bricks)
while fallen:
    z_bricks, fallen = fall(z_bricks)

at_rest = {}
for z_axis, brick_indices in z_bricks.items():
        for br_idx in brick_indices:
            brick = bricks[br_idx]
            if z_axis+1 in z_bricks:
                at_rest[br_idx] = set(potentially_touching for potentially_touching in z_bricks[z_axis + 1] if touching(brick, bricks[potentially_touching]) and potentially_touching!=br_idx)
            else:
                at_rest[br_idx]=set()

supported = {brick_idx: {k for k,touching_set in at_rest.items() if brick_idx in touching_set} for brick_idx in at_rest}
roll=0
for _, supporting in at_rest.items():
    if all(len(supported[on_top]) > 1 for on_top in supporting):
        roll+=1
print(roll)

end_state = z_bricks
roll2=0
for i, _ in enumerate(bricks):
    moved=set()
    z_bricks = {k:[x for x in v if x!=i] for k,v in end_state.items()}
    z_bricks, fallen = fall(z_bricks)
    while fallen:
        moved.update(fallen)
        z_bricks, fallen = fall(z_bricks)
    roll2+=len(moved)
print(roll2)