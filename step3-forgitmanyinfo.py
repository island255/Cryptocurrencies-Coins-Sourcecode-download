import requests
from bs4 import BeautifulSoup
import time

head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

f=open("GitMany/NameAndLink.csv","r")
Names=[]
Links=[]

for line in f.readlines():
    temp=line.strip().split(",")
    Names.append(temp[0])
    Links.append(temp[1])
f.close()
f=open("GitMany/Languages.csv","w")
f.write("Coin,Pinned Repositories,Description,Language\n")
counter=0
for i in range(len(Names)):
    counter+=1
    print("第"+str(counter)+"个:"+Names[i])
    r=requests.get(Links[i],head)
    while(r.status_code!=200):
        time.sleep(10)
        r=requests.get(Links[i],head)
    soup=BeautifulSoup(r.text,"html.parser")
    divs=soup.findAll("div",{"class":"pinned-repo-item-content"})
    for div in divs:
        f.write(Names[i]+",")
        title=div.find("span",{"class":"repo js-repo"})
        f.write(title.string.replace(",",".")+",")
        desc=div.find("p",{"class":"pinned-repo-desc text-gray text-small d-block mt-2 mb-3"})
        try:
            f.write(desc.string.replace(",",".").strip()+",")
        except TypeError:
            f.write("None"+",")
        except AttributeError:
            f.write("None"+",")
        try:
            langu=div.find("span",{"class":"repo-language-color pinned-repo-meta"}).next_sibling.strip()
            f.write(langu.replace(",",".").strip()+"\n")
        except AttributeError:
            f.write("None\n")
f.close()