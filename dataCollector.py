#! /usr/bin/env python3.9
# -*- coding : utf8 -*-

import os
import requests
from sklearn.cluster import cluster_optics_dbscan
from decorators import timer
from pathlib import Path
from time import sleep
from pprint import pprint

URL = "https://www.mdr.de/nachrichten/podcast/kekule-corona/"
DATA = os.path.join(os.getcwd(),'data')
RAW = os.path.join(DATA,'RAW')

FILENAME_PREFIX = "kekule-corona-kompass-"
FILENAME_POSTFIX = "-100-downloadFile.pdf"

EINERNAMEN = ("",
            "ein",
            "zwei",
            "drei",
            "vier",
            "fuenf",
            "sechs",
            "sieben",
            "acht",
            "neun")

ZEHNERNAMEN = ("",
            "",
            "zwanzig",
            "dreissig",
            "vierzig",
            "fuenfzig",
            "sechzig",
            "siebzig",
            "achtzig",
            "neunzig")
"""
//*[@id="content"]/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div[1]/h4[1]/a

XPATH to max-count

#mdr größer 119 -folge- in der url bis 137

"""
def _int_to_written_number(index: int):
    if index >= 100:
        hunderter = index // 100
        _,zehner,einer,zehner_einer_text = _int_to_written_number(index % 100)
        text = EINERNAMEN[hunderter]+"hundert"+zehner_einer_text if zehner_einer_text else EINERNAMEN[hunderter]+"hundert"
        return hunderter, zehner, einer, text

    if index >= 20:
        zehner = index // 10
        einer = index % 10
        text = EINERNAMEN[einer]+"und"+ZEHNERNAMEN[zehner] if einer != 0 else ZEHNERNAMEN[zehner]
        return 0, zehner, einer, text

    if index >= 13:
        einer = index % 10
        return 0,1,einer,EINERNAMEN[einer]+"zehn"

    if index == 12:
        return 0,1,2,"zwoelf"

    if index == 11:
        return 0,1,1,"elf"

    if index == 10:
        return 0,1,0,"zehn"

    if index > 1:
        return 0,0,index,EINERNAMEN[index]

    if index == 1:
        return 0,0,1,"eins"

    return None, None, None, None

#dreissig
#einhundertneunundsechzig

@timer
def check_folder_structure():
    Path(RAW).mkdir(parents=True,exist_ok=True)
    Path(os.path.join(RAW,'mdr')).mkdir(parents=True,exist_ok=True)
    Path(os.path.join(RAW,'ndr')).mkdir(parents=True,exist_ok=True)
    
def create_dowload_list_mdr(n:int=184):
    link_list_to_pdfs = [""]
    for i in range(64,n+1):
        _,_,_,i_to_str = _int_to_written_number(i)
        if i <= 119:
            link = "https://www.mdr.de/nachrichten/podcast/kekule_folge_"+i_to_str+FILENAME_POSTFIX
        elif i <= 136:
            link = URL+FILENAME_PREFIX+"folge-"+i_to_str+FILENAME_POSTFIX
        else:
            link = URL+FILENAME_PREFIX+i_to_str+FILENAME_POSTFIX
        link_list_to_pdfs.append(link)
    pprint(link_list_to_pdfs)
    return link_list_to_pdfs

def create_download_list_ndr(n:int=89):
    link_list = []
    for i in range(100,(89*2)+1,2):
        link_list.append("https://www.ndr.de/nachrichten/info/coronaskript"+str(i)+".pdf")
    pprint(link_list)
    return link_list


def request_every_link(link_list,folder_name:str):
    for i,element in enumerate(link_list):
        try:
            element = str(element)
        except TypeError:
            print(f"Element : {element} is not type castable to str")
            break
        name = element.split("/")[-1]
        print(f"> downloading {name}")
        try:
            result = requests.get(element)
        except ConnectionError:
            print("connection error")
        sleep(.3)
        with open(os.path.join(os.path.join(RAW,folder_name),element.split("/")[-1]),"wb") as f:
            f.write(result.content)
    return True

@timer
def main():
    check_folder_structure()
    
    mdr_download_list = create_dowload_list_mdr()
    request_every_link(mdr_download_list[1:],"mdr")

    ndr_download_list = create_download_list_ndr()
    request_every_link(ndr_download_list,"ndr")

if __name__ == "__main__":
    main()

