import math
import re
from collections import defaultdict

with open('input/day5.txt', 'r') as f:
     data=f.read().strip()


# data='''seeds: 79 14 55 13
#
# seed-to-soil map:
# 50 98 2
# 52 50 48
#
# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15
#
# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4
#
# water-to-light map:
# 88 18 7
# 18 25 70
#
# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13
#
# temperature-to-humidity map:
# 0 69 1
# 1 0 69
#
# humidity-to-location map:
# 60 56 37
# 56 93 4'''

def make_map(start, end, override=None):
     entries = data.split(f'{end}:')[0].split(f'{start}:')[-1].strip().splitlines()
     if override:
          entries=override
     entries = [[int(y) for y in x.split()] for x in entries]
     def fn(v):
          for entry in entries:
               if v in range(entry[1], entry[1]+entry[2]):
                    return v-entry[1]+entry[0]
          return v
     return fn

seeds = data.splitlines()[0].replace('seeds: ','').split()
seed_soil = make_map('seed-to-soil map', 'soil-to-fertilizer map')
soil_fertilizer = make_map('soil-to-fertilizer map', 'fertilizer-to-water map')
fertilizer_water = make_map('fertilizer-to-water map', 'water-to-light map')
water_light = make_map('water-to-light map', 'light-to-temperature map')
light_temp = make_map('light-to-temperature map', 'temperature-to-humidity map')
temp_humidity = make_map('temperature-to-humidity map', 'humidity-to-location map')
humidity_location = make_map('','',data.split('humidity-to-location map:')[-1].strip().splitlines())
def get_location(seed):
     soil = seed_soil(seed)
     fert = soil_fertilizer(soil)
     water = fertilizer_water(fert)
     light = water_light(water)
     temp = light_temp(light)
     humidity = temp_humidity(temp)
     location = humidity_location(humidity)
     return location

p1 = min([get_location(int(y)) for y in seeds])
print(p1)
seed_ranges = [(int(seeds[i]),int(seeds[i+1])) for i in range(0,len(seeds),2)]
new_seeds = (x for y in [range(v1,v1+v2) for v1,v2 in seed_ranges] for x in y)
curr_min = p1
for y in new_seeds:
     lo = get_location(y)
     if lo<curr_min:
          curr_min=lo
print(lo)