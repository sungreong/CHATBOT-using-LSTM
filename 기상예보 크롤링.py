# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:41:06 2017

@author: acorn
"""
#### https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/
###############################################################################
###############################################################################
######## 관련사이트 https://www.dataquest.io/blog/web-scraping-tutorial-python/
########          https://developer.mozilla.org/en-US/docs/Web/HTML/Element
###############################################################################
### request 요청 객체 (html) + Beautiful soup 파싱객체 
### 태그 파싱할때는 상위 태그를 찾고 하위 태그 탐색 
import requests
from bs4 import BeautifulSoup
import re
### 주소에 ? 는 웹브라우저와 동일하게 한다.

##  http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168

################################## 대기정보  ###############################
URL = "http://weather.naver.com/air/airFcast.nhn"
page = requests.get(URL)
page.request
page.close
page.cookies
page.status_code ### 성고하면 200 오류나면 400 500
page.headers 
page.text  
page.content

soup = BeautifulSoup(page.text,'html.parser')
content=soup.find(id="content") #find 한개만 출력한다. 

## 원하는 id class 를 탐색 전체를 찾을 떄는 find_all
# html id name class 3개로 구분
## id name - tag로 구분 // css selector : class등으로 구분  
environ=content.find(class_='data')
## class 
len(environ)  # 
type(environ) # bs4 형식으로 출력된다. # reslutset
####### 한글인 것만 크롤링하기 

hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
result = hangul.sub('', str(environ))


###################### 생활정보   ##################################
URL = "http://weather.naver.com/life/lifeNdx.nhn?cityRgnCd=CT001000"
page = requests.get(URL)
page.status_code

soup = BeautifulSoup(page.text,'html.parser')
content=soup.find(id="content") #find 한개만 출력한다. 
################# 한개만 있는것을 목포료 추출하낟.



## class 
len(environ)  # 
type(environ) # bs4 형식으로 출력된다. # reslutset
######################################## 한글인 것만 크롤링하기 

####### title 가져오기 
ti=content.find_all('img')
title=[]
for en in ti :
    ti2 = re.compile('[^ ㄱ-ㅣ가-힣]+')
    ti2 = ti2.sub('', str(en)).strip(" ")
    title.append(ti2)

######## content
environ=content.find_all(class_='txt')
content3=[]
for en in environ:
    content2 = re.compile('[^ ㄱ-ㅣ가-힣]+')
    content2 = content2.sub('', str(en)).strip(" ")
    content3.append(content2)
####### 지수 
environ=content.find_all('dd')
number=[]
for en in environ:
    num= re.compile('[^ 0-9]+')
    num = num.sub('', str(en)).strip(" ")
    number.append(num)
number
######### 앞에 3개 통합시켜서 생활정보 출력 
life_info=[]
for i in range(0,len(content3)) :
    k=title[i]+" "+content3[i]+" "+number[i]+"점"
    life_info.append(k)
    
    
########## 동네별 날씨 
import pandas as pd

URL = "http://weather.naver.com/rgn/townWetr.nhn"
page = requests.get(URL)
page.status_code
soup = BeautifulSoup(page.text,'html.parser')
content=soup.find("dl")
sub=content.find_all("dt")
sub2=re.compile('[^ ㄱ-ㅣ가-힣 | \,]+')
sub2=sub2.sub('',str(sub)).strip(" ").replace("  "," ").split(",").strip(" ")
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
    e=sub2[i]+" (수치) "+ab[i]
    town_weather.append(e)
    
URL="http://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09350621"
URL="http://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09350104"
page = requests.get(URL)
page.status_code
soup = BeautifulSoup(page.text,'html.parser')
############### 오늘날씨  #############
a=soup.find("div",{"class":"fl"})
time=a.find('h5')
str(time).replace("<h5><span>","").replace("</span>","").replace("</h5>","")
temp2=a.find('em')
temp3 = re.compile('[^ ㄱ-ㅣ가-힣 | 0-9 ]+')
temp4=temp3.sub(' ',str(temp2)).strip(" ").split(" ")
temp=temp4[1]+" "+temp4[0]+"℃"
rain=a.find('p')
rain.find_all("span")
temp3 = re.compile('[^ㄱ-ㅣ가-힣|0-9|\+|\-|\.]+')
temp4=temp3.sub(' ',str(rain))
temp5=temp4.strip(" ").replace("  "," ")
end1=str(temp5).find("|")
temp=temp5[:end1-3]+"℃"
rainfall=temp5[end1+2:end1+9]+"%"
start=str(temp5).find("미")
ozone=temp5[start:].replace("도움말","").strip(" ")
today=temp+" , "+rainfall+" , "+ozone
today
######## 주간 예보 미래의 오전 오후 기상 예보 

import numpy as np
URL = "http://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=15210510"
page = requests.get(URL)
page.status_code
soup = BeautifulSoup(page.text,'html.parser')
content=soup.find("table",{"class" : "tbl_weather tbl_today4"})
 
day=content.find_all(scope="row")
timetemp=content.find_all(class_="nm")
info=content.find_all(class_="info")
### day 2개씩 만들기
day2 = re.compile('[^ ㄱ-ㅣ가-힣]+')
day2 = day2.sub('', str(day)).strip(" ").replace("  "," ").split(" ")
day=np.array(day2)
day=np.repeat(day,[2]*len(day),axis=0)
day
### timetemp
temp = re.compile('[^ ㄱ-ㅣ가-힣 | 0-9 | \.]+')
timetemp2=temp.sub('',str(timetemp)).strip(" ").replace("  "," ").replace("   "," ").split("  ")
htemp=[]
for i in range(0,len(timetemp2)) :
    a=timetemp2[i]+"℃"
    htemp.append(a)
htemp
#### info
info3=str(info).replace("</li>","").replace('<li class="info">',"").replace("[","").replace("]","").split(" ")

week_forecast=[]
for i in range(0,len(day)):
    a=day[i]+" : "+htemp[i]+", 날씨 상태 : "+info3[i]
    week_forecast.append(a)
week_forecast
str(week_forecast)
['주말날씨',str(week_forecast)]
import datetime
i = datetime.datetime.now()
today2=" %s-%s-%s" % (i.year, i.month, i.day)
today=input("오늘은 %s 입니다. 어떤게 궁금한가요?" %(today2))
day =input("언제 %s 가 궁금한가요?  형식은 yyyymmdd 로 표기해주세요" %(today))
news= "http://weather.naver.com/news/wetrNewsList.nhn?ymd="+day
news


#### 메인 뉴스 가져오기 
URL = "http://weather.naver.com/news/wetrNewsList.nhn?ymd=20170904"
page = requests.get(URL)
page.status_code
soup = BeautifulSoup(page.text,'html.parser')
content=soup.find("div",{"id":"content_sub"})
main_adrress=content.find("dt").find("a").get('href')
page = requests.get(main_adrress)
page.status_code
soup = BeautifulSoup(page.text,'html.parser')
content=soup.find("div",{"id":"articleBodyContents"})
type(content)
num=str(content).find("</script>")
numend=str(content).find("<!-- // 본문 내용 -->")
news = re.compile('[^ ㄱ-ㅣ가-힣]+')
main_news=news.sub('',str(content)[num:numend]).replace("  "," ")




## 이미지 태그를 만들떄는 2가지 정보를 입력
## 이미지 보이거나 이미지가 보이지 않을 떄 표현하는 정보
img= tonight.find('img')
########## 안에 2가지 정보가 있을 때 
img
type(img)
img['alt']
#img 객체는 python의 dictionary와 같이 태그의 속성들을 저장한다. 
#따라서 title.get('속성이름')나 title['속성이름']처럼 이용할 수 있다.
desc=img['title']
img.get('title')
type(desc)
print(desc)

### find 는 tag에 이용  아니면 select 는 :CSS 
# tag  구분하는것 id , name  id는 고유이름이기 떄문에 중복 불가
## name 서버측에서 태그를 구분하는 것이기 떄문에 중복가능
## check box 여러개 선택 
### CSS 문법
### css 여러군데 적용가능하기 떄문에 중독가능성

period_tags=seven_day.select(".tombstone-container .period-name") 
type(period_tags) # list 형식에서는 get_text 안된다.
type(period_tags[0]) # bs4 tag 같은 경우 get_text() 가능
periods=[pt.get_text() for pt in period_tags]
periods
type(periods)
seven_day.select(".tombstone-container")
short_descs=[sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps=[t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs=[d['title'] for d in seven_day.select(".tombstone-container img")]

print(short_descs)
print(temps)
print(descs)

import pandas as pd 
weather = pd.DataFrame({
        "period" : periods,
        "short_desc" : short_descs,
        "temp" : temps,
        "desc" : descs
        })
print(weather)
type(weather['temp'])
#?P 가 들어 오면 컬럼이름으로 사용 그 값은 d+ 숫자 : 정규식표현
weather.temp
temp_nums=weather["temp"].str.extract("(?P<temp_이름>\d+)",expand=False)
temp_nums  # ?P 로 이름이 들어간다 
weather['temp-num']=temp_nums.astype('int')
temp_nums
weather['temp-num'].mean()
is_night=weather['temp'].str.contains('Low')
weather['is_night']=is_night
weather[is_night]
weather.temp
type(weather.temp)
weather["temp"].str.extract("(:*)",expand=False) 
weather["temp"].str.extract("([a-zA-z ]+)",expand=False) # 문자 추출 
weather["temp"].str.extract("(\w+)",expand=False) # 문자 추출 
weather["temp"].str.extract("(\W+)",expand=False) # 문자 숫자 아닌것과 매치
weather["temp"].str.extract("(\S+)",expand=False) # 문자 추출 
weather["temp"].str.extract("(\D+)",expand=False) # 문자 추출 
weather["temp"].str.extract("([^0-9]*)",expand=False) # 문자 추출 
########## 문제 네이버 첫 페이지에서 로또 회차와 당첨번호를 확인하시오 
k=pd.Series(['매매 bb.12.cc'])
k.str.extract(" (\w*) ")
k.str.extract("(\w+) ")
k.str.extract("(\w+)")
k.str.extract("(.*|\d+)")
k.str.extract("(.*?) ")
page = requests.get("http://www.nlotto.co.kr/gameResult.do?method=byWin&drwNo=764")
page.status_code  # 200은 성공 400 500 은  오류 
page.content ### HTML content of the page
page.text
soup=BeautifulSoup(page.text,'html.parser')
print(soup.prettify())
list(soup.children)
[type(item) for item in list(soup.children)] 

page = requests.get("http://www.nlotto.co.kr/gameResult.do?method=byWin&drwNo=764")
soup=BeautifulSoup(page.text,'html.parser')
soup.prettify()
k=soup.find("meta",{"id":"desc"})
type(k)
k['content']
k.get('content')


line = str(soup.find("meta", {"id" : "desc", "name" : "description"})['content'])
print(line)
type(line)
begin = line.find("당첨번호")
begin = line.find(" ", begin) + 1
end = line.find(".", begin)
numbers = line[begin:end]
print("당첨번호: " + numbers)

######### javascript 로 동적 출력
import requests
import pandas as pd 
from bs4 import BeautifulSoup
 ###################### 태그속성확인 할수 있음 class 인것을 암  여기선 하나만 있어서 하나만 암
soup = BeautifulSoup('<abc class="blodest" name="bbb">Extremely bold</b>','html.parser')
# tag 참조 가능 
tag=soup.abc
print(type(tag))
print(tag.name)  # abc
# print(tag['id'])
print(tag.attrs)  ###  속성 2개인 것을 알수있다. 
#############################################
print(tag.text)  # tag로 받았기 때문에. text로 한다.
##get.text( ) 와 같은 역할 find 한 결과를 받을 떄 get.text()

tag['id']='verybold' ### 태그 추가하는 것
print(tag.attrs)  ### attrs이 하나더 추가된다 
tag['another-attribute']=1
print('추가된 태그 확인 \n',tag)
print(tag.attrs)  ### attrs이 하나더 추가된다 
tag['id']
#######    배열식 접근도 가능하다 
css_soup= BeautifulSoup('<p class="body strikeout" name="bbb  ccc"><p>' ,'html.parser')
css_soup.p['class']
css_soup.p['name']

#####  텍스트파싱 (정규식표현)
import re 
text = "문의사항이 있으면 032-2-2-3245 으로 연락주시기 바랍니다."
regex = re.compile(r'\d\d\d-\d-\d-\d\d\d\d')
matchobj=regex.search(text)
phonenumber=matchobj.group()
print(phonenumber)

regex=re.compile(r'\d+') #d+ 패턴1개이상 숫자 #d* 0개이상 
matchobj2=regex.search(text)
phonenumber2=matchobj2.group()
phonenumber2


regex=re.compile(r'-\d+') #d+ 패턴1개이상 숫자 #d* 0개이상 
matchobj2=regex.search(text)
phonenumber2=matchobj2.group()
phonenumber2


regex=re.compile(r'(\d{3})-(\d{1})-(\d{1})-(\d{4})') #패턴에서 괄호는 그룹 
matchobj2=regex.search(text)
phonenumber2=matchobj2.group() ##### FULL
phonenumber2
phonenumber2=matchobj2.group(1)
phonenumber2
phonenumber2=matchobj2.group(2)
phonenumber2
phonenumber2=matchobj2.group(3)
phonenumber2
phonenumber2=matchobj2.group(4)
phonenumber2
##############################################################################
################################## 로또 사이트 당첨번호 크롤링 ###############
########### 참고사이트 http://it-diary.tistory.com/2 ########################

d=[]
def main(k): 
    basic_url = "http://www.nlotto.co.kr/gameResult.do?method=byWin&drwNo=" 
    for i in range(1, k): 
        resp = requests.get(basic_url + str(i)) 
        soup = BeautifulSoup(resp.content, 'html.parser')
        line = str(soup.find("meta", {"id" : "desc", "name" : "description"})['content']) 
        begin = line.find("당첨번호") 
        begin = line.find(" ", begin) + 1 
        end = line.find(".", begin) 
        numbers = line[begin:end] 
        begin = line.find("총") 
        begin = line.find(" ", begin) + 1
        end = line.find("명", begin)
        persons = line[begin:end] 
        begin = line.find("당첨금액") 
        begin = line.find(" ", begin) + 1 
        end = line.find("원", begin) 
        amount = line[begin:end] 
        a = {"당첨회차" : [i] ,
             "당첨번호" : [numbers],
             "당첨인원" : [persons],
             "당첨금액" : [amount]}
        k=pd.DataFrame(a)
        d.append(k)
    return d

k=main(4)
table=pd.concat(k,ignore_index=True )
table

###########################################
from bs4 import BeautifulSoup as bs 
import requests
import pandas as pd
import re
date="2017.07.14"
url_part1="""http://dart.fss.or.kr/dsac001/search.ax?selectDate="""
url_part2="""&sort=&series=&mdayCnt=0&currentPage"""
url=url_part1+date+url_part2
url
res = requests.get(url)
soup=bs(res.text,'html.parser')
res.text
res.content
print(soup.prettify())
print(soup.find_all("p")[1])
print(soup.find_all("p")[1].text)
regex=re.compile(r'(\d{3})') #d+ 패턴1개이상 숫자 #d* 0개이상 
totnum=soup.find_all("p")[1].text
match=regex.search(totnum)
ph=match.group()
ph

