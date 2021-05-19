from decorators import timer
import PyPDF2 as pdf

from PyPDF2 import PdfFileReader as reader

def importFile(fileName):
    r = reader(fileName)
    fileInfo = r.getDocumentInfo()
    pageLayout = r.getPageLayout()
    pageNum = r.getNumPages()
    print(fileInfo,pageLayout,pageNum,sep='\n')

importFile('C:/Users/teres/OneDrive/Dokumente/Studium/Master/vl/CoronaPodcasts/MDR_KCKompass/kck172.pdf')