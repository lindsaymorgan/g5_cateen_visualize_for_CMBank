# 百度地图：http://map.baidu.com/  百度地图poi：http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
# coding:utf-8
# github:https://github.com/tianyu8969/python-to-baidumap
# *注意* 百度最多返回400条记录

import json
import xlwt
from datetime import datetime
from urllib import request
from urllib.parse import quote
import sys
import time
import pandas as pd
import re
import sys
from tqdm import tqdm
canteen_pd=pd.read_excel('金葵花餐厅恢复情况收集-0701.xlsx')
canteen_pd_sub_1=canteen_pd[canteen_pd['是否在线']==1]
canteen_pd_sub_2=canteen_pd[canteen_pd['是否在线']!=1]
# bank_list=['增城','荔湾','滨江东','东山','华强','科技园'] #'分营',
# canteen_list=["熹素","五号茶居","宋川菜","mortons grille","江由辉师傅主理","海门鱼仔店","蔓莳创意美蔬","COVA"] #,"The Maple Leaf"
canteen_list_sub1=set([re.split(r"[（(]",i)[0] for i in canteen_pd_sub_1['门店名称']])
canteen_list_sub2=set([re.split(r"[（(]",i)[0] for i in canteen_pd_sub_2['门店名称']])
# canteen_list=[]
# with open('cateen_name.txt','r',encoding='utf-8') as f:
# 	for line in f:
# 		canteen_list.append(line.strip('\n').split(',')[0])

# canteen_list=['点都']
#
#
# num = [i.split('（')[0] for i in list(canteen_pd['门店名称'])]

# 获取当前日期
today = datetime.today()
# 将获取到的datetime对象仅取日期如：2017-4-6
today_date = datetime.date(today)

json_name = 'data_tmap.json'
# 百度地图poi：http://api.map.baidu.com/place/v2/search
# 请替换为自己申请的key值：申请Web服务API类型KEY http://lbsyun.baidu.com/apiconsole/key?application=key
# ak=8VUjfqGwgnHwEZLxwPpnZvO1Sgeq2HFO
# http://api.map.baidu.com/place/v2/search?query=卫生服务中心&tag=医疗&page_size=20&page_num=0&scope=2&region=上海&coord_type=3&output=json&ak=8VUjfqGwgnHwEZLxwPpnZvO1Sgeq2HFO
# url_amap = 'http://api.map.baidu.com/place/v2/search?query=招商银行bank支行&page_size=20&page_num=pageindex&scope=1&region=广州市&coord_type=3&output=json&ak=8VUjfqGwgnHwEZLxwPpnZvO1Sgeq2HFO'
url_amap = 'http://api.map.baidu.com/place/v2/search?query=canteen&page_size=20&page_num=pageindex&scope=1&region=广州市&coord_type=3&output=json&ak=8VUjfqGwgnHwEZLxwPpnZvO1Sgeq2HFO'
# url_amap = 'http://api.map.baidu.com/place/v2/search?query=地铁站&tag=交通设施&page_size=20&page_num=0&scope=1&bounds=39.671107, 116.078440,40.233799, 116.431564&coord_type=3&output=json&ak=8VUjfqGwgnHwEZLxwPpnZvO1Sgeq2HFO'
# url_amap = 'http://api.map.baidu.com/place/v2/search?query=地铁站&tag=交通设施&page_size=20&page_num=0&scope=1&bounds=39.671107, 116.431564,40.241761, 116.757228&coord_type=3&output=json&ak=8VUjfqGwgnHwEZLxwPpnZvO1Sgeq2HFO'

page_size = 20  # 每页条目数，最大限制为20条
page_index = r'page_num=1'  # 显示页码
total_record = 0  # 定义全局变量，总行数，百度有限制不能超过400条
# Excel表头
hkeys = ['canteen_name', 'line', 'lat', 'lon']
# 获取数据列
bkeys = [ 'name',  'address',  ['location', 'lat', 'lng']]

u"""
        城市内检索
        百度在没有查找到对应查询请求时, 会返回在其它城市查找到的结果, 返回格式为[{'num': , 'name': ''} ...]这样的数组
        获取一页query相关地理信息
        根据关键词query查找所有地址信息
        *注意* 百度最多返回400条记录
        :param query: 查询关键词
        :param region: 地区
        :param kwargs:
        :return:  if success return
            {
                status: 本次API访问状态, 成功返回0, 其他返回其他数字,
                message: 对本次API访问状态值的英文说明, 如果成功返回'ok', 失败返回错误说明,
                total: 检索总数, 用户请求中设置了page_num字段时才会出现, 当检索总数超过760时, 多次刷新同一请求得到的total值, 可能稍有不同
                results: [
                    {
                        name:  POI名称,
                        location: {
                            lat: 纬度,
                            lng: 经度
                        },
                        address: POI地址信息,
                        telephone: POI电话信息,
                        uid: POI的唯一标识,
                        detail_info: {  # POI扩展信息, 仅当scope=2时, 显示该字段, 不同POI类型, 显示的detail_info字段不同
                            distance: 距离中心点距离,
                            type: POI类型,
                            tag: 标签,
                            detail_url: POI的详情页,
                            price: POI商户的价格,
                            shop_hours: 营业时间,
                            overall_rating: 总体评分,
                            taste_rating: 口味评分,
                            service_rating: 服务评分,
                            environment_rating: 环境评分,
                            facility_rating: 星级评分,
                            hygiene_rating: 卫生评分,
                            technology_rating: 技术评分,
                            image_num: 图片数,
                            groupon_num: 团购数,
                            discount_num: 优惠数,
                            comment_num: 评论数,
                            favorite_num: 收藏数,
                            checkin_num: 签到数
                        }
                    }
                    ...
                ]
            }
            else return None.
        """
# 获取数据
def get_data(canteen_name,pageindex):
    global total_record
    # 暂停500毫秒，防止过快取不到数据
    time.sleep(0.5)
    print('解析页码： ' + str(pageindex) + ' ... ...')
    url = url_amap.replace('pageindex', str(pageindex))
    url = url_amap.replace('canteen', canteen_name)
    # 中文编码
    url = quote(url, safe='/:?&=')
    html = ""
    with request.urlopen(url) as f:
        html = f.read()
    rr = json.loads(html)
    if total_record == 0:
        total_record = int(rr['total'])
    return [[i['name'],i['address'],i['location']['lat'],i['location']['lng']]  for i in rr['results'] if 'address' in i]


def getPOIdata(canteen_list):

    result=list()
    for index,canteen_name in tqdm(enumerate(canteen_list)):
        global total_record
        print('获取POI数据开始')
        tmp=get_data(canteen_name,0)
        for u in tmp:
            result.append(u)
        if (total_record % page_size) != 0:
            page_number = int(total_record / page_size)
        else:
            page_number = int(total_record / page_size)

        for each_page in range(1, page_number):
            tmp=get_data(canteen_name,each_page)
            for u in tmp:
                result.append(u)

    return result



if __name__ == '__main__':
    # 写入数据到json文件，第二次运行可注释
    # canteen_list = ['点都']
    result=getPOIdata(canteen_list_sub1)
    res_pd=pd.DataFrame.from_records( result, columns=['Name', 'Place', 'lat', 'lon'])
    res_pd.to_csv('canteen_list_sub1.csv',index=0)

    result = getPOIdata(canteen_list_sub2)
    res_pd = pd.DataFrame.from_records(result, columns=['Name', 'Place', 'lat', 'lon'])
    res_pd.to_csv('canteen_list_sub2.csv', index=0)
    # 读取json文件数据写入到excel
    # write_data_to_excel("diandou_position")