import copy
import json
import math
import re
from collections import defaultdict
from functools import cache
from queue import PriorityQueue

with open('input/day17.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533'''.splitlines()

def dijkstra(G, start, goal):
    """ Uniform-cost search / dijkstra """
    visited = set()
    start = (start, 0, None)
    cost = {start: 0}
    parent = {start: None}
    todo = PriorityQueue()

    todo.put((0, start))
    while todo:
        while not todo.empty():
            v_cost, vertex = todo.get()  # finds lowest cost vertex
            # loop until we get a fresh vertex
            if vertex not in visited: break
        else:  # if todo ran out
            break  # quit main loop
        visited.add(vertex)
        location, dir_counter, previous_direction = vertex
        if location == goal:
            break
        for neighbor, distance in G[location].items():
            # if the distance to the neighbor is shorter using the current node,
            # update the distance for the neighbor
            direction = (neighbor[0] - location[0], neighbor[1] - location[1])
            if previous_direction == direction:
                new_dir_counter = dir_counter+1
            elif previous_direction and (
                    previous_direction[0] == direction[0] and previous_direction[1] == -direction[1] or previous_direction[1] ==
                    direction[1] and previous_direction[0] == -direction[0]):
                continue
            else:
                new_dir_counter = 0
            neighbor = (neighbor, new_dir_counter, direction)
            if neighbor in visited or new_dir_counter>2: continue  # skip these
            old_cost = cost.get(neighbor, float('inf'))  # default to infinity
            new_cost = cost[vertex] + distance
            if new_cost < old_cost:
                todo.put((new_cost, neighbor))
                cost[neighbor] = new_cost
                parent[neighbor] = vertex

    return parent, v_cost


def make_path(parent, goal):
    goal = next(x for x in parent if x[0]==goal)
    if goal not in parent:
        return None
    v = goal
    path = []
    while v is not None:  # root has null parent
        path.append(v)
        v = parent[v]
    return path[::-1]



graph = {}
rows = len(data)
cols = len(data[0])
directions = [(0,1), (0,-1), (1,0), (-1,0)]

for i, v in enumerate(data):
     for j, c in enumerate(v):
          reachable = {}
          for _dir in directions:
               potential_r, potential_c = i+_dir[0], j+_dir[1]
               if potential_r>=rows or potential_r<0 or potential_c>=cols or potential_c<0:
                    continue
               else:
                    reachable[(potential_r, potential_c)]=int(data[potential_r][potential_c])
          graph[(i,j)]=reachable

parent, cost = dijkstra(graph, (0,0), (rows-1, cols-1))
path = make_path(parent, (rows-1, cols-1))
basic_path = [x[0] for x in path]
out_grid = [list(x) for x in data]
for i in range(rows):
    for j in range(cols):
        if (i,j) in basic_path:
            out_grid[i]=[x if jj!=j else 'X' for jj,x in enumerate(out_grid[i])]

print(cost)
# print('\n'.join(''.join(x) for x in out_grid))