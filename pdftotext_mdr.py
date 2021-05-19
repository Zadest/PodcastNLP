from decorators import timer
import PyPDF2 as pdf

from PyPDF2 import PdfFileReader as reader

def importFile(fileName):
    r = reader(fileName)
    fileInfo = r.getDocumentInfo()
    pageLayout = r.getPageLayout()
    pageNum = r.getNumPages()
    print(fileInfo,pageLayout,pageNum,sep='\n')

importFile('/Users/nikavolk-spiller/Desktop/kck172.pdf')
