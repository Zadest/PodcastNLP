from nltk.tokenize import word_tokenize
from decorators import timer
import PyPDF2 as pdf
import re as re
import os

import json

from PyPDF2 import PdfFileReader as reader

def extrText(fileName):
    r = reader(fileName)
    numPages =  r.getNumPages()
    text = ''
    for i in range(numPages):
        page = r.getPage(i)
        text = text + page.extractText()
    return text

def performRegEx(text):
    # Bindestrich entfernen
    expColon = re.compile(r"([a-z])(?:-\n)([a-z])")
    colonText = expColon.sub(r'\1\2',text)

    # Zeilenumsprung entfernen
    expLB = re.compile(r'\n')
    lbText = expLB.sub(r'',colonText)

    structText = re.sub(r"\s{2,}","\n",lbText)
    time = re.compile(r"([0-9]{1,}:[0-9]{2}:[0-9]{2})|([0-9]{1,}:[0-9]{2})")
    structText = time.sub(r"\n\1",structText)
    # Unterteilung nach Redner
    expCS = re.compile(r"\s(Camillo Schumann|CAMILLO SCHUMANN)[\s|\:]")
    expJK = re.compile(r"\s(Jan Kröger|Jan Christian Kröger|JAN KRÖGER|JAN CHRISTIAN KRÖGER)[\s|\:]")
    expAK = re.compile(r"\s(Alexander Kekulé|ALEXANDER KEKULÉ|Prof\. Dr\. med\. Dr\. rer\. nat\. Alexander S\. Kekulé)[\s|\:]")
    cs = expCS.sub(r"\nCamillo Schumann\n",structText)
    jk = expJK.sub(r"\nJan Kröger\n",cs)
    ak = expAK.sub(r"\nAlexander Kekulé\n",jk)
    speakertransformed = ak
    return speakertransformed


def find_time(text):
    time = re.compile(r"(([0-9]{1,}:[0-9]{2}:[0-9]{2})|([0-9]{1,}:[0-9]{2}))")
    return time.findall(text)

def find_date(text):
    date = re.compile(r"([0-9]{1,}\..+\d{4})\s")
    return date.findall(text)

def iterateFiles(filepath,index):
    return_list = []
    for filename in os.listdir(filepath):
        path = os.path.join(filepath,filename)
        if os.path.exists(path) and path.split('.')[-1].lower() == "pdf":
            text = extrText(path)
            text = performRegEx(text)
            if len(text)> 0:
                print(f"appending {path=}")
                return_list.append(text)
        else:
            print('Datei nicht gefunden.')
    return return_list

mylist = iterateFiles(os.path.join('data','RAW','mdr'),len(os.listdir(os.path.join("data","RAW","mdr"))))

"""all_podcasts = {}
for podcast_count in range(len(mylist)):
    working_text = mylist[podcast_count].split('\n')
    episode = {}
    for i in range(len(working_text)-1):
        if len(working_text[i].split(" ")) < 3:
            episode[str(i//2)] = [working_text[i],working_text[i+1]]
    all_podcasts[str(podcast_count)] = episode

for key in all_podcasts:
    with open(os.path.join("data","refined","mdr",key+".json"), "w", encoding="utf-8") as f:
        json.dump(all_podcasts[key],f,indent=4, ensure_ascii=False)"""

'''for key in all_podcasts["1"]:
    for part in all_podcasts["1"][key]:
        if part == "Camillo Schumann": 
            print(all_podcasts["1"][key]) '''