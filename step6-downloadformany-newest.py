import requests
from bs4 import BeautifulSoup
import time
import zipfile
import os
import re
from pprint import pprint

head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
GitHub="https://github.com"

f=open("code/release-many/catalogue.csv","r")
Names=[]
Links=[]

for line in f.readlines():
    temp=line.strip().split(",")
    Names.append(temp[0])
    Links.append(temp[1])
f.close()


textlist=[]


for i in range(len(Names)):

    if(os.path.exists("code/release-many-latest/"+Names[i])==False):
        os.mkdir("code/release-many-latest/"+Names[i])
    name=Links[i].strip('/').split('/')[-1]
    # print(name)
    # if(os.path.exists("code/release-many-latest/"+Names[i]+"/"+name)==False):
    #     os.mkdir("code/release-many-latest/"+Names[i]+"/"+name)  
    # f1=open("code/release-many-latest/"+Names[i]+"/"+name+"/catalogue.csv","wb")  

    tagLinks=Links[i]+"/tags"
    path="code/release-many-latest/"+Names[i]+"/"
    r=requests.get(tagLinks,head)
    
    print("第"+str(i)+"个:"+Names[i])
    try:
        r=requests.get(tagLinks,head)
            
        iota=0
        if(r.status_code==404):
            print("no download link")
            continue
        while(r.status_code!=200):
            iota=iota+1
            time.sleep(5)
            r=requests.get(tagLinks,head)
            if(iota>=10):
                print("too many loops")
                break      
    except:
        print("web error")
        continue
            
    soup=BeautifulSoup(r.text,"html.parser")
    uls=soup.findAll("ul",{"class","list-style-none f6"})
    if(uls!=[]):
        ul=uls[0]
        li=ul.li
        # releasetime=li.contents[-2].string.strip()
        # releasetime=releasetime.replace(',','')
        
        link=GitHub+ul.contents[5].a.attrs["href"]
        
        # subname=link.strip('/').split('/')[-1]
        # print(subname)
            
        # text=releasetime+','+link+','+subname+'\n'
            
        # f1.write(text.encode('ascii'))
        try:
            print(path+name+".zip")
            if(os.path.exists(path+name+".zip")==False):
                r=requests.get(link,head)
                iota=0
                while(r.status_code!=200):
                    iota=iota+1
                    time.sleep(5)
                    r=requests.get(link.strip(),head)
                    if(iota>=10):
                        print("no web")
                        continue
                f=open(path+name+".zip","ab")
                f.write(r.content)
                f.close()
                azip=zipfile.ZipFile(path+name+".zip")
                azip.close() 
                # time.sleep(2)  
        except:
            print("download error")

    time.sleep(2)
    # f1.close()


        
