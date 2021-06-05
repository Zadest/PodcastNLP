#! /usr/bin/env python
# -*- coding: utf8 -*-

############### dataCollectorMDR.py

# for downloading / webscraping
import requests
from time import sleep

# for searching / extracting information
import re
from xml.etree.ElementTree import ElementTree, fromstring

# for utility
import os
import sys
from utils import _loading, _flatten_list,request_every_link

MDR_XML = "https://www.mdr.de/nachrichten/podcast/kekule-corona/kompass-104-avBundle.xml"
REGEX = r"^<li class\=\"css.*$" 

def _find_links(data:str,regex_statement:str,rel_postition_to_regex:int=0) -> list[str]:
    data_list = data.split('\n')
    links = []
    for i, line in enumerate(data_list):
        if re.search(regex_statement,line):
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

def _load_and_decode_mdr_XML(mdr_xml_url: str) -> str:
    data = ""
    try:
        result = requests.get(mdr_xml_url)
        if result.status_code != requests.codes.ok:
            raise ConnectionError
        data = result.content.decode("utf8")
    except Exception as e:
        print(">>> Something went wrong :\n",e)
    finally:
        return data

def get_download_files_list_mdr() -> list[str] or None:
    print(">>> loading XML from mdr...")
    data = _load_and_decode_mdr_XML(MDR_XML)
    print(">>> extract data from mdr-xml...")
    links = parse_mdr_xml(data)
    total_links = len(links)
    subsite_links = []
    file_links = []
    for i,link in enumerate(links):
        _loading(i,total_links,status="getting subsite links...")
        result = requests.get(link)
        temp_links = _find_links(result.content.decode("utf8"),regex_statement=r"^<li class\=\"css.*$",rel_postition_to_regex=2)
        if temp_links == []:
            continue
        else:
            subsite_links.append(temp_links)
        sleep(0.05)
    _loading(i+1,total_links,status="done!")
    print("")
    
    subsite_links = _flatten_list(subsite_links)

    total_links = len(subsite_links)

    for i,link in enumerate(subsite_links):
        _loading(i,total_links,status="getting download links...")
        result = requests.get(link)
        data = result.content.decode("utf8").split("\n")
        for i, line in enumerate(data):
            if re.search(r"<span class=\"linkText\">",line):
                if i >= 1:
                    temp_link = "https://www.mdr.de"+data[i-1].split("\"")[1]
                    file_links.append(temp_link)
    _loading(i+1,total_links,status="done!")
    print("")
    return file_links or None

if __name__ == "__main__":
    file_list = get_download_files_list_mdr()
    request_every_link(file_list,os.path.join("data","raw"),"mdr",verbose=True,keep_name=True)
    print("")