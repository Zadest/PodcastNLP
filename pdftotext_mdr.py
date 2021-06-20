from nltk.tokenize import word_tokenize
from .decorators import timer
import PyPDF2 as pdf
import re as re
import os

import json

from PyPDF2 import PdfFileReader as reader

def importFile(fileName):
    r = reader(fileName)
    fileInfo = r.getDocumentInfo()
    pageLayout = r.getPageLayout()
    pageNum = r.getNumPages()
    print(fileInfo,pageLayout,pageNum,sep='\n')

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
    expColon = re.compile("(?:[a-z])(-\n)")
    colonText = expColon.sub('',text)

    print(re.search(r"\n[A-Z]*\n",text))
    # Zeilenumsprung entfernen
    expLB = re.compile('\n')
    lbText = expLB.sub('',colonText)
    # Bindestrich einfügen. Fehler TODO
    # expLB = re.compile('[a-z][A-Z]')
    # lbText = expLB.sub('[a-z]-[A-Z]',colonText)
    # Unterteilung nach Redner
    expCS = re.compile("\sCamillo Schumann\s")
    expJK = re.compile("\sJan Kröger\s")
    expAK = re.compile("\sAlexander Kekulé\s|\sProf. Dr. med. Dr. rer. nat. Alexander S. Kekulé\s")
    cs = expCS.sub("\nCamillo Schumann\n",lbText)
    jk = expJK.sub("\nJan Kröger\n",cs)
    ak = expAK.sub("\nAlexander Kekulé\n",jk)
    speakertransformed = ak
    return speakertransformed

def iterateFiles(filepath,index):
    return_list = []
    for filename in os.listdir(filepath):
        path = os.path.join(filepath,filename)
        if os.path.exists(path) and path.split('.')[-1].lower() == "pdf":
            text = extrText(path)
            #print(performRegEx(text))
            return_list.append(performRegEx(text))
        else:
            print('Datei nicht gefunden.')
    return return_list

mylist = iterateFiles(os.path.join('data','RAW','mdr'),127)

all_podcasts = {}
for podcast_count in range(len(mylist)):
    working_text = mylist[podcast_count].split('\n')
    episode = {}
    for i in range(len(working_text)-1):
        if len(working_text[i].split(" ")) < 3:
            episode[str(i)] = [working_text[i],working_text[i+1]]
    all_podcasts[str(podcast_count)] = episode

for key in all_podcasts:
    with open(os.path.join("data","refined","mdr",key+".json"), "w", encoding="utf-8") as f:
        json.dump(all_podcasts[key],f,indent=4, ensure_ascii=False)

'''for key in all_podcasts["1"]:
    for part in all_podcasts["1"][key]:
        if part == "Camillo Schumann": 
            print(all_podcasts["1"][key]) '''