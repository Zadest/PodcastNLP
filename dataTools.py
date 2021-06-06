#! /usr/bin/env python
# -*- coding: utf8 -*-

import json
import os
from pathlib import Path
from typing import Any

from utils import request_every_link

from dataCollectorNDR import get_download_files_list_ndr
from dataCollectorMDR import get_download_files_list_mdr

def safe_dict_to_json(text:dict,folder:str,filename:str):
    path = os.path.join(os.path.join("data","refined"),folder)
    Path.mkdir(path,parents=True,exist_ok=True)
    with open(filename+".json", "w") as f:
        json.dump(text,f)

def load_files(keep_name:bool=True,verbose:bool=True):
    print(">>> Starting Data Collection...")
    print(">>> MDR...")
    mdr_download_list = get_download_files_list_mdr()
    print(">>> download files from MDR...")
    request_every_link(mdr_download_list,os.path.join("data","RAW"),"mdr",keep_name=keep_name,verbose=verbose)
    print(">>> done!")
    print(">>> NDR...")
    ndr_download_list = get_download_files_list_ndr()
    print(">>> download files from NDR...")
    request_every_link(ndr_download_list,os.path.join("data","RAW"),"ndr",keep_name=keep_name,verbose=verbose)
    print(">>> done!")
    print(">>> all done!")

def iter_files(folder:str,func) -> (list[Any] or None):
    return_val = []
    files = os.listdir(folder)
    for file in files:
        print(file)
        abs_path= os.path.join(folder,file)
        if os.path.isfile(abs_path):
            return_val.append(func(abs_path))
    return return_val or None

if __name__ == "__main__":
    load_files()