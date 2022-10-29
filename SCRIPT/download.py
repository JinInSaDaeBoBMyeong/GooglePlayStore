import os
import subprocess
import pandas as pd

def download_script(name,download_cnt,PWD):
    os.chdir(".\\googleplay\\cmd\\googleplay")
    os.system("go build")
    
    df = pd.read_csv(PWD+f"\\RESULT\\{name}",index_col=None)
    google_start = PWD+"\\googleplay\\cmd\\googleplay\\googleplay.exe"
    
    os.chdir(PWD)
    #DataSet
    email = input("Input your Email :")
    passwd = input("Input your passwd : ")
    os.system(f"{google_start} -email {email} -password {passwd}")
    os.system(f"{google_start} -device")
    
    ##폴더 만들고 다음 폴더에 파일 넣는 형태
    try:
        os.mkdir(f".\\DataSet\\{name.split('.')[0]}")
    except:
        None
    os.chdir(f".\\DataSet\\{name.split('.')[0]}")
    
    count =0

    for index,value in enumerate(df['package_name']):
        if df['cnt_download'][index] not in download_cnt:
            continue        
        count+=1
        try:
            if count %7==0:
                os.system(f"{google_start} -device")
            print(f"[*]Processing with {value}\n")

            #getting apk version
            os.system(f"{google_start} -a {value}")
            result = subprocess.Popen(f"{google_start} -a {value}",stdout=subprocess.PIPE)
            out = result.stdout.read().decode('utf-8')
            print(out)
            tmp = out.rfind("Version Code: ")
            Version_Code= out[tmp:].split('\n')[0].split(": ")[1]

            #Purchase apk
            os.system(f"{google_start} -a {value} -purchase")

            #Bring apk
            os.system(f"{google_start} -a {value} -v {Version_Code}")
        except:
            print(f"\t[-]fail...!! for {value}")
