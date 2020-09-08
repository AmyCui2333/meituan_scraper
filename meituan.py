import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import re
import json

def gethtmlcode(url,header):
    res = requests.get(url, headers=headers)
    html = res.text
    htmlcode = soup(html, "html.parser")
    return (htmlcode)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Host': 'sh.meituan.com',
    'Referer': 'http://sh.meituan.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Content-Type': 'text/html;charset=utf-8',
    'Cookie':'_lxsdk_cuid=173e35a9e77c8-0078ef7f82fc7f-3323765-e1000-173e35a9e77c8; iuuid=74F6DA7DEE6127CEF65311048287A0884B08CAB941D575D9EC626C6B633D4C61; _lxsdk=74F6DA7DEE6127CEF65311048287A0884B08CAB941D575D9EC626C6B633D4C61; cityname=%E5%B9%BF%E5%B7%9E; ci=10; rvct=10%2C20; uuid=2d6da491743d4e65a489.1597350938.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=173ee611145-79f-8f2-b36%7C%7C9'

}
base_url='https://sh.meituan.com/yundongjianshen/'

filename = "运动健身.csv"
f = open(filename,"w",encoding='utf-8-sig')
header = "名称,地址,最低价,人均消费,评分,评论数,电话号码"
f.write(header + "\n")

ctg_list=[]
area_list=[]
home_soup = gethtmlcode(base_url,headers)
ctg = home_soup.findAll("div",{"class":"tag-group tag-group-expend"})[0]
ctg_tags = ctg.findAll("a")
area = home_soup.findAll("div",{"class":"tag-group tag-group-expend"})[1]
area_tags = area.findAll("a",{"href":re.compile('//sh.meituan.com/yundongjianshen/')})
for a in ctg_tags:
    ctg_list.append(a.get('href'))
for a in area_tags:
    area_list.append(a.get('href'))
a = 0
for ctg_item in ctg_list:
    a=a+1
    b=0
    for area_item in area_list:
        first_url='https:' + ctg_item[:-1] + area_item[33:]
        first_soup = gethtmlcode(first_url, headers)
        b=b+1
        try:
            nav = first_soup.findAll("nav",{"class":"mt-pagination"})[0]
            num = nav.findAll("a")
            if len(num) == 1:
                page_num = 1
            elif len(num) > 1:
                page_num = int(num[-2].text)
            for i in range(1,(page_num+1)):
                url = first_url + 'pn' + str(i) + "/"
                page_soup = gethtmlcode(url,headers)
                js = page_soup.findAll("script")
                script = js[9].text
                data = re.findall("window.AppData = (.*);",script)[0]
                dictdata = json.loads(data)
                search_results = dictdata["searchResult"]
                results = search_results["searchResult"]
                for n in range(len(results)):
                    title = str(results[n]["title"])
                    adrs = str(results[n]["address"])
                    lowp = str(results[n]["lowestprice"])
                    avgp = str(results[n]["avgprice"])
                    score = str(results[n]["avgscore"])
                    comments = str(results[n]["comments"])
                    phone = str(results[n]["phone"])
                    f.write(title + "," + adrs + "," + lowp + "," + avgp + "," + score + "," + comments + "," + phone + "\n")
        except:
            pass
        print('finished catagory ' + str(a) + ' of area' + str(b))
f.close()
