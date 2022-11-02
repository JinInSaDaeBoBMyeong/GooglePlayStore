from SCRIPT.crawler import *
from SCRIPT.download import *
from SCRIPT.count import *
from SCRIPT.crawler_v2 import *
import os

if   __name__=="__main__":
    PWD = os.getcwd()
    os.system("git clone https://github.com/89z/googleplay.git")
    download_list=[]
    
    ##crawler
    country = input("INPUT YOUR COUNTRY : ")
    download = input("DOWNLOAD : ")
    print(f"[*]Please, wait for 4 hour :) - traveling to {country}")
    File_name,tmp_list = crawler(country, download)
    
    ##crawler_v2
    tmp_list= crawler_v2(country, download)
    
    print("[*]Crawling is Done\n\n")
    
    ##download
    for index, value in enumerate(tmp_list):
        tmp = input(f"{value} is need for download?(O/X)\n>")
        if tmp=='O':
            download_list.append(value)
            
    download_script(File_name,download_list,PWD)
    
    os.chdir(PWD)
    ##count
    cnt = print_list(File_name)
    print(f"Valid Count : {len(cnt)}")
    
