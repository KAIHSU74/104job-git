import requests,bs4
from requests_html import HTMLSession
import re
import time
import random
import configparser
from fake_useragent import UserAgent
from db import *
ua = UserAgent()
headers = {'User-Agent':ua.random}
import db
# 取得地區編號
def get_city_code():
    url = 'https://www.104.com.tw/public/function01/utf8/jsonArea.js?v=200323'
    r = requests.get(url, headers=headers)
    objsoup = bs4.BeautifulSoup(r.text, 'lxml')
    area = re.findall('"des":"(\w+)","no":"(\d+)"', objsoup.text)
    city_dict = {}
    for i in area:
        city_dict[i[0]] = i[1]
    return city_dict 

# 取得職缺總頁數
def get_pageNumber(keyword, city_code):
    url = "https://www.104.com.tw/jobs/search/?ro=0"+'&isnew='+str(update_time)+"&kwop=7&keyword="+str(keyword)+"&jobcatExpansionType=0&area="+str(city_code)
    r = requests.get(url, headers=headers)
    objSoup = bs4.BeautifulSoup(r.text, 'lxml')
    pagesNumber = re.search('"totalPage":(\d+)', objSoup.text).group().split(':')[1]
    return pagesNumber

# 取得每一頁每筆職務資訊，存入資料庫
def get_page(keyword, pageNumber):
    for p in range(int(pageNumber)):
        url = 'https://www.104.com.tw/jobs/search/?ro=0'+'&isnew='+str(update_time)+'&kwop=7&keyword='+str(keyword)+'&jobcatExpansionType=0&area='+str(city_code)+\
        '&order=15&asc=0&page='+str(p+1)+'&mode=s&jobsource=2018indexpoc'
        r = requests.get(url, headers=headers)
        objSoup = bs4.BeautifulSoup(r.text, 'lxml')
        jobs = objSoup.find_all('article', class_='js-job-item')
        temp_dict = {}
        for job in jobs:
            try:      
                info_dict = None
                # 更新時間
                temp_dict['job_time'] = job.find('span', class_="b-tit__date").text.strip()
                # 公司名稱
                temp_dict['company_name'] = job['data-cust-name']
                # 職缺名稱
                temp_dict['job_name'] = job['data-job-name']
                job_intro = job.find('ul',class_ = 'job-list-intro')
                job_list_intro = job_intro.find_all('li')
                # 職務所在地區
                temp_dict['job_area'] = job_list_intro[0].text
                # 工作經驗
                temp_dict['job_years'] = job_list_intro[1].text
                # 學歷
                temp_dict['education'] = job_list_intro[2].text
                # # 工作內容簡述
                temp_dict['job_describe'] = job.find('p').text.replace('\r\n','').replace('\n','')
                list_tag = job.find('div', class_='job-list-tag b-content')
                # 職務薪資 公司類型 員工人數等資訊
                temp_dict['job_info'] = list_tag.text.strip().replace('\n','/')
                # 職務連結網址
                temp_dict['job_104url'] = 'https:'+ job.find('h2', class_='b-tit').find('a')['href']
                temp_dict['job_id'] = temp_dict['job_104url'].split('?')[0].split('/')[-1]
                info_dict = temp_dict
                if info_dict:
                    insert_db(info_dict)        
            except Exception as e:
                print(e)
                time.sleep(3)
     

if __name__=='__main__':
    cf = configparser.ConfigParser()
    cf.read('104job.conf', encoding='utf8')                     # 讀取設定檔
    keyword = str(cf.get('104job','keyword')).split(',')        # 關鍵字
    city = str(cf.get('104job', 'city')).split(',')             # 搜尋地區
    update_time = str(cf.get('104job', 'update_time'))          # 職務更新時間
    for c in city:
        city_code = get_city_code()[c]                          # 地區編號
        for k in keyword:
            pageNumber = get_pageNumber(k, city_code)
            get_page(k, pageNumber)
        