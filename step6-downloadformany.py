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

flag=0

for i in range(len(Names)):

    if(os.path.exists("code/release-many/"+Names[i])==False):
        os.mkdir("code/release-many/"+Names[i])
    name=Links[i].strip('/').split('/')[-1]
    if(os.path.exists("code/release-many/"+Names[i]+"/"+name)==False):
        os.mkdir("code/release-many/"+Names[i]+"/"+name)  
    f1=open("code/release-many/"+Names[i]+"/"+name+"/catalogue.csv","wb")  

    tagLinks=Links[i]+"/tags"
    path="code/release-many/"+Names[i]+"/"+name+"/"
    r=requests.get(tagLinks,head)
    while(1):
        if(flag==1):
            break
        flag = 0
        print("第"+str(i+1)+"个:"+Names[i])
        try:
            r=requests.get(tagLinks,head)
            
            iota=0
            if(r.status_code==404):
                print("no download link")
                flag=1
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
        for ul in uls:
            li=ul.li
            releasetime=li.contents[-2].string.strip()
            releasetime=releasetime.replace(',','')
            # print(releasetime.replace(',',''))
            # f.write(time+",")
            link=GitHub+ul.contents[5].a.attrs["href"]
            # f.write(link+",")
            subname=link.strip('/').split('/')[-1]
            print(subname)
            # f.write(subname+"\n")
            text=releasetime+','+link+','+subname+'\n'
            # print(text)
            # print(type(text))
            f1.write(text.encode('ascii'))
            try:
                if(os.path.exists(path+subname)==False):
                    r=requests.get(link,head)
                    iota=0
                    while(r.status_code!=200):
                        iota=iota+1
                        time.sleep(5)
                        r=requests.get(link.strip(),head)
                        if(iota>=10):
                            print("no web")
                            continue
                    f=open(path+subname,"ab")
                    f.write(r.content)
                    f.close()
                    azip=zipfile.ZipFile(path+subname)
                    azip.close() 
                    # time.sleep(2)  
            except:
                print("download error")
                         

        next= soup.find("a",string="Next")
        if(next == None):
            break
        else:
            tagLinks=next["href"]
        time.sleep(5)
    f1.close()


        
