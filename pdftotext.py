# -*- coding : utf8 -*-
import PyPDF2 as pdf

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
    Text = ''
    for i in range(numPages):
        page = r.getPage(i)
        Text = Text + page.extractText()
    
    print(Text,sep='\n')
    '''
    with open('Skript001ndr.txt','wb') as f:
        f.write(Text)
    '''
# importFile('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/NDR_CVUpdate/SkriptFolge001.pdf')
extrText('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/NDR_CVUpdate/SkriptFolge001.pdf')