#! /usr/bin/env python
#coding=utf-8
# 定时抓取城市 aqi 数据
# http://pm25.in
    
import json
import time, os 
import requests
import datetime
from MSSql_SqlHelp import MSSQL 

def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, timeout=120)

def parse_html_aqi(dis_aqi):
    print(len(dis_aqi))
    for x in dis_aqi:
        area = x["area"]
        time_point = x["time_point"]
        sql = "select count(id) from Space0015A where column_1='%s' and column_19='%s' " %(area,time_point)
        isRepeat = ms.ExecQuery(sql.encode('utf-8'))
        if isRepeat[0][0] == 0:
            aqi = x["aqi"]
            co = x["co"]
            co_24h = x["co_24h"]
            no2 = x["no2"]
            no2_24h = x["no2_24h"]
            o3 = x["o3"]
            o3_24h = x["o3_24h"]
            o3_8h = x["o3_8h"]
            o3_8h_24h = x["o3_8h_24h"]
            pm10 = x["pm10"]
            pm10_24h = x["pm10_24h"]
            pm2_5 = x["pm2_5"]
            pm2_5_24h = x["pm2_5_24h"]
            primary_pollutant = x["primary_pollutant"]
            quality = x["quality"]
            so2 = x["so2"]
            so2_24h = x["so2_24h"]
            level = x["level"]
            sql = "insert into Space0015A values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(aqi,area,co,co_24h,no2,no2_24h,o3,o3_24h,o3_8h,o3_8h_24h,pm10,pm10_24h,pm2_5,pm2_5_24h,quality,level,so2,so2_24h,primary_pollutant,time_point)
            ms.ExecNonQuery(sql.encode('utf-8'))


#MS Sql Server 链接字符串
ms = MSSQL(host=".",user="sa",pwd="sa",db="SmallIsBeautiful")

#每个 token 每小时最多调用 5 次，'5j1znBVAsnSf5xQyNQyq'为测试key
token = ['7rMwJqMxrmuDRFsAxBqP','5j1znBVAsnSf5xQyNQyq','K6LgqdJKZP2R9Svedskd']

def main():
    now = datetime.datetime.now()
    print("开始时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  
    try:
        dist_aqi = download_page("http://pm25.in/api/querys/aqi_ranking.json?token=7rMwJqMxrmuDRFsAxBqP").json()
        if type(dist_aqi) == dict:
            print(dist_aqi["error"])
        else:
            parse_html_aqi(dist_aqi)
    except Exception as e:
        #raise e
        print("Error：抓取返回超时")

    now = datetime.datetime.now()
    print("结束时间：" + now.strftime('%Y-%m-%d %H:%M:%S'))  


def re_exe(cmd, inc = 60): 
    while True: 
        os.system(cmd);
        print("PM25.in城市排名 抓取_Start")
        main()
        print('PM25.in城市排名 抓取_End')
        time.sleep(inc) 

# N秒 执行一次
re_exe("echo %time%", 1800)

