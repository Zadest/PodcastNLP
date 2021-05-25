#! /usr/bin/env python3.9
# -*- coding : utf8 -*-

import os
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

def _find_links(data:str) -> list[str]:
    data_list = data.split('\n')
    links = []
    for i, line in enumerate(data_list):
        if re.search(REGEX,line):
            link = data_list[i+2].split("\"")[1]
            link = "https://www.mdr.de"+link
            #print(link)
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
    data = _load_and_decode_mdr_XML(MDR_XML)
    links = parse_mdr_xml(data)
    subsite_links = []
    file_links = []
    for link in links:
        result = requests.get(link)
        temp_links = _find_links(result.content.decode("utf8"))
        if temp_links == []:
            continue
        else:
            subsite_links.append(temp_links)
        sleep(0.1)
    subsite_links = _flatten_list(subsite_links)

    for link in subsite_links:
        result = requests.get(link)
        data = result.content.decode("utf8").split("\n")
        for i, line in enumerate(data):
            if re.search(r"<span class=\"linkText\">",line):
                if i >= 1:
                    temp_link = "https://www.mdr.de"+data[i-1].split("\"")[1]
                    file_links.append(temp_link)
        
    return file_links

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

#def check_byte_size():


@timer
def main():
    check_folder_structure()

    mdr_download_list = create_download_list_mdr()
    request_every_link(mdr_download_list[1:],"mdr")

    ndr_download_list = create_download_list_ndr()
    request_every_link(ndr_download_list,"ndr")

if __name__ == "__main__":
    main()

