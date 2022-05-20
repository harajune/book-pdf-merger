import argparse
from PyPDF2 import PdfFileMerger, PdfFileReader

class PdfParameter:
  def __init__(self, filename, reverse=False):
    self._filename = filename
    self._reverse = reverse

  @property
  def filename(self):
    return self._filename

  @property
  def reverse(self):
    return self._reverse

class Pdf:
  def __init__(self, pdfParameter):
    self._pdfParameter = pdfParameter
    self._currentPage = 0
  
  @property
  def fileObject(self):
    return self._fileObject

  @property
  def currentPage(self):
    return self._currentPage

  @property
  def numOfPages(self):
    return self._numOfPages

  def load(self):
    self._fileObject = open(self._pdfParameter.filename, "rb")
    self._numOfPages = PdfFileReader(self._fileObject).getNumPages()

    # client have to call next() first.
    # the page number begins with 0
    if self._pdfParameter.reverse:
      self._currentPage = self._numOfPages
    else:
      self._currentPage = -1

  def next(self):
    if self._pdfParameter.reverse:
      self._currentPage = self._currentPage - 1
    else:
      self._currentPage = self._currentPage + 1

    if self._currentPage < 0 or self._currentPage >= self._numOfPages:
      return False

    return True

class PdfMerger:
  def __init__(self, outputFileName):
    self._merger = PdfFileMerger()
    self._outputFileName = outputFileName

  def append(self, pdf):
    self._merger.append(fileobj=pdf.fileObject, pages=(pdf.currentPage, pdf.currentPage + 1))

  def write(self):
    self._merger.write(self._outputFileName)

def parseArguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('--out', help='output file path', required=True)
  parser.add_argument('--in1', help='first input pdf path', required=True)
  parser.add_argument('--in2', help='second input pdf path', required=True)
  parser.add_argument('--reverse1', help='reverse first pdf page order', action='store_true')
  parser.add_argument('--reverse2', help='reverse second pdf page order', action='store_true')
  
  return parser.parse_args()

def writeMergedPdf(pdfParameter1, pdfParameter2, outputFileName):
  merger = PdfMerger(outputFileName)
  pdf1 = Pdf(pdfParameter1)
  pdf1.load()
  
  pdf2 = Pdf(pdfParameter2)
  pdf2.load()

  validatePdf(pdf1, pdf2)

  # usually, pdf1 is greater than pdf2
  while pdf1.next():
    merger.append(pdf1)

    if pdf2.next():
      merger.append(pdf2)

  merger.write()
  
def validatePdf(pdf1, pdf2):
  # check file page difference
  num_difference = pdf1.numOfPages - pdf2.numOfPages
  if num_difference < 0 or num_difference > 1:
    raise Exception('Invalid page numbers: in1:%d in2:%d' % 
      (pdf1.numOfPages, pdf2.numOfPages))

if __name__ == '__main__':
  args = parseArguments()

  pdf1 = PdfParameter(args.in1, args.reverse1)
  pdf2 = PdfParameter(args.in2, args.reverse2)

  outputFileName = args.out

  writeMergedPdf(pdf1, pdf2, outputFileName)


