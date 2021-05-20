import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
#read file
f = open('chatroom-6.txt', "r",encoding="utf-8")
lines = f.readlines()
f.close()
message_search_value='<div class="talklist-item">'
user_search_str='<span class="name">'
time_search='<span class="time">'
#looking for patterns
count=0
for line in lines:
    if line.strip()==message_search_value:
        count += 1
       # line = line.strip().lower().split()
       # for words in line:
       #     if words.find(message_search_value.lower()) != -1:
       #         print(words)
print(f"直播间消息总数：{count}")

first_flag=0
name_list=list()
first_time=dict()
last_time=dict()
for line in lines:
    if len(re.split(user_search_str, line.strip()))!=1:
        name=re.split('</span>',re.split(user_search_str, line.strip())[1])[0]
        if name not in name_list:
            first_flag=1
        name_list.append(name)

    if len(re.split(time_search, line.strip()))!=1:
        time = datetime.strptime(re.split('</span>', re.split(time_search, line.strip())[1])[0],'%Y-%m-%d %H:%M:%S')
        if first_flag==1:
            first_time[name]=time
            first_flag=0
        last_time[name]=time

        # print(name)
        # name_set.add(name)
       # line = line.strip().lower().split()
       # for words in line:
       #     if words.find(message_search_value.lower()) != -1:
       #         print(words)
print(Counter(name_list))
print(first_time)
print(last_time)
print(sorted([((last_time[i]-first_time[i]).seconds/60,i )for i in first_time],reverse=True))
plt.hist([(last_time[i]-first_time[i]).seconds/60 for i in first_time], bins=30, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.show()
print(f"直播间互动人数：{len(Counter(name_list))}")