print(len(soup.find_all("table")))
print(soup.find_all("tr"))
print(len(soup.find_all("tr")))
print(soup.find_all("tr")[0])  # 0번쨰하고 1번째
print(soup.find_all("tr")[len(soup.find_all("tr"))-1]) # 맨마지막 꺼 출력하려면 len -1
############# 시간 빼오기  ##############
k=soup.find_all("tr")[2] ; k
print("============================")
k.find_all('td',class_="cen_txt")
print("============================")
k.find_all('td',class_="cen_txt")[0]
print("============================")
k.find_all('td',class_="cen_txt")[0].text
print("============================")
k.find_all('td',class_="cen_txt")[0].text.strip()
print("============================")
k.find("a")
k.find("a").text
k.find("a").text.strip()
#k.find("a").text.encode("utf-8")
#k.find("a").text.encode("utf-8").strip()
#str(k.find("a").text.encode("utf-8")).strip()


teststr =str(k.find_all('td')[1].find("a").get("href"))
teststr
print(re.findall(r"[0-9]{8}",teststr)[0])
k.find_all('td')
k.find_all('td')[0] # cen_txt
k.find_all('td')[1] # 
k.find_all('td')[2] #
k.find_all('td')[3]
k.find_all('td')[4]
k.find_all('td')[5]
len(k.find_all('td'))





#####  빈칸 
resultData=pd.DataFrame()
resultData=resultData.append(# 데이터 프레임 append 된다
                             {"pubTime": "","ComName":"",
                              "Cat" : "","coID":"",
                              "Content":"","reqDate":"",
                              "pubDate":"","rcpNo":""},
                              ignore_index=True)

resultData
totnum=soup.find_all("p")[1].text
match=regex.search(totnum)
totNum=match.group()
totNum=int(totNum)

i=0
totPage = int((totNum/100)+1)
for page in range(1, totPage+1):
    print (str(page))
    urlrolling = url + str(page)
    tempXML = requests.get(urlrolling)
    soup=bs(tempXML.text, 'html.parser')
    print (urlrolling)
    
    tempNumCont = len(soup.find_all("tr"))
    print (tempNumCont)
    
    
    for j in range(1, tempNumCont):
        resultData.ix[i,"pubTime"] = str(soup.find_all("tr")[j].find_all("td", class_="cen_txt")[0].text).strip()
        resultData.ix[i,"ComName"] = str(soup.find_all("tr")[j].find("a")).strip()
        resultData.ix[i,"Cat"] = str(soup.find_all("tr")[j].find_all("td")[1].find("img").get("title")).strip()
        tempStr = str(soup.find_all("tr")[j].find_all("td")[1].find("a").get("href"))
        resultData.ix[i,"coID"] = re.findall(r"[0-9]{8}",tempStr)[0]
        tempStr = str(soup.find_all("tr")[j].find_all("td")[2].find("a").text).strip()
        resultData.ix[i,"Content"] = re.sub("\r|\n|\t","",tempStr)
        resultData.ix[i,"reqDate"] = str(soup.find_all("tr")[j].find_all("td")[4].text).strip()
        resultData.ix[i,"pubDate"] = date
        tempStr = str(soup.find_all("tr")[j].find_all("td")[2].find("a").get("href"))
        resultData.ix[i, "rcpNo"] = re.findall(r"[0-9]{14}",tempStr)[0]
       
        i = i+1 
resultData
resultData.ix[1,"pubTime"]
    urlrolling = url + str(1)
    tempXML = requests.get(urlrolling)
    soup=bs(tempXML.text, 'html.parser')

######################   http://devanix.tistory.com/296  ####################
tempStr = str(soup.find_all("tr")[1].find_all("td")[2].find("a").text).strip()
re.sub("\r|\n|\t","",tempStr)
soup.find_all("tr")[1]
soup.find_all("tr")[1].find_all("td")[2].find("a").text.strip()
