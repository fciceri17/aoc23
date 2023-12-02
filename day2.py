import re
with open('input/day2.txt', 'r') as f:
     data=f.readlines()


# data='''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.splitlines()

target = {'red':12, 'green': 13, 'blue': 14}
source = {}
for entry in data:
     v = re.match(r'Game ([0-9]+): (.*)', entry)
     idg, vs = v.groups()
     source[int(idg)] = [{v: int(k) for k,v in [x.split(' ') for x in counts.split(', ')]} for counts in vs.split('; ')]

impossible = set()
for game_id, draws in source.items():
     for color, maa in target.items():
          if any(v.get(color,0)>maa for v in draws):
               impossible.add(int(game_id))
print(sum(x for x in source if x not in impossible))


added = []
for game, draws in source.items():
     drawn=[]
     for color in target:
          v = max(t.get(color,0) for t in draws)
          drawn.append(v)
     added.append(drawn[0]*drawn[1]*drawn[2])
print(sum(added))