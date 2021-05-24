from decorators import timer
import PyPDF2 as pdf
import re as re

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
    global Text
    Text = ''
    for i in range(numPages):
        page = r.getPage(i)
        Text = Text + page.extractText()
    # print(Text)

def performRegEx(Text):
    # Bindestrich entfernen
    expColon = re.compile("-\n")
    colonText = expColon.sub('',Text)
    # Zeilenumsprung entfernen
    expLB = re.compile('\n')
    lbText = expLB.sub('',colonText)
    # Bindestrich einfügen. Fehler TODO
    # expLB = re.compile('[a-z][A-Z]')
    # lbText = expLB.sub('[a-z]-[A-Z]',colonText)
    # Unterteilung nach Redner
    expCS = re.compile("\sCamillo Schumann\s")
    expAK = re.compile("\sAlexander Kekulé\s|\sProf. Dr. med. Dr. rer. nat. Alexander S. Kekulé\s")
    CS = expCS.sub("\nCamillo Schumann\n",lbText)
    AK = expAK.sub("\nAlexander Kekulé\n",CS)
    SpeakerTransformed = AK
    print(SpeakerTransformed)


# importFile('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/MDR_KCKompass/kck172.pdf')
extrText('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/MDR_KCKompass/kck172.pdf')
performRegEx(Text)