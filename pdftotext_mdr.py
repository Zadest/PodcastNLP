from typing import ContextManager
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
    structText = expLB.sub(r'',colonText)

    # structText = re.sub(r"\s{2,}","\n",structText)
    # time = re.compile(r"([0-9]{1,}:[0-9]{2}:[0-9]{2})|([0-9]{1,}:[0-9]{2})")
    # structText = time.sub(r"\n\1",structText)
    
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
    return time.findall(text) or None

def find_date(text):
    date = re.compile(r'([0-9]{1,2}\.\s+[\w|0-9]{1,}\s(?:2020|2021))')
    return date.findall(text) or None

def find_id(text):
    id = re.compile(r'(\#[0-9]{1,3})')
    return id.findall(text) or None

def iterateFiles(filepath,index):
    return_list = []
    for filename in os.listdir(filepath):
        path = os.path.join(filepath,filename)
        if os.path.exists(path) and path.split('.')[-1].lower() == "pdf":
            text = extrText(path)
            text = performRegEx(text)
            if os.listdir(filepath).index(filename) == 0:
                print(text)
            if len(text)> 0:
                print(f"appending {path=}")
                return_list.append(text)
        else:
            print('Datei nicht gefunden.')
    return return_list

mylist = iterateFiles(os.path.join('data','RAW','mdr'),len(os.listdir(os.path.join("data","RAW","mdr"))))


for i, episode in enumerate(mylist):
    results = re.findall(r'\n(.*\s(?:Schumann|Kröger|Kekulé))\n(.*)',episode)
    header = episode[:re.search(r'\n(.*\s(?:Schumann|Kröger|Kekulé))\n(.*)',episode).span()[0]+1]
    print(header)
    date = find_date(header) or 'None'
    id = find_id(header)
    meta = {
            'id': id,
            'source' : '',
            'title' : '',
            'date': date[0],
            'speakers' : []
        }
    speakers = []
    content = {'0' : ["None",header]}
    for j,textblock in enumerate(results,1):
        if textblock[0] not in speakers:
            speakers.append(textblock[0])
        content[str(j)] = [textblock[0],textblock[1].strip()]
    meta["speakers"] = speakers
    dump = {"metadata":meta,"content":content}
    with open(os.path.join('data','REFINED','mdr',str(i)+'.json'), 'w', encoding='utf-8') as f:
        json.dump(dump,f, ensure_ascii=False, indent=4)
