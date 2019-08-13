import requests
from bs4 import BeautifulSoup
import zipfile
import time
import os

head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
GitHub="https://github.com"



f=open("coinlink.csv","r")
Names=[]
Links=[]

for line in f.readlines():
    temp=line.strip().split(",")
    Names.append(temp[0])
    Links.append(temp[1])
f.close()

if(os.path.exists("code/release-0")==False):
    os.mkdir("code/release-0")
if(os.path.exists("code/release-many")==False):
    os.mkdir("code/release-many")

releases_0=open("code/release-0/catalogue.csv",'w')
releases_many=open("code/release-many/catalogue.csv",'w')


for i in range(len(Names)):
    r=requests.get(Links[i],head)
    while(r.status_code!=200):
        time.sleep(10)
        r=requests.get(Links[i],head)

    releasesnumber=0
    soup=BeautifulSoup(r.text,"html.parser")
    spans=soup.findAll("span",{"class":"num text-emphasized"})
    if(spans!=[]):
        releasesnumber=spans[2].text.strip()

    if(releasesnumber=="0" or releasesnumber=="1" ):
        print("0 "+Names[i])
        
        releases_0.write(Names[i]+",")
        releases_0.write(Links[i]+"\n")
    else:
        print("num:"+str(i)+" "+Names[i])
        
        releases_many.write(Names[i]+",")
        releases_many.write(Links[i]+"\n")

releases_0.close()
releases_many.close()



        







