from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def crawler(country,download):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Head-less 설정, 브라우저를 열지 않음
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('.\\SCRIPT\\chromedriver.exe', options=options)
    driver.get(url=f"https://play.google.com/store/apps?hl={country}")      #나라 설정

    pre_link = "https://play.google.com/store/apps/details?id="

    ##해당 페이지에서 href인것 다 찾기("/store.apps/details?id="이 담긴 것)
    links = driver.find_elements(By.XPATH,'//a[contains(@href,"/store/apps/details?id=")]')
    for i,_ in enumerate(links):
        links[i] = links[i].get_attribute('href')+"&hl="+country              #나라 설정
    links = list(set(links))

    seq =[]

    cnt = 0
    cnt_init = len(links)

    for link in links:
        print("[*]"+link.split('?id=')[1].split('&')[0]+" is doing")
        try:
            cnt+=1
            if cnt_init==cnt:
                print("[*]You can input Ctrl+C anytime you want!!:)")
            driver.get(url=link)
            
            #Download 수 파악
            try:
                cnt_down = driver.find_elements(By.XPATH,f'//div[text()="{download}"]')
                target = cnt_down[0].find_elements(By.XPATH,"..")
                seq.append(target[0].text.split("\n")[0])
            except:
                seq.append("None")

        
            #수집
            tmp = driver.find_elements(By.XPATH,'//a[contains(@href,"/store/apps/details?id=")]')
            for i,_ in enumerate(tmp):
                tmp[i] = tmp[i].get_attribute('href')+"&hl="+country          #나라 설정
                
            for j in tmp:
                if j not in links:
                    links.append(j)
        except:
            print("[*]ERROR IS IN "+link)
            break

    df = {
        'package_name':[],
        'cnt_download':[],
    }

    for i,_ in enumerate(seq):
        df['package_name'].append(links[i].split("?id=")[1].split("&")[0])
        df['cnt_download'].append(seq[i])  


    df = pd.DataFrame.from_dict(df)
    df.to_csv(f".\\RESULT\\{country}_googlestore.csv",index=None, encoding="utf-8")   #나라

    download_list = set(seq)
    
    return f"{country}_googlestore.csv",download_list




