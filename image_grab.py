#---written by black_perl(ankush sharma) @ 19-08-2013------
#----currently this is in beta stage ;can retrieve only images with url scheme "http" from only "http" web sources -------
#---the best thing about is that you can use it over proxy which is the cause of above restriction ---------
#-----for using it, you have to make a folder in your local disc(here in the code i have named it as image_grabber1)---------
#--------this code is will soon be converted to it's alpha stage------------------
#--------for any queries message me at dc, nick-@dustin---------------------

import httplib
import base64
import sys
from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import *

def proxy_connect(proxy_str,port,username,password):
#we should specify the objects in yhe order we declare them in opener builder
  proxy=ProxyHandler({"http":"http://{0}:{1}@{2}:{3}".format(username,password,proxy_str,port)})
  auth=HTTPBasicAuthHandler()#needed to authenticate proxy for the username and password supplied
  opener=build_opener(proxy,auth,HTTPHandler)#it provides opening environment for urlopen/http handler for opening http type request with urlopen
  install_opener(opener)
  print "------OPENER INSTALLED----------"
  
def getpage(proxy,link,auth):
    con=httplib.HTTPConnection(proxy,80)
    con.request("GET",link,headers={"Proxy-Authorization":"Basic "+auth})
    response=con.getresponse()
    if response.status==200:
        print response.status
        print response.reason
        page=response.read()
        return page
    else:
        print "--------CONNECTION PROBLEM-----------"
        sys.exit()


def encoder(username,password):
    auth_en=str(base64.b64encode(username+":"+password))
    return auth_en

def save_html(page):
    fob=open("D:\\image_grabber\page.html","w")
    fob.write(page)
    fob.flush()
    fob.close()
    path="D:\\image_grabber\page.html"
    return path

def parser(path):
    target=[]
    file_obj=open(path,"r")
    soup=bs(file_obj)
    for image in soup.findAll("img"):
        img_file=image["src"]
        target.append(img_file)
    print target
    return target


def downloader(images):
    count=1
    for img in images:
        k=urlopen(str(img))
        parse_result=urlparse.urlparse(img)
        m=parse_result[2].split("/")[-1]
        if ".jpg" in str(m) or ".png" in str(m):
           print m
           f=open("D:\\image_grabber3\{}".format(str(m)),"wb")
           f.write(k.read())
           f.flush()
           f.close()
           print count
           count+=1
        
        
    

def main():
    print "enter proxy credentials"
    proxy_server=raw_input("enter proxy server address:")
    username=raw_input("Enter username:")
    password=raw_input("Enter password:")
    auth_enc=encoder(username,password)
    link=raw_input("Enter a link to be parsed:")
    page_str=getpage(proxy_server,link,auth_enc)
    f_path=save_html(page_str)
    target_images=parser(f_path)
    proxy_connect(proxy_server,80,username,password)
    downloader(target_images)
    print "------------------------DONE-------------------------------"
    



if __name__=="__main__":main()
    
        
