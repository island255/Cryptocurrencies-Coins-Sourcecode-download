head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

import requests
import time
import re
import os

class getInformation(object):
    def getNameAndLink(self):
        f=open("catalogue.csv","r")
        f.readline()
        self.SourceCodeLink=[]
        self.Names=[]
        for line in f.readlines():
            attrs=line.strip().strip(",").split(",")
            if(len(attrs)==4):
                self.Names.append(attrs[0])
                self.SourceCodeLink.append(attrs[3])
            else:
                continue
        f.close()
    def getInfor(self):
        if(os.path.exists("GitOne")==False):
            os.mkdir("GitOne")
        if(os.path.exists("GitMany")==False):
            os.mkdir("GitMany")
        if(os.path.exists("Bitbucket")==False):
            os.mkdir("Bitbucket")
        self.errorfile=open("error.csv","a")
        for i in range(len(self.Names)):
            print("第"+str(i+1)+"个："+self.SourceCodeLink[i])
            try:
                if("github" in self.SourceCodeLink[i]):
                    r=self.getHTML(self.SourceCodeLink[i])
                    if(r==None):
                        self.errorfile.write(self.Names[i]+","+self.SourceCodeLink[i]+"\n")
                        continue
                    else:
                        if(re.findall(r'href=".+?.zip"',r.text)==[]):
                            self.forGitMany(r,i)
                        else:
                            self.forGitOne(r,i)
                else:
                    r=self.getHTML((self.SourceCodeLink[i]).replace("src/","downloads"))
                    if(r==None):
                        self.errorfile.write(self.Names[i]+","+self.SourceCodeLink[i]+"\n")
                        continue
                    else:
                        self.forBitbucket(r,i)
            except:
                i=i-1
                continue
        self.errorfile.close()
    def getHTML(self,url):
        r=requests.get(url,head)
        counter=0
        while(r.status_code!=200):
            if(counter>10):
                return None
            time.sleep(2)
            r=requests.get(url,head)
            counter+=1
        return r
    def forGitOne(self,r,i):
        f=open("GitOne/NameAndLink.csv","a")
        f.write(self.Names[i]+","+self.SourceCodeLink[i]+"\n")
        f.close()
    def forGitMany(self,r,i):
        f=open("GitMany/NameAndLink.csv","a")
        f.write(self.Names[i]+","+self.SourceCodeLink[i]+"\n")
        f.close()
    def forBitbucket(self,r,i):
        f=open("Bitbucket/NameAndLink.csv","a")
        f.write(self.Names[i]+","+self.SourceCodeLink[i]+"\n")
        f.close()
def main():
    g=getInformation()
    g.getNameAndLink()
    g.getInfor()
if __name__=="__main__":
    main()