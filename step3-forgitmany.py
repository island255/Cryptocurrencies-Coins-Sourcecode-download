import requests
from bs4 import BeautifulSoup
import time

head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
GitHub="https://github.com"


f=open("GitMany/NameAndLink.csv","r")
Names=[]
Links=[]

for line in f.readlines():
    temp=line.strip().split(",")
    Names.append(temp[0])
    Links.append(temp[1])
f.close()

counter=0
f=open("GitMany/soucecodelinks.csv","w")
f.write("Coin,SourceCodeLink\n")
for i in range(len(Names)):
    counter+=1
    print("第"+str(counter)+"个:"+Names[i])
    r=requests.get(Links[i],head)
    while(r.status_code!=200):
        time.sleep(10)
        r=requests.get(Links[i],head)
    soup=BeautifulSoup(r.text,"html.parser")
    divs=soup.findAll("div",{"class":"pinned-repo-item-content"})
    if(divs!=[]):
        for div in divs:
            f.write(Names[i]+",")
            title=div.find("span",{"class":"repo js-repo"})
            f.write(Links[i].strip('/')+"/"+title.string.replace(",",".")+"\n")
    else:
        divs=soup.findAll("div",{"class":"d-inline-block mb-1"})
        num=0
        for div in divs:
            if(num<3):
                # print(Names[i])
                f.write(Names[i]+",")
                title=div.a.attrs["href"]
                f.write(GitHub+title+"\n")
                num=num+1


f.close()