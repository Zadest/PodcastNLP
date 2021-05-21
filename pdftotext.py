from decorators import timer
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
    o = po(fileName)
    r = reader(fileName)
    text = o.extractText()
    print(text,sep='\n')

# importFile('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/NDR_CVUpdate/SkriptFolge001.pdf')
extrText('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/NDR_CVUpdate/SkriptFolge001.pdf')