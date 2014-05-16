# @ black_perl(ankush sharma) 
# Grab images by fetching a url over a complex network

# @ Python 2.x.x

## importing libraries
import httplib
import base64
import sys
import urlparse
import logging

from bs4 import BeautifulSoup as bs
from urllib2 import *
'''		The urllib2 module defines functions and classes which help in opening URLs (mostly HTTP) in a complex 
	    world — basic and digest authentication, redirections, cookies and more.
'''

def proxy_connect(proxy_str,port,username,password):
  '''   Installs the opener director objectsto work over proxy network to work for the global urlopen.
  '''
  '''	urlopen function works in according to an opener director object .
  '''
  '''	Handler objects are the real workers behing fetching a request, opener director objects can be insta
  		-ntiated using the install_opener function;which manages the collection of all the handlers required for different type of requests viz. 
  		the requests using http,https and other protocol schemes.
  '''
  proxy=ProxyHandler({"http":"http://{0}:{1}@{2}:{3}".format(username,password,proxy_str,port)}) # Proxy handler object
  auth=HTTPBasicAuthHandler() # Auth handler object
  opener=build_opener(proxy,auth,HTTPHandler) # building an opener that has the power of authentication, working behind 
  # proxy and uses the HTTP protocol , this function creates an opener director object
  #install_opener(opener) # this function sets the global urlopen to use than opener redirector object  
  # we will use opener.open()
  # use logging to log 
  
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
        if ".jpg" in str(m) or ".png" in str(m) and str(parse_result[0])=="http":
           print m
           f=open("D:\\image_grabber\{}".format(str(m)),"wb")
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
    
        
