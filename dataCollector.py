#! /usr/bin/env python3.9
# -*- coding : utf8 -*-

import os
import sys
from threading import currentThread
import requests
from xml.etree.ElementTree import ElementTree, fromstring
from decorators import timer
from pathlib import Path
from time import sleep
from pprint import pprint
import re

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

MDR_XML = "https://www.mdr.de/nachrichten/podcast/kekule-corona/kompass-104-avBundle.xml"

REGEX = r"^<li class\=\"css.*$"
"""
//*[@id="content"]/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div[1]/h4[1]/a

XPATH to max-count

regex = <li class\=\"cssDownload hasNoRessort \"\n>\n<a href=\"(.*)\"

#mdr größer 119 -folge- in der url bis 137

"""

def _loading(current:int, total:int, status:str=""):
    bar_length = 80
    filled_length = int(round(bar_length* current/ float(total)))

    percents = round((100 * current + 1) / float(total), 1)

    bar = "=" * filled_length + ">" + " " * (bar_length -filled_length)

    sys.stdout.write("\r[%s] %s%s ... %s\r" % (bar, percents, "%", status))
    sys.stdout.flush()

def _load_and_decode_mdr_XML(mdr_xml_url: str) -> str:
    data = ""
    try:
        result = requests.get(mdr_xml_url)
        if result.status_code != requests.codes.ok:
            raise ConnectionError
        data = result.content.decode("utf8")
    except Exception as e:
        print("Something went wrong :",e)
    finally:
        return data

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

def _find_links(data:str,regex_statement:str,rel_postition_to_regex:int=0) -> list[str]:
    data_list = data.split('\n')
    links = []
    for i, line in enumerate(data_list):
        if re.search(REGEX,line):
            link = data_list[i+rel_postition_to_regex].split("\"")[1]
            link = "https://www.mdr.de"+link
            links.append(link)
    return links

def parse_mdr_xml(mdr_xml:str) -> list[str]:
    tree = ElementTree(fromstring(mdr_xml))
    root = tree.getroot()
    max_count = int(root[-4].text)
    links = []
    for i, avDocument in enumerate(root[-2].iter("avDocument")):
        links.append(avDocument.find("htmlUrl").text)
    return links

def _flatten_list(not_flat_list:list[list[str]]) -> list[str]:
    return [item for sublist in not_flat_list for item in sublist]

@timer
def check_folder_structure():
    Path(RAW).mkdir(parents=True,exist_ok=True)
    Path(os.path.join(RAW,'mdr')).mkdir(parents=True,exist_ok=True)
    Path(os.path.join(RAW,'ndr')).mkdir(parents=True,exist_ok=True)

def create_download_list_mdr() -> list[str]:
    print(">> loading XML from mdr")
    data = _load_and_decode_mdr_XML(MDR_XML)
    print(">> extract data from mdr-xml")
    links = parse_mdr_xml(data)
    total_links = len(links)
    subsite_links = []
    file_links = []
    for i,link in enumerate(links):
        _loading(i,total_links,status="getting subsite links")
        result = requests.get(link)
        temp_links = _find_links(result.content.decode("utf8"),regex_statement=r"^<li class\=\"css.*$",rel_postition_to_regex=2)
        if temp_links == []:
            continue
        else:
            subsite_links.append(temp_links)
        sleep(0.1)
    print("")
    
    subsite_links = _flatten_list(subsite_links)

    total_links = len(subsite_links)

    for i,link in enumerate(subsite_links):
        _loading(i,total_links,status="getting download links")
        result = requests.get(link)
        data = result.content.decode("utf8").split("\n")
        for i, line in enumerate(data):
            if re.search(r"<span class=\"linkText\">",line):
                if i >= 1:
                    temp_link = "https://www.mdr.de"+data[i-1].split("\"")[1]
                    file_links.append(temp_link)
    
    print("")
        
    return file_links

def create_download_list_mdr_OLD(n:int=184):
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
    print(">> creating link list")
    for i in range(100,(89*2)+1,2):
        _loading(i//2,89,status="adding links to ndr list")
        link_list.append("https://www.ndr.de/nachrichten/info/coronaskript"+str(i)+".pdf")
    #pprint(link_list)
    return link_list


def request_every_link(link_list,folder_name:str,keep_name:bool=True):
    for i,element in enumerate(link_list):
        _loading(i,len(link_list),status="downloading "+folder_name)
        try:
            element = str(element)
        except TypeError:
            print(f"Element : {element} is not type castable to str")
            break
        name = element.split("/")[-1]
        #print(f"> downloading {name}")
        try:
            result = requests.get(element)
        except ConnectionError:
            print("connection error")
        sleep(.3)
        if keep_name:
            with open(os.path.join(os.path.join(RAW,folder_name),element.split("/")[-1]),"wb") as f:
                f.write(result.content)
        else:
            with open(os.path.join(os.path.join(RAW,folder_name),str(i)+"."+element.split("/")[-1].split(".")[-1]),"wb") as f:
                f.write(result.content)
    return True

@timer
def main():
    print(">  checking for correct folder structure")
    check_folder_structure()
    print(">  done!")
    print(">  MDR")
    mdr_download_list = create_download_list_mdr()
    print(">> download files from MDR")
    request_every_link(mdr_download_list,"mdr",keep_name=False)
    print(">> done!")
    print(">  NDR")
    ndr_download_list = create_download_list_ndr()
    print(">> download files from NDR")
    request_every_link(ndr_download_list,"ndr",keep_name=False)
    print(">> done!")
    print(">  all done!")

if __name__ == "__main__":
    main()

