# -*- coding : utf8 -*-
from typing import Text
import PyPDF2 as pdf
import re as re
import os

from PyPDF2 import PdfFileReader as reader

import json
from pathlib import Path

import texttojson_ndr as jndr

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
    # Unterteilung nach Redner
    expCD = re.compile("\sChristian Drosten\s")
    expKH = re.compile("\sKorinna Hennig\s|\sCorinna Hennig\s")
    expAM = re.compile("\sAnja Martini\s")
    expDB = re.compile("\sDirk Brockmann\s")
    expSC = re.compile("\sSandra Ciesek\s")
    expSK = re.compile("\sProf. Dr. Stefan Kluge\s|\sStefan Kluge\s")
    expBS = re.compile("\sBeke Schulmann\s")
    cd = expCD.sub("\nChristian Drosten:",lbText)
    kh = expKH.sub("\nKorinna Hennig:",cd)
    am = expAM.sub("\nAnja Martini:",kh)
    db = expDB.sub("\nDirk Brockmann:",am) 
    sc = expSC.sub("\nSandra Ciesek:",db)
    sk = expSK.sub("\nStefan Kluge:",sc) 
    bs = expBS.sub("\nBeke Schulmann:",sk) 
    speakertransformed = bs
    # Spezialfolge 51
    # if Folge = 51: 
    expBiS = re.compile("\sProf. Birgit Spinath\s|\sBirgit Spinath\s")
    expJM = re.compile("\sProf. Dr. Jürgen Manemann\s|\sJürgen Manemann\s")
    expJSC = re.compile("\sProf. Dr. Jonas Schmidt-Chanasit\s|\sJonas Schmidt-Chanasit\s")
    bis = expBiS.sub("\nBirgit Spinath:",speakertransformed)
    jm = expJM.sub("\nJürgen Manemann:",bis)
    jsc = expJSC.sub("\nJonas Schmidt-Chanasit:",jm)
    speakertransformed = jsc
    # Spezialfolge 52
    # if Folge = 52:
    expMA = re.compile("\sProf. Dr. Marylyn Addo\s|\sMarylyn Addo\s")
    expAB = re.compile("\sProf. Dr. Alena Buyx\s|\sAlena Buyx\s")
    expHGE = re.compile("\sProf. Dr. Hans-Georg Eichler\s|\sHans-Georg Eichler\s")
    expWG = re.compile("\sProf. Dr. Wolfgang Greiner\s|\sWolfgang Greiner\s")
    ma = expMA.sub("\nMarylyn Addo:",speakertransformed)
    ab = expAB.sub("\nAlena Buyx:",ma)
    hge = expHGE.sub("\nHans-Georg Eichler:",ab)
    wg = expWG.sub("\nWolfgang Greiner:",hge)
    speakertransformed = wg
    # Spezialfolge 53
    # if Folge = 53:
    expAnM = re.compile("\sAnia Muntau\s")
    expLW = re.compile("\sLothar Wieler\s")
    expMK = re.compile("\sMartin Kriegel\s")
    anm = expAnM.sub("\nAnia Muntau:",speakertransformed)
    lw = expLW.sub("\nLothar Wieler:",anm)
    mk = expMK.sub("\nMartin Kriegel:",lw)
    speakertransformed = mk
    # Spezialfolge 67
    # if Folge = 67:
    expGR = re.compile("\sGernot Rohde\s")
    gr = expGR.sub("\nGernot Rohde:",speakertransformed)
    speakertransformed = gr
    # Spezialfolge 81
    # if Folge = 81:
    expCDS = re.compile("\sChristian Dohna-Schwake\s")
    cds = expCDS.sub("\nChristian Dohna-Schwake:",speakertransformed)
    speakertransformed = cds
    # Doppelter Space entfernen
    spaceText =  re.sub(' +',' ',speakertransformed)
    # Linebreak vor Redner
    cd2 = expCD.sub("\nChristian Drosten:",spaceText)
    kh2 = expKH.sub("\nKorinna Hennig:",cd2)
    am2 = expKH.sub("\nAnja Martini:",kh2)
    db2 = expAM.sub("\nDirk Brockmann:",am2)
    sc2 = expSC.sub("\nSandra Ciesek:",db2)
    sk2 = expSK.sub("\nStefan Kluge:",sc2) 
    bs2 = expBS.sub("\nBeke Schulmann:",sk2) 
    speakertransformed = bs
    # Spezialfolge 51
    # if Folge = 51: 
    bis2 = expBiS.sub("\nBirgit Spinath:",speakertransformed)
    jm2 = expJM.sub("\nJürgen Manemann:",bis2)
    jsc2 = expJSC.sub("\nJonas Schmidt-Chanasit:",jm2)
    speakertransformed = jsc2
    # Spezialfolge 52
    # if Folge = 52:
    ma2 = expMA.sub("\nMarylyn Addo:",speakertransformed)
    ab2 = expAB.sub("\nAlena Buyx:",ma2)
    hge2 = expHGE.sub("\nHans-Georg Eichler:",ab2)
    wg2 = expWG.sub("\nWolfgang Greiner:",hge2)
    speakertransformed = wg2
    # Spezialfolge 53
    # if Folge = 53:
    anm2 = expAnM.sub("\nAnia Muntau:",speakertransformed)
    lw2 = expLW.sub("\nLothar Wieler:",anm2)
    mk2 = expMK.sub("\nMartin Kriegel:",lw2)
    speakertransformed = mk2
    # Spezialfolge 67
    # if Folge = 67:
    gr2 = expGR.sub("\nGernot Rohde:",speakertransformed)
    speakertransformed = gr2
    # Spezialfolge 81
    # if Folge = 81:
    cds2 = expCDS.sub("\nChristian Dohna-Schwake:",speakertransformed)
    speakertransformed = cds2
    # Sonderzeichen
    specChar1 = re.compile('—|ﬁ')
    specCharText = specChar1.sub('"',speakertransformed)
    specChar2 = re.compile('Š')
    specCharText = specChar2.sub('—',specCharText)
    cleanText = specCharText
    print(cleanText,sep='\n\n')
    return cleanText

def iterateFiles(filepath:str,index):
    for i in range(100,index,2):
        path = os.path.join(filepath,'coronaskript'+str(i)+'.pdf')
        print(path)
        if os.path.exists(path):
            text = extrText(path)
            retext = performRegEx(text)
            with open(str(i)+'.txt','w',encoding='utf-8') as f:
                f.write(retext)
            jndr.dicttojson(str(i)+'.txt')
        else:
            print('Datei nicht gefunden.')


# wenn die Python-Datei ausgeführt wird, wird folgendes ausgeführt : 
#if __name__ == "__main__":
    # get folder:
folder = os.path.join('data','RAW','ndr')
print(folder)
    # # get file count in folder:
    # file_count = len(os.listdir(folder))-1

    # # Iterate over all files in folder:
    # iterateFiles(folder,file_count)

iterateFiles(folder,102)