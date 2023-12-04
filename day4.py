import math
import re
from collections import defaultdict

with open('input/day4.txt', 'r') as f:
     data=f.read().strip().splitlines()


# data='''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.splitlines()


tot=0
obtain = defaultdict(int)
for card in data:
     card_id, numbers = card.split(': ')
     card_id = card_id.replace('Card ', "").strip()
     obtain[card_id]+=1
     winning, have = numbers.split(' | ')
     score = -1
     have = have.split()
     for entry in winning.split():
          if entry in have:
               score+=1
     if score>=0:
          tot+=2**score
          for i in range(int(card_id)+1, int(card_id)+int(score)+2):
               obtain[str(i)]+=obtain[card_id]

print(tot)
print(sum(obtain.values()))