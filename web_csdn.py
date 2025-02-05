# -- coding: utf-8 -- 
# Author: CTL
# Created: 2025-2-5
# Description: CTL Media Spider for Weibo Hot
"https://blog.csdn.net/m0_72947390/article/details/132832280" # 作为初始参考
from base64 import encode
import io
import os
import re 
import sys
import requests
import time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, false
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import requests  
from urllib import parse  
# from parse_html import get_dataframe_from_html_text  
import logging  
# from rich.progress import track    
  
logging.basicConfig(level=logging.INFO)  

global engine
# TODO 增加数据库连接
def check_engine(check_engine_name):
    if check_engine_name is None:
        logging.error("engine is None")
        engine =create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/alice_py",echo=True, max_overflow=5)
        return False
    if check_engine_name == "local":
        engine =create_engine("mysql+pymysql://root:123456@localhost:3306/alice_py",echo=True, max_overflow=5)
    elif check_engine_name == "web":
        engine =create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/alice_py",echo=True, max_overflow=5)
    return engine # 也不需要返回，因为全局变量engine已经被赋值了

# TODO 增加现在的网页版热搜获取(手机版没有"热""爆"等标签),并存入数据库
def get_wb_hot(cookie):
    # engine =create_engine("mysql+pymysql://root:tai%40aile401120@127.0.0.1:3306/alice",echo=True, max_overflow=5)
    url = "https://s.weibo.com/top/summary?click_from=index_rank_more&cate=realtimehot" # 网页热搜
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
               , 'Cookie': cookie}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    wb_hot_list = []
    for i in soup.find_all('tr', class_=''):
        wb_hot_list.append(i)
    del wb_hot_list[0] # 删除第一行
    try:
     # 遍历热搜列表
     for i in wb_hot_list:
       data ={}
       datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 时间
       hot_order = i.find("td").text.strip()
       if hot_order == "•" : # 排名为"•"的为广告或者辟谣等
         hot_order="-1"
         url = "https://s.weibo.com"+i.find('a')['href_to']
         hot_content = i.find('td',class_="td-02").text.strip()
         try: # 有推荐广告，热度为0。
            hot_degree = extract_numbers(i.find('span').text.strip())[0]
         except:
             hot_degree = 0
         hot_sign = i.find('td',class_="td-03").text.strip()
       else:   
         url = "https://s.weibo.com"+i.find('a')['href']
         print("url is :"+url)
         # 通过热搜url获取具体的作者等信息
         data = get_author_and_host(url,cookie)
         print(data,flush=True)
         author = data["author"]
         author_url = data["author_url"]
         host = data["host"]
         host_url = data["host_url"]
         hot_content = i.find('td',class_="td-02").text.strip()
         try: # 有推荐广告，热度为0，其实代码逻辑上避免了
            hot_degree = extract_numbers(i.find('span').text.strip())[0]    
         except:
             hot_degree = 0
         hot_sign = i.find('td',class_="td-03").text.strip()
       time.sleep(2) # 防止频繁访问
    #    engine.execute("insert into wb_hot_author(hot_order,hot_degree,content,sign,create_time,url,author,author_url,host,host_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (hot_order,hot_degree,hot_content,hot_sign,datetime,url,author,author_url,host,host_url))     
    finally:
         # 关闭数据库
         print("end")
        #  engine.dispose()
         


def extract_numbers(s):
    # 使用正则表达式查找所有数字
    numbers = re.findall(r'\d+', s)
    return numbers   


# TODO 增加cookie获取方法
def get_cookie():
    # cookie一段时间会变化，先每次获取最新的cookie
    cookie = ""
    return cookie


def get_author_and_host(url,cookie):
     data = {"author":"","author_url":"","host":"","host_url":""}
    #  url = "https://s.weibo.com/weibo?q=%23%E4%BD%A0%E5%A5%BD%E6%9D%8E%E7%84%95%E8%8B%B1%E7%BB%99%E5%93%AA%E5%90%92%E7%9A%84%E8%B4%BA%E5%9B%BE%23&t=31&band_rank=1&Refer=top" # 单条具体热搜
    #  url ="https://s.weibo.com/weibo?q=%E8%97%95%E9%A5%BC&t=31&band_rank=48&Refer=top"
     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
               , 'Cookie': cookie}
     response = requests.get(url, headers=headers)
     soup = BeautifulSoup(response.text, 'html.parser')
     # 判断url中是否含有# 判断是否为话题（有话题有话题主持人，有host）
     if "%23" in url: # 有话题，记录置顶和话题主持人
         soup1 = soup.find('div', class_="card-user-a") 
         host = soup1.find('a',class_="name").text.strip() # 寻找话题主持人
         host_url = "https:"+soup1.find('a')['href'] # 话题主持人url
         data["host"] = host
         data["host_url"] = host_url
         soup2 = soup.find('div', class_="card-feed")
         author = soup2.find('a',class_="name").text.strip() # 寻找作者
         data["author"] = author
         author_url = "https:"+soup2.find('a',class_="name")['href'] # 作者url
         data["author_url"] = author_url
     else: # 没有话题，记录作者
         soup1 = soup.find('div', class_="card-feed")
         author = soup1.find('a',class_="name").text.strip() # 寻找作者
         author_url = "https:"+soup1.find('a',class_="name")['href'] # 作者url
         data["author"] = author
         data["author_url"] = author_url
     return data


if __name__ == "__main__":  
    # cookie ="SINAGLOBAL=720276293468.316.1728443512183; SCF=AoEXykP1GwUoQtJjIvCELZG66a7yIu3_PPacGdQls8pIEH3A_D__H_0IOWMDoxiZDzEuGC60o4blE2RxnVX7aWI.; _s_tentry=weibo.com; Apache=7544007357406.682.1738716345122; ULV=1738716345200:17:1:1:7544007357406.682.1738716345122:1737336551146; ALF=1741309121; SUB=_2A25KpseRDeRhGeVN6VIW8S_Ezz2IHXVp2kVZrDV8PUJbkNAYLUWnkW1NTF7Pc0Bg0WWSZboG4Ki8AMKh-y826sKy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh69xCU.ySiq8_sl-X_XuZ85JpX5KMhUgL.Foe0eo5NeK2RSh22dJLoI0YLxK-LBKqL1KqLxKMLBozLB.-LxKML1-eL1-qLxKML1-2L1hBLxKqL1-eL1h.LxK-LBo5LB.-LxK-LBoMLBoBt"
    cookie= "SCF=Ao1AVwBuJ9CE_L0as8l8h1zgtLNKDYFk9zhc-ywerB0HOav1628GZIL6njIQQO7P7Bm4cV-BCBju33JOPCF2eSQ.; SINAGLOBAL=3442491573124.1777.1737208502693; ALF=1741350949; SUB=_2A25Kpyt1DeRhGeVN6VIW8S_Ezz2IHXVp3SK9rDV8PUJbkNANLXKmkW1NTF7Pc4NVJCccHsBULw4IwKmoeFjESJhX; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh69xCU.ySiq8_sl-X_XuZ85JpX5KMhUgL.Foe0eo5NeK2RSh22dJLoI0YLxK-LBKqL1KqLxKMLBozLB.-LxKML1-eL1-qLxKML1-2L1hBLxKqL1-eL1h.LxK-LBo5LB.-LxK-LBoMLBoBt; _s_tentry=weibo.com; Apache=2122641620077.6633.1738759355224; ULV=1738759355237:2:1:1:2122641620077.6633.1738759355224:1737208502694"
    get_wb_hot(cookie)
    
    
   
