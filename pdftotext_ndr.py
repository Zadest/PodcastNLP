# -*- coding : utf8 -*-
from typing import Text
import PyPDF2 as pdf
import re as re
import os

from PyPDF2 import PdfFileReader as reader

import json
from pathlib import Path

import texttojson_ndr as jndr
from dataTools import iter_files as iter

def text_to_dict(text:str,write_state:bool=False) -> dict[int,list[str]] or None:
    textLineItems = text.split('\n')    
    my_dict = {}
    j = 0
    for i in range(0,len(textLineItems)-1):
        if len(textLineItems[i].split(" ")) <= 2:
            my_dict[j] = [textLineItems[i],textLineItems[i+1].encode("utf-8").decode("utf-8")]
            j += 1
    if not my_dict:
        return None
    if write_state:
        with open("data/test.json","w") as f:
            print("test write")
            f.write(json.dumps(my_dict,indent=4))
    return my_dict

def extrText(fileName):
    r = reader(fileName)
    numPages =  r.getNumPages()
    text = ''
    for i in range(numPages):
        page = r.getPage(i)
        text = text + page.extractText()
    # print(Text)
    return text

def performRegEx(text):
    # Bindestrich entfernen
    expColon = re.compile("\n-")
    colonText = expColon.sub('',text)
    # Zeilenumsprung entfernen
    expLB = re.compile('\n')
    lbText = expLB.sub(' ',colonText)
    # Start
    head = re.sub('1/','\nHead\n1/',lbText)
    # Unterteilung nach Redner
    expCD = re.compile("\sChristian Drosten\s")
    expKH = re.compile("\sKorinna Hennig\s|\sCorinna Hennig\s")
    expAM = re.compile("\sAnja Martini\s")
    expDB = re.compile("\sDirk Brockmann\s")
    expSC = re.compile("\sSandra Ciesek\s")
    expSK = re.compile("\sProf. Dr. Stefan Kluge\s|\sStefan Kluge\s")
    expBS = re.compile("\sBeke Schulmann\s")
    cd = expCD.sub("\nChristian Drosten\n",head)
    kh = expKH.sub("\nKorinna Hennig\n",cd)
    am = expAM.sub("\nAnja Martini\n",kh)
    db = expDB.sub("\nDirk Brockmann\n",am) 
    sc = expSC.sub("\nSandra Ciesek\n",db)
    sk = expSK.sub("\nStefan Kluge\n",sc) 
    bs = expBS.sub("\nBeke Schulmann\n",sk) 
    speakertransformed = bs
    # Spezialfolge 51
    # if Folge = 51: 
    expBiS = re.compile("\sProf. Birgit Spinath\s|\sBirgit Spinath\s")
    expJM = re.compile("\sProf. Dr. J??rgen Manemann\s|\sJ??rgen Manemann\s")
    expJSC = re.compile("\sProf. Dr. Jonas Schmidt-Chanasit\s|\sJonas Schmidt-Chanasit\s")
    bis = expBiS.sub("\nBirgit Spinath\n",speakertransformed)
    jm = expJM.sub("\nJ??rgen Manemann\n",bis)
    jsc = expJSC.sub("\nJonas Schmidt-Chanasit\n",jm)
    speakertransformed = jsc
    # Spezialfolge 52
    # if Folge = 52:
    expMA = re.compile("\sProf. Dr. Marylyn Addo\s|\sMarylyn Addo\s")
    expAB = re.compile("\sProf. Dr. Alena Buyx\s|\sAlena Buyx\s")
    expHGE = re.compile("\sProf. Dr. Hans-Georg Eichler\s|\sHans-Georg Eichler\s")
    expWG = re.compile("\sProf. Dr. Wolfgang Greiner\s|\sWolfgang Greiner\s")
    ma = expMA.sub("\nMarylyn Addo\n",speakertransformed)
    ab = expAB.sub("\nAlena Buyx\n",ma)
    hge = expHGE.sub("\nHans-Georg Eichler\n",ab)
    wg = expWG.sub("\nWolfgang Greiner\n",hge)
    speakertransformed = wg
    # Spezialfolge 53
    # if Folge = 53:
    expAnM = re.compile("\sAnia Muntau\s")
    expLW = re.compile("\sLothar Wieler\s")
    expMK = re.compile("\sMartin Kriegel\s")
    anm = expAnM.sub("\nAnia Muntau\n",speakertransformed)
    lw = expLW.sub("\nLothar Wieler\n",anm)
    mk = expMK.sub("\nMartin Kriegel\n",lw)
    speakertransformed = mk
    # Spezialfolge 67
    # if Folge = 67:
    expGR = re.compile("\sGernot Rohde\s")
    gr = expGR.sub("\nGernot Rohde\n",speakertransformed)
    speakertransformed = gr
    # Spezialfolge 81
    # if Folge = 81:
    expCDS = re.compile("\sChristian Dohna-Schwake\s")
    cds = expCDS.sub("\nChristian Dohna-Schwake\n",speakertransformed)
    speakertransformed = cds
    # Doppelter Space entfernen
    spaceText =  re.sub(' +',' ',speakertransformed)
    # Linebreak vor Redner
    cd2 = expCD.sub("\nChristian Drosten\n",spaceText)
    kh2 = expKH.sub("\nKorinna Hennig\n",cd2)
    am2 = expKH.sub("\nAnja Martini\n",kh2)
    db2 = expAM.sub("\nDirk Brockmann\n",am2)
    sc2 = expSC.sub("\nSandra Ciesek\n",db2)
    sk2 = expSK.sub("\nStefan Kluge\n",sc2) 
    bs2 = expBS.sub("\nBeke Schulmann\n",sk2) 
    speakertransformed = bs
    # Spezialfolge 51
    # if Folge = 51: 
    bis2 = expBiS.sub("\nBirgit Spinath\n",speakertransformed)
    jm2 = expJM.sub("\nJ??rgen Manemann\n",bis2)
    jsc2 = expJSC.sub("\nJonas Schmidt-Chanasit\n",jm2)
    speakertransformed = jsc2
    # Spezialfolge 52
    # if Folge = 52:
    ma2 = expMA.sub("\nMarylyn Addo\n",speakertransformed)
    ab2 = expAB.sub("\nAlena Buyx\n",ma2)
    hge2 = expHGE.sub("\nHans-Georg Eichler\n",ab2)
    wg2 = expWG.sub("\nWolfgang Greiner\n",hge2)
    speakertransformed = wg2
    # Spezialfolge 53
    # if Folge = 53:
    anm2 = expAnM.sub("\nAnia Muntau\n",speakertransformed)
    lw2 = expLW.sub("\nLothar Wieler\n",anm2)
    mk2 = expMK.sub("\nMartin Kriegel\n",lw2)
    speakertransformed = mk2
    # Spezialfolge 67
    # if Folge = 67:
    gr2 = expGR.sub("\nGernot Rohde\n",speakertransformed)
    speakertransformed = gr2
    # Spezialfolge 81
    # if Folge = 81:
    cds2 = expCDS.sub("\nChristian Dohna-Schwake\n",speakertransformed)
    speakertransformed = cds2
    # Infos
    info = re.sub('WEITERE','\nInfo\nWEITERE',speakertransformed)
    speakertransformed = info
    # Sonderzeichen
    specChar1 = re.compile('???|???')
    specCharText = specChar1.sub('"',speakertransformed)
    specChar2 = re.compile('??')
    specCharText = specChar2.sub('???',specCharText)
    cleanText = specCharText
    return cleanText

def iterateFiles(filepath:str,index):
    for i in range(100,index,2):
        path = os.path.join(filepath,'coronaskript'+str(i)+'.pdf')
        print(path)
        if os.path.exists(path):
            text = extrText(path)
            retext = performRegEx(text)
            path2 = os.path.join('data','REFINED','ndr')
            if os.path.exists(path2):
                with open(os.path.join(path2,str(i)+'.txt'),'w',encoding='utf-8') as f:
                    f.write(retext)
                jndr.dicttojson(i,path2)
        else:
            print('Datei nicht gefunden.')

# TODO make it work
def findHeadlines(file):
    with open(file,'r') as f:
        spans = f.readlines()
        # print(spans)
        for i in range(0,len(spans)):
            h = re.search('\b[A-Z][A-Z][A-Z]',spans[i])
            if h:
                print(i,h)

# wenn die Python-Datei ausgef??hrt wird, wird folgendes ausgef??hrt : 
if __name__ == "__main__":
    # get folder:
    folder = os.path.join('data','RAW','ndr')
    # get file count in folder
    file_count = len(os.listdir(folder))-1

    # Iterate over all files in folder:
    iterateFiles(folder,file_count)
