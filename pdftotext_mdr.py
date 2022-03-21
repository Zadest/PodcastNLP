from nltk.tokenize import word_tokenize
from decorators import timer
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

    expDS = re.compile(r' +')
    structText = expDS.sub(r' ',structText)
    # structText = re.sub(r"\s{2,}","\n",structText)
    # time = re.compile(r"([0-9]{1,}:[0-9]{2}:[0-9]{2})|([0-9]{1,}:[0-9]{2})")
    # structText = time.sub(r"\n\1",structText)
    
    # Unterteilung nach Redner
    expCS = re.compile(r"\s(Camillo Schumann|CAMILLO SCHUMANN|Camillo Schuhmann|CAMILLIO SCHUHMANN)[\s|\:]")
    expJK = re.compile(r"\s(Jan Kröger|Jan Krüger|Jan Christian Kröger|JAN KRÖGER|JAN CHRISTIAN KRÖGER)[\s|\:]")
    expAK = re.compile(r"\s(Alexander Kekulé|ALEXANDER KEKULÉ)[\s|\:]")
    expTD = re.compile(r"\s(Tim Deisinger|TIM DEISINGERF)[\s|\:]")
    expSM = re.compile(r"\s(Stefanie Markert|STEFANIE MARKERT)[\s|\:]")
    cs = expCS.sub(r"\nCamillo Schumann\n",structText)
    jk = expJK.sub(r"\nJan Kröger\n",cs)
    ak = expAK.sub(r"\nAlexander Kekulé\n",jk)
    td = expTD.sub(r'\nTim Deisinger\n',ak)
    sm = expSM.sub(r'\nStefanie Markert\n',td)
    errata = re.sub(r'(Jan Krüger)','Jan Kröger',sm)
    speakertransformed = errata
    return speakertransformed

def refine_Header(text):
    return_text = re.sub(r'Jan Christian Kröger,','Jan Kröger',text)
    return_text = re.sub(r'Prof\. Dr\. med\. Dr\. rer\. nat\. Alexander S\. Kekulé','Alexander Kekulé',return_text)
    return return_text

def find_time(text):
    time = re.compile(r"(([0-9]{1,}:[0-9]{2}:[0-9]{2})|([0-9]{1,}:[0-9]{2}))")
    return time.findall(text) or None

def find_date(text):
    date = re.compile(r'([0-9]{1,2}\.\s*[\w|0-9]{1,}\s(?:2020|2021))')
    date1 = re.compile(r'(\d*\.\d*\.\d*)')
    return date.findall(text) or date1.findall(text)

def find_id(text):
    id = re.compile(r'(\#[0-9]{1,3})')
    return id.findall(text) or re.findall(r'(Folge\s[0-9]{2,3})',text)

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
    results = re.findall(r'\n(.*\s(?:Schumann|Kröger|Kekulé|Deisinger|Markert))\n(.*)',episode)
    header = episode[:re.search(r'\n(.*\s(?:Schumann|Kröger|Kekulé|Deisinger|Markert))\n(.*)',episode).span()[0]+1]
    #print(f'{header=}')
    date = find_date(header)
    id = find_id(header) or ['-1']
    if id[0] == 'Folge 82':
        continue
    meta = {
            'id': id[0],
            'source' : '',
            'title' : '',
            'date': date[0],
            'speakers' : []
        }
    speakers = list(set(re.findall(r'(Alexander Kekulé|Camillo Schumann|Jan Kröger|Tim Deisinger|Stefanie Markert)',refine_Header(header))))
    #print(speakers)
    content = {'0' : ["None",header]}
    for j,textblock in enumerate(results,1):
        if textblock[0] not in speakers:
            print(" ".join([content[str(j-1)][1],results[j-1][0],results[j-1][1]]))
            print(f'{id=}',f'\n{textblock=}',f'\n{speakers=}','\n\n')
            content[str(j-1)][1] = " ".join([content[str(j-1)][1],results[j-1][0],results[j-1][1]])
            continue
        content[str(j)] = [textblock[0],textblock[1].strip()]
    meta["speakers"] = speakers
    dump = {"metadata":meta,"content":content}
    with open(os.path.join('data','REFINED','mdr',str(i)+'.json'), 'w', encoding='utf-8') as f:
        json.dump(dump,f, ensure_ascii=False, indent=4)

