import re
with open('input/day1.txt', 'r') as f:
     data=f.readlines()


def get_n(v):
     out = []
     curr_l=0
     for i in range(len(v)):
         m=re.match(r'.*(one|two|three|four|five|six|seven|eight|nine).*', v[curr_l:i+1])
         if m:
             out.append(heh(m.groups()))
             curr_l=i
         elif v[i].isnumeric():
             out.append(v[i])
             curr_l=i
     return out


def heh(stt):
    if 'one' in stt:
        return '1'
    if 'two' in stt:
        return '2'
    if 'three' in stt:
        return '3'
    if 'four' in stt:
        return '4'
    if 'five' in stt:
        return '5'
    if 'six' in stt:
        return '6'
    if 'seven' in stt:
        return '7'
    if 'eight' in stt:
        return '8'
    if 'nine' in stt:
        return '9'

dats1 = [''.join(n for n in v if n.isnumeric()) for v in data]
dats2 = [get_n(v) for v in data]
print(sum(int(v[0]+v[-1]) for v in dats1))
print(sum(int(v[0]+v[-1]) for v in dats2))