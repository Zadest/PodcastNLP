from decorators import timer
import PyPDF2 as pdf
import re as re
import os

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
    expColon = re.compile("-\n")
    colonText = expColon.sub('',text)
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
    print(speakertransformed)

def iterateFiles(filepath,index):
    for i in range(0,index):
        path = os.path.join(filepath,str(i)+'.pdf')
        if os.path.exists(path):
            text = extrText(path)
            performRegEx(text)
        else:
            print('Datei nicht gefunden.')

# importFile('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/MDR_KCKompass/kck172.pdf')
# extrText('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/MDR_KCKompass/kck172.pdf')
# performRegEx(text)
iterateFiles(os.path.join('data','RAW','mdr'),127)