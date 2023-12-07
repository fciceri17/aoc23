import math
import re
from collections import defaultdict

with open('input/day7.txt', 'r') as f:
     data=f.read().strip().splitlines()

# data='''32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483'''.splitlines()


hand_map = {
     5:5,
     4:4,
     'full':3,
     3:2,
     '2pair':1,
     2: 0
}

reverse_hand_map = {v:k for k,v in hand_map.items()}
def score_hand(cards):
     counts=defaultdict(int)
     for c in cards:
          counts[c]+=1
     check_full=False
     check_2pair=False
     for value, score in counts.items():
          if score>3:
               return hand_map[score]
          if score==3:
               if not check_full:
                    check_full=True
               else:
                    return hand_map['full']
          if score==2:
               if not check_2pair:
                    check_2pair=True
               else:
                    return hand_map['2pair']
               if not check_full:
                    check_full=True
               else:
                    return hand_map['full']
     if check_full and check_2pair:
          return hand_map[2]
     if check_full:
          return hand_map[3]
     return -1


vs = 'A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2'

ranked = {c:-i for i,c in enumerate(vs.split(', '))}

def sort_fn(cards, scorer=score_hand, order=ranked):
     score = scorer(cards)
     card_order = [order[v] for v in cards]
     return score, card_order

all_hands = [v.split() for v in data]
sorted_hands = sorted(all_hands, key=lambda x: sort_fn(x[0]))
print(sum((i+1)*int(v[1]) for i,v in enumerate(sorted_hands)))

new_order = {k:v if k!='J' else -1000 for k,v in ranked.items()}
def score_hand_j(cards):
     counts=defaultdict(int)
     for c in cards:
          counts[c]+=1
     score = score_hand(cards)
     if 'J' not in counts:
          return score
     if hand_map.get(counts['J'],0)==score:
          if score==5:
               return 5
          return hand_map[counts['J']+max(v for k,v in counts.items() if k!='J')]
     scored = reverse_hand_map.get(score, 'high_card')
     if scored=='high_card':
          return 0 # ONLY 1 J
     if isinstance(scored, int):
          return hand_map[scored+counts['J']]
     if scored=='2pair':
          if counts['J']==1:
               return hand_map['full']
          return hand_map[4]
     if counts['J']==3:
          return 5
     return hand_map[3+counts['J']]

sorted_hands_j = sorted(all_hands, key=lambda x: sort_fn(x[0], scorer=score_hand_j, order=new_order))
print(sorted_hands_j)
print(sum((i+1)*int(v[1]) for i,v in enumerate(sorted_hands_j)))
