import sys
import os
from time import sleep
import requests
from pathlib import Path

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

def _loading(current:int, total:int, status:str=""):
    bar_length = 60

    filled_length = int(round(bar_length* current/ float(total)))

    percents = round((100 * current + 1) / float(total), 1)

    bar = "=" * filled_length + ">" + " " * (bar_length -filled_length)
    if len(status)> 32:
        status = status[0:64]
    sys.stdout.write("\r[%s] %s%s > %s\r" % (bar, percents, "%", status))
    sys.stdout.flush()

def _flatten_list(not_flat_list:list[list[str]]) -> list[str]:
    return [item for sublist in not_flat_list for item in sublist]

def request_every_link(link_list,root: str,folder_name:str,keep_name:bool=True, verbose:bool=False):
    full_path = os.path.join(root,folder_name)
    Path(full_path).mkdir(parents=True,exist_ok=True)
    for i,element in enumerate(link_list):
        _loading(i,len(link_list),status="downloading "+folder_name)
        try:
            element = str(element)
        except TypeError:
            print(f"Element : {element} is not type castable to str")
            break
        name = element.split("/")[-1]
        if verbose:
            _loading(i+1, len(link_list),status=f"> downloading {name}")
        try:
            result = requests.get(element)
        except ConnectionError:
            print("connection error")
        sleep(.1)
        if keep_name:
            with open(os.path.join(full_path,element.split("/")[-1]),"wb") as f:
                f.write(result.content)
        else:
            with open(os.path.join(full_path,str(i)+"."+element.split("/")[-1].split(".")[-1]),"wb") as f:
                f.write(result.content)
    return True

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