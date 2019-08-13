from bs4 import BeautifulSoup
import requests
import time

url="https://coinmarketcap.com/coins/views/all/"
head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
r=requests.get(url,head)

while(r.status_code!=200):
    r=requests.get(url,head)
soup=BeautifulSoup(r.text,"html.parser")

results1=soup.findAll("span",{"class":"currency-symbol"})
results2=soup.findAll("a",{"class":"currency-name-container"})

f=open("catalogue.csv","w")
f.write("Name,Symble,Link,SourceCodeLink\n")

for i in range(len(results1)):
    f.write(results2[i].string+","+results1[i].a.string+",")
    f.write("https://coinmarketcap.com"+results1[i].a.attrs["href"])
    r=requests.get("https://coinmarketcap.com"+results1[i].a.attrs["href"],head)
    print(str(i)+":https://coinmarketcap.com"+results1[i].a.attrs["href"])
    while(r.status_code!=200):
        time.sleep(2)
        r=requests.get("https://coinmarketcap.com"+results1[i].a.attrs["href"],head)
    soup=BeautifulSoup(r.text,"html.parser")
    a=soup.findAll("a",text="Source Code")
    for link in a:
        f.write(","+link.attrs["href"])
    f.write("\n")
f.close()