# -*- coding : utf8 -*-
from typing import Text
import PyPDF2 as pdf
import re as re

from PyPDF2 import PdfFileReader as reader
from PyPDF2.pdf import PageObject as po

def importFile(fileName):
    r = reader(fileName)
    fileInfo = r.getDocumentInfo()
    pageLayout = r.getPageLayout()
    pageNum = r.getNumPages()
    outlines = r.getOutlines() 
    print(fileInfo,pageLayout,pageNum,outlines,sep='\n')

def extrText(fileName):
    r = reader(fileName)
    numPages =  r.getNumPages()
    global Text
    Text = ''
    for i in range(numPages):
        page = r.getPage(i)
        Text = Text + page.extractText()
    print(Text)

def performRegEx(Text):
    # Bindestrich entfernen
    expColon = re.compile("\n-")
    colonText = expColon.sub('',Text)
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
    CD = expCD.sub("\nChristian Drosten\n",lbText)
    KH = expKH.sub("\nKorrina Hennig\n",CD)
    AM = expAM.sub("\nAnja Martini\n",KH)
    DB = expDB.sub("\nDirk Brockmann\n",AM) 
    SC = expSC.sub("\nSandra Ciesek\n",DB)
    SK = expSK.sub("\nStefan Kluge\n",SC) 
    BS = expBS.sub("\nBeke Schulmann\n",SK) 
    SpeakerTransformed = BS
    # Spezialfolge 51
    # if Folge = 51: 
    expBiS = re.compile("\sProf. Birgit Spinath\s|\sBirgit Spinath\s")
    expJM = re.compile("\sProf. Dr. Jürgen Manemann\s|\sJürgen Manemann\s")
    expJSC = re.compile("\sProf. Dr. Jonas Schmidt-Chanasit\s|\sJonas Schmidt-Chanasit\s")
    BiS = expBiS.sub("\nBirgit Spinath\n",SpeakerTransformed)
    JM = expJM.sub("\nJürgen Manemann\n",BiS)
    JSC = expJSC.sub("\nJonas Schmidt-Chanasit\n",JM)
    SpeakerTransformed = JSC
    # Spezialfolge 52
    # if Folge = 52:
    expMA = re.compile("\sProf. Dr. Marylyn Addo\s|\sMarylyn Addo\s")
    expAB = re.compile("\sProf. Dr. Alena Buyx\s|\sAlena Buyx\s")
    expHGE = re.compile("\sProf. Dr. Hans-Georg Eichler\s|\sHans-Georg Eichler\s")
    expWG = re.compile("\sProf. Dr. Wolfgang Greiner\s|\sWolfgang Greiner\s")
    MA = expMA.sub("\nMarylyn Addo\n",SpeakerTransformed)
    AB = expAB.sub("\nAlena Buyx\n",MA)
    HGE = expHGE.sub("\nHans-Georg Eichler\n",AB)
    WG = expWG.sub("\nWolfgang Greiner\n",HGE)
    SpeakerTransformed = WG
    # Spezialfolge 53
    # if Folge = 53:
    expAnM = re.compile("\sAnia Muntau\s")
    expLW = re.compile("\sLothar Wieler\s")
    expMK = re.compile("\sMartin Kriegel\s")
    AnM = expAnM.sub("\nAnia Muntau\n",SpeakerTransformed)
    LW = expLW.sub("\nLothar Wieler\n",AnM)
    MK = expMK.sub("\nMartin Kriegel\n",LW)
    SpeakerTransformed = MK
    # Spezialfolge 67
    # if Folge = 67:
    expGR = re.compile("\sGernot Rohde\s")
    GR = expGR.sub("\nGernot Rohde\n",SpeakerTransformed)
    SpeakerTransformed = GR
    # Spezialfolge 81
    # if Folge = 81:
    expCDS = re.compile("\sChristian Dohna-Schwake\s")
    CDS = expCDS.sub("\nChristian Dohna-Schwake\n",SpeakerTransformed)
    SpeakerTransformed = CDS
    # Doppelter Space entfernen
    space = re.compile('\s\s')
    spaceText =  space.sub(' ',SpeakerTransformed)
    # Linebreak vor Redner
    CD2 = expCD.sub("\nChristian Drosten\n",spaceText)
    KH2 = expKH.sub("\nKorrina Hennig\n",CD2)
    AM2 = expKH.sub("\nAnja Martini\n",KH2)
    DB2 = expAM.sub("\nDirk Brockmann\n",AM2)
    SC = expSC.sub("\nSandra Ciesek\n",DB)
    SK = expSK.sub("\nStefan Kluge\n",SC) 
    BS = expBS.sub("\nBeke Schulmann\n",SK) 
    SpeakerTransformed = BS
    # Spezialfolge 51
    # if Folge = 51: 
    BiS = expBiS.sub("\nBirgit Spinath\n",SpeakerTransformed)
    JM = expJM.sub("\nJürgen Manemann\n",BiS)
    JSC = expJSC.sub("\nJonas Schmidt-Chanasit\n",JM)
    SpeakerTransformed = JSC
    # Spezialfolge 52
    # if Folge = 52:
    MA = expMA.sub("\nMarylyn Addo\n",SpeakerTransformed)
    AB = expAB.sub("\nAlena Buyx\n",MA)
    HGE = expHGE.sub("\nHans-Georg Eichler\n",AB)
    WG = expWG.sub("\nWolfgang Greiner\n",HGE)
    SpeakerTransformed = WG
    # Spezialfolge 53
    # if Folge = 53:
    AnM = expAnM.sub("\nAnia Muntau\n",SpeakerTransformed)
    LW = expLW.sub("\nLothar Wieler\n",AnM)
    MK = expMK.sub("\nMartin Kriegel\n",LW)
    SpeakerTransformed = MK
    # Spezialfolge 67
    # if Folge = 67:
    GR = expGR.sub("\nGernot Rohde\n",SpeakerTransformed)
    SpeakerTransformed = GR
    # Spezialfolge 81
    # if Folge = 81:
    CDS = expCDS.sub("\nChristian Dohna-Schwake\n",SpeakerTransformed)
    SpeakerTransformed = CDS
    # Sonderzeichen
    specChar1 = re.compile('—|ﬁ')
    specCharText = specChar1.sub('"',SpeakerTransformed)
    specChar2 = re.compile('Š')
    specCharText = specChar2.sub('—',specCharText)
    #specChar3 = re.compile('\w,\w')
    #specCharText = specChar3.sub("n's",specCharText)
    cleanText = specCharText
    print(cleanText,sep='\n\n')
    '''
    with open('Skript001ndr.txt','wb') as f:
        f.write(Text)
    '''
# importFile('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/NDR_CVUpdate/SkriptFolge001.pdf')
extrText('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/NDR_CVUpdate/SkriptFolge001.pdf')
performRegEx(Text)