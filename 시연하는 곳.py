# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 17:21:23 2017

@author: acorn
"""
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



weather=["aa","bb","cc","dd","ee","ff","gg","hh","ii","jj",
         "kk","mm","ll","nn","oo","pp","qq","rr","ss","tt"]
dic={"aa":aaa,"bb":bbb,"cc":ccc,"dd":ddd,"ee":eee,"ff":fff,"gg":ggg,"hh":hhh,"ii":iii,
     "jj":jjj,"kk":kkk,"ll":lll,"mm":mmm,"nn":nnn,"oo":ooo,"pp":ppp,"qq":qqq,"rr":rrr,
     "ss":sss,"tt":ttt}

def question():
    number=int(input("몇 개 물어 볼꺼야?"))
    for i in range(1,number+1):
        question=print("{}번째 질문".format(i) )
        answer=input(question)
        output=''.join(predict([answer,'']))
        for a in weather :
            if output.find(a) > -1 :
                output=output.replace(a,dic[a])
        if answer.find("어") > -1:
            start=answer.find("어")   
            end=answer.find("의")
            word1=answer[start+2:end]
            word2=dictionary(word1)
            dic2={"zz":word1,"yy":word2}
            output=output.replace("zz",dic2("zz")).replace("yy",dic2["yy"])
        print("A: " + output)
        

       
c="단어 ace의 뜻을 알려줘!"
c[start+2:end]   
question()
def dictionary(word) :
    main_news= "http://endic.naver.com/search.nhn?sLn=kr&isOnlyViewEE=N&query="+word
    page = requests.get(main_news)
    page.status_code
    soup = BeautifulSoup(page.text,'html.parser')
    content=soup.find("div",{"class":"align_right"})
    aa=content.find_all("span")
    b=str(aa)
    ########### <>안에 있는 것들 다 제거하기
    k=re.sub('<.*?>',"",b)
    index=k.find("더보기")
    word2=k[:index-7].replace("[","").replace("]","")
    return word2

dictionary()
