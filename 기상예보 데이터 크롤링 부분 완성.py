# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 13:17:01 2017

@author: acorn
"""

############################
#packages
import tensorflow as tf
import numpy as np
import sys
import datetime
print (sys.version)
print (tf.__version__) #1.1이상 가능
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
###########################




def main():
    print("안녕 만나서 반가워")
    a=input("뭐가 궁금하니?")
    input("아~ %s가 궁금하구나?" %(a))
    i = datetime.datetime.now()
    today2=" %s-%s-%s" % (i.year, i.month, i.day)
    input("오늘은 %s 인데, 오늘이 궁금한거지?" %(today2))
    day =input("오늘 날짜를 써줘 형식은 yyyymmdd 이야")
    print("고마워 곧 %s에 대한 메인뉴스를 가져올게" %(day))
    ### 메인뉴스 
    main_news= "http://weather.naver.com/news/wetrNewsList.nhn?ymd="+day
    page = requests.get(main_news)
    page.status_code
    soup = BeautifulSoup(page.text,'html.parser')
    content=soup.find("div",{"id":"content_sub"})
    main_adrress=content.find("dt").find("a").get('href')
    page = requests.get(main_adrress)
    page.status_code
    soup = BeautifulSoup(page.text,'html.parser')
    content=soup.find("div",{"id":"articleBodyContents"})
    num=str(content).find("</script>")
    numend=str(content).find("<!-- // 본문 내용 -->")
    news = re.compile('[^ ㄱ-ㅣ가-힣]+')
    main_news2=news.sub('',str(content)[num:numend]).replace("  "," ").strip(" ")
    main_news=['메인뉴스',main_news2]
    print("오늘의 메인 뉴스야!!"," ",main_news)
    ##### 원하는 지역 
    which=input("메인 뉴스는 보여줬고 원하는 구 있어? 아 근데! 서울특별시 쪽만 물어봐 줄래?ㅎ")
    print("아 '%s' 라고 생각하는구나 고마워 지금 알아볼게" %(which))
    f = open("주소록.txt", 'r')
    data=f.readlines()
    k=[]
    for i in range(0,len(data)):
        a=(data[i].replace("\n","").split(" "))
        k.append(a)
    address = [{x[0] : x[1] for x in k}]
    a=[]
    for k in address[0].keys():
        a.append(k)
    f = open("서울특별시_구.txt", 'r')
    gu_data=f.read().splitlines() 
    print("서울 특별시 구에 대한 정보야"," ",gu_data)
    gu=input("원하는 구가 어디야?")
    gu2=[]
    for bb in a :
        if bb.find(gu) >1:
            gu2.append(bb)
    print("%s동 데이터야 %s" %(gu,gu2) )
    dong=input("원하는 동이 어디야?")
    dong2=[]
    for bb in a :
        if bb.find(dong) >1 :
            dong2.append(bb)
    dong2[0]
    print("이 %s이 궁금하구나!" %(dong2[0]))
    URL="http://weather.naver.com/rgn/townWetr.nhn?naverRgnCd="+address[0][dong2[0]]
    page = requests.get(URL)
    page.status_code
    soup = BeautifulSoup(page.text,'html.parser')
    # 원하는 구 오늘 날씨 상태
    current=soup.find("div",{"class":"fl"})
    time=current.find('h5')
    ###
    time=str(time).replace("<h5><span>","").replace("</span>","").replace("</h5>","")
    #time=['현재시간을 알려줘',time]
    temp2=current.find('em')
    temp3 = re.compile('[^ ㄱ-ㅣ가-힣 | 0-9 ]+')
    temp4=temp3.sub(' ',str(temp2)).strip(" ").split(" ")
    temp_1=temp4[1]+" "+temp4[0]+"℃"
    temper=temp_1
    rain=current.find('p')
    rain.find_all("span")
    temp3 = re.compile('[^ㄱ-ㅣ가-힣|0-9|\+|\-|\.]+')
    temp4=temp3.sub(' ',str(rain))
    temp5=temp4.strip(" ").replace("  "," ")
    end1=str(temp5).find("|")
    temp_2=temp5[:end1-3]+"℃"
    ###
    temp_change=temp_2
    ###
    rainfall=temp5[end1+2:end1+9]+"%"
    start=str(temp5).find("미")
    ozone=temp5[start:].replace("도움말","").strip(" ")
    ###
    dust_ozone=ozone
    content=soup.find("dl")
    sub=content.find_all("dt")
    sub2=re.compile('[^ ㄱ-ㅣ가-힣 | \,]+')
    sub2=sub2.sub('',str(sub)).replace("  "," ").split(",")
    k=content.find_all("span")
    str(k).replace("<span>","").replace("</span>","")
    dd=re.compile('[^0-9  | \. | \~ ]').sub('', str(k)).replace("/","").replace("  "," ")
    dd=dd.split(" ")
    dd[0]=dd[0]+"㎍/㎥"
    dd
    ab=[]
    for i in range(0,len(dd),2):
        word=dd[i]+' <'+ dd[i+1] +'>'
        ab.append(word)
    town_weather=[]
    for i in range(0,len(sub2)):
        e=sub2[i]+"수치는"+ab[i]
        town_weather.append(e)
    ###
    dust_number=town_weather[0]
    ###
    ozone_number=town_weather[1]
    ###
    total_number=town_weather[2]
    print("%s 현재 날씨 대기 상태 데이터를 가져왔어" %(dong2[0]))
    print("다음은 %s 주간 날씨 데이터를 가져올게" %(dong2[0]))
    content=soup.find("table",{"class" : "tbl_weather tbl_today4"})
    day=content.find_all(scope="row")
    ### day 2개씩 만들기
    day2 = re.compile('[^ ㄱ-ㅣ가-힣]+')
    day2 = day2.sub('', str(day)).strip(" ").replace("  "," ").split(" ")
    day=np.array(day2)
    day=np.repeat(day,[2]*len(day),axis=0)
    hh=soup.find_all("ul",{"class":"text"})
    temp = re.compile('[^ ㄱ-ㅣ가-힣 | 0-9 | \.]+')
    week_today=temp.sub('',str(hh)).strip(" ").replace("  "," ").replace("   "," ").split("  ")
    tomo_week=week_today[2:]
    index=tomo_week[0].find('.')
    ###
    tomo_morning=tomo_week[0][0:index+2]+"℃"+" "+tomo_week[0][index+3:]+"%"
    ###
    tomo_afternoon=tomo_week[1][0:index+2]+"℃"+" "+tomo_week[1][index+3:]+"%"
    tomo_weekday=tomo_week[2:]
    day3=[]
    for a in tomo_weekday :
        a=a[0:index+2]+"℃"+" "+a[index+3:]
        day3.append(a)
    final=[]
    for i in range(0,len(day3)):
        s=day[i]+" "+day3[i]
        final.append(s)
    later_two_morn=final[0]
    later_two_after=final[1]
    later_thr_morn=final[2]
    later_thr_after=final[3]
    later_fou_morn=final[4]
    later_fou_after=final[5]
    later_five_morn=final[6]
    later_five_after=final[7]
    later_six_morn=final[8]
    later_six_after=final[9]
    print("주간 날씨 데이터도 가져 왔어")
    return time, temper, temp_change , rainfall , dust_ozone ,dust_number, ozone_number,total_number,tomo_morning,tomo_afternoon,later_two_morn,later_two_after,later_thr_morn,later_thr_after,later_fou_morn,later_fou_after,later_five_morn,later_five_after,later_six_morn,later_six_after

data=main()
aaa=data[0]
bbb=data[1]
ccc=data[2]
ddd=data[3]
eee=data[4]
fff=data[5]
ggg=data[6]
hhh=data[7]
iii=data[8]
jjj=data[9]
kkk=data[10]
lll=data[11]
mmm=data[12]
nnn=data[13]
ooo=data[14]
ppp=data[15]
qqq=data[16]
rrr=data[17]
sss=data[18]
ttt=data[19]
