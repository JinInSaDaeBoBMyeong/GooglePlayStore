import os

def print_list(name):
    PATH = f".\\DataSet\\{name.split('.')[0]}"
    download_list = os.listdir(PATH)

    for i,j in enumerate(download_list):
        download_list[i] = j.split("-")[0]

    return set(download_list)