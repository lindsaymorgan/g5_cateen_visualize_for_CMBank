import requests
import json
import csv
import datetime
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
page=1
url = f'https://liveroom.zh.cmbchina.com/chatroom/msgList?toid=7ebc9575afbf425d9553eceadd9046dc&id=1597841666527&page={page}&equalflag=false'
res = requests.get(url)
print(f"直播间消息总数：{res.json()['totalElements']}")
page_num=res.json()['totalPages']

first_flag=0
name_dict=dict()
id_list=list()
time_list=list()
say_list=list()
first_time=dict()
last_time=dict()

for page in tqdm(range(page_num,0,-1)):
    time.sleep(1)
    url = f'https://liveroom.zh.cmbchina.com/chatroom/msgList?toid=7ebc9575afbf425d9553eceadd9046dc&id=1597841666527&page={page}&equalflag=false'
    res = requests.get(url)

    while res.status_code != 200:
        time.sleep(1)
        res = requests.get(url)

    for i in res.json()['content']:
        id_list.append(i['fromid'])
        if i['fromid'] not in name_dict:
            name_dict[i['fromid']]=json.loads(i['message'])['nickname']
            first_time[i['fromid']]=datetime.datetime.fromtimestamp(i['datetime']/1000)
        last_time[i['fromid']]=datetime.datetime.fromtimestamp(i['datetime']/1000)

print([(name_dict[k],v) for k,v in Counter(id_list).items()])
print(len(Counter(id_list)))
print(first_time)
print(last_time)
print(sorted([((last_time[i]-first_time[i]).seconds/60,i )for i in first_time],reverse=True))
plt.hist([(last_time[i]-first_time[i]).seconds/60 for i in first_time], bins=30, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.show()



