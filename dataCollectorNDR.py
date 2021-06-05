#! /usr/bin/env python
# -*- coding: utf8 -*-

############### dataCollectorNDR.py

# for downloading / webscraping
import requests
from time import sleep

# for searching / extracting information
import re

# for utility
import os
import sys
from utils import _loading, request_every_link

#
NDR_URL = "https://www.ndr.de/nachrichten/info/Coronavirus-Update-Die-Podcast-Folgen-als-Skript,podcastcoronavirus102.html"
NDR_ROOT = "https://www.ndr.de"

## extraction of file names and location form website
def get_download_files_list_ndr() -> list[str] or None:
    return_values = []
    try:
        result = requests.get(NDR_URL)
        if result.status_code != requests.codes.ok:
            raise ConnectionError
        data = result.content.decode("utf8").split('\n')
        for item in data:
            if re.search(r"<a href=\"/nachrichten/info/coronaskript\d*.pdf",item):
                return_values.append(str(NDR_ROOT+item.split("\"")[1]))
    except ConnectionError as ce:
        print("Something went wrong! (Connection)")
        print(ce)
    finally:
        return return_values or None
    
## downloading all files and renaming them if wanted
def download_files_from_root(root:str,files:list[str],folder:str,keep_name:bool=True, verbose:bool=False):
    for i,element in enumerate(files):
        try:
            element = str(element)
        except TypeError:
            print(f"Element : {element} is not type castable to str")
            break
        name = element.split("/")[-1]
        if verbose:
            _loading(i, len(files),status=f"> downloading {name}")
        try:
            result = requests.get(root+element)
        except ConnectionError:
            print("connection error")
        sleep(.1)
        if keep_name:
            with open(os.path.join(os.path.join("data","RAW",folder),element.split("/")[-1]),"wb") as f:
                f.write(result.content)
        else:
            with open(os.path.join(os.path.join("data","RAW",folder),str(i)+"."+element.split("/")[-1].split(".")[-1]),"wb") as f:
                f.write(result.content)
    if verbose:
        _loading(i+1, len(files),status=f"> downloading {name}")
    print("\n")

if __name__ == "__main__":
    file_list = get_download_files_list_ndr()
    request_every_link(file_list,os.path.join("data","raw"),"ndr",verbose=True,keep_name=True)