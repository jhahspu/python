from PyPDF2 import PdfFileMerger, PdfFileReader
import glob, os

mo = PdfFileMerger()

lst = [i for i in glob.glob("*.pdf")]

for i in lst:
  fl, ext = os.path.splitext(i)
  mo.append(PdfFileReader(fl + '.pdf', 'rb'))

mo.write('merged.pdf')