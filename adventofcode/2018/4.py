'''
tl;dr Sort by date to get the guard entries in the right order. The other thing that's key is that all of a Guard's data gets over before the next Guard starts. Use patterns in lines between guards
to solve this.
'''
import re
import sys
from collections import Counter
from operator import itemgetter

#Part 1
with open('4.txt') as f:
#with open('dump') as f:
    data = f.read().rstrip().split('\n')

mins = {}

# Sort records so they're in the right order
data = sorted(data)

for record in data:
    match = re.match(r'\[(.*)\]\s{1}(.*)', record)
    if match:
        #Get date and time
        date_and_time = match.group(1)
        date,time = date_and_time.split(' ')
        year,month,day = date.split('-')
        hour,minute = time.split(':')
        minute = int(minute)

        #Get Guard Id
        guard_data = match.group(2)
        t1 = guard_data.split(' ')
        if guard_data.startswith('Guard'):
            gid = t1[1][1:]
            
            #Initialize guard dictionary
            if gid not in mins.keys():
                mins[gid] = []
            wake_min_start = int(minute)

        #Get sleep data
        elif guard_data.startswith('falls'):
            sleep_min_start = int(minute)

        #Get awake data
        elif guard_data.startswith('wakes'):
            for i in range(sleep_min_start, minute):
                mins[gid].append(i)

# Guard who spends the most minutes asleep
gids = sorted(mins, key=lambda k: len(mins[k]), reverse=True)

for gid,minutes in mins.items():
    if gid == gids[0]:
        tmin = Counter(minutes).most_common(1)[0]
        print("Part 1:", int(tmin[0]) * int(gid))

#Part 2
gid_times = {}
gid_mins = {}
for gid,minutes in mins.items():
    if minutes:
        gid_times[gid] = Counter(minutes).most_common(1)[0][1]
        gid_mins[gid] = Counter(minutes).most_common(1)[0][0]

sorted_by_count = sorted(gid_times.items(), key=itemgetter(1), reverse=True)[0][0]
print("Part 2", int(sorted_by_count) * int(gid_mins[sorted_by_count]))
