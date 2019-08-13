import requests
from bs4 import BeautifulSoup
import time
import zipfile
import os
import re

head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
GitHub="https://github.com"

f=open("code/release-0/catalogue.csv","r")
Names=[]
Links=[]

for line in f.readlines():
    temp=line.strip().split(",")
    Names.append(temp[0])
    Links.append(temp[1])
f.close()

counter=0
for i in range(len(Names)):
    counter+=1
    if(os.path.exists("code/release-0/"+Names[i])==False):
        os.mkdir("code/release-0/"+Names[i])
    # try:
    Names[i]=Names[i].strip(".")
    try:
        print("第"+str(counter)+"个:"+Names[i])
        r=requests.get(Links[i],head) 
        
        iota=0
        if(r.status_code==404):
            print("no download link")
            continue
        while(r.status_code!=200):
            iota=iota+1
            time.sleep(10)
            r=requests.get(Links[i],head)
            if(iota>=80):
                print("too many loops")
                break
        soup=BeautifulSoup(r.text,"html.parser")
        # print(soup)    
        hrefs=soup.findAll("a",string = re.compile("Download ZIP"))
        # print(hrefs)
        if(hrefs==[]):
            continue
        link=GitHub + hrefs[0].attrs["href"]
        # print("ok")
        path="code/release-0/"+Names[i]+"/"
        name=Links[i].strip('/').split('/')[-1]     
        print(name)  
        if(os.path.exists(path+name+".zip")==False):
            r=requests.get(link,head)
            iota=0
            while(r.status_code!=200):
                iota=iota+1
                time.sleep(2)
                r=requests.get(link.strip(),head)
                if(iota>=20):
                    print("no web")
                    continue
            f=open(path+name+".zip","ab")
            f.write(r.content)
            f.close()
            azip=zipfile.ZipFile(path+name+".zip")
            azip.close()
    except:
        print("ERROR1")
        continue

        
