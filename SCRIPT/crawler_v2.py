from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import time

def crawler_v2(country,download):
    #크롤러 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('.\\SCRIPT\\chromedriver.exe', options=options)
    
    df = pd.read_csv(f".\RESULT\{country}_googlestore.csv") 
    df = df.to_dict('list')
    
    #이전 크롤링에서 정보 가져오기
    links = df['package_name']
    seq = df['cnt_download']
    pre_link = "https://play.google.com/store/apps/details?id="
    
    #검색 기반인데, 전부 검색하면 시간이 다수 걸려 일부만 진행    
    before_links= links[:-100]
    after_links = links[-100:]

    before_cnt = len(before_links)
    for index,value in enumerate(after_links):
        try:
            print(f"[+{index}]{value} is doing - {len(links)}개")
            
            #검색 기반 진행도중에 crash가 터지는 경우가 다수 존재하여 예외문 처리하였습니다.
            try:
                driver.get(url=f"https://play.google.com/store/search?q={value}&hl={country}&c=apps")
            except:
                driver.close()
                print("ERROR IS OCCURED")
                driver = webdriver.Chrome('.\\SCRIPT\\chromedriver.exe', options=options) ##경로 Googleplay로 수정해야함
                driver.get(url=f"https://play.google.com/store/search?q={value}&hl={country}&c=apps")
                
            
            #스크롤 진행하여 수집
            scroll = 0
            while driver.execute_script("return document.body.scrollHeight")!=scroll:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                scroll = driver.execute_script("return document.body.scrollHeight")
                time.sleep(1.5)
                
            tmp = driver.find_elements(By.XPATH,'//a[contains(@href,"/store/apps/details?id=")]')
            for i,_ in enumerate(tmp):
                tmp[i] = tmp[i].get_attribute('href') 
            tmp_1=[]
            
            
            #이전 다운로드 수('seq')의 개수를 일정 넘으면, 새로운 link(package명)에 대해 들어가는 것으로 판단하여 다운로드 수 수집
            if len(seq) <= before_cnt+index:
                print("[*]You can input Ctrl+C anytime you want!!:)")
                driver.get(url=pre_link+value+"&hl="+country)
                try:
                    cnt_down = driver.find_elements(By.XPATH,f'//div[text()="{download}"]')
                    target = cnt_down[0].find_elements(By.XPATH,"..")
                    seq.append(target[0].text.split("\n")[0])
                except:
                    seq.append("None")
                    
                tmp_1 =list(driver.find_elements(By.XPATH,'//a[contains(@href,"/store/apps/details?id=")]'))
                for i,_ in enumerate(tmp_1):
                    tmp_1[i] = tmp_1[i].get_attribute('href')
            
            #넣을 데이터
            for j in set(tmp+tmp_1):
                j = j.split("?id=")[1]
                if j not in links:
                    links.append(j)
                    after_links.append(j)
                    
        except KeyboardInterrupt:
            print("KeyboardInterrupt exception is caught")
            break
        except Exception as e:
            print('Error',e)
            break
    try:
        driver.close()
    except:
        None

    num_seq = len(seq)
    
    df['package_name'] = links[:num_seq]
    df['cnt_download'] = seq
    
    df = pd.DataFrame.from_dict(df)
    df.to_csv(f".\\RESULT\\{country}_googlestore.csv",index=None, encoding="utf-8") #경로 수정
    
    return set(seq)
    #다운로드