import argparse
from PyPDF2 import PdfFileMerger, PdfFileReader

def write_merged_pdf(pdf1, pdf2, output_pdf, **kargs):
  merger = PdfFileMerger()
  num_pages1 = PdfFileReader(pdf1).getNumPages()
  num_pages2 = PdfFileReader(pdf2).getNumPages()

  reverse1 = kargs['reverse1'] or False
  reverse2 = kargs['reverse2'] or False

  # check file page difference
  num_difference = num_pages1 - num_pages2
  if num_difference < 0 or num_difference > 1:
    raise Exception('Invalid page numbers: in1:%d in2:%d' % (num_pages1, num_pages2))
  
  for index in range(num_pages1):
    page1 = index
    if reverse1:
      page1 = num_pages1 - index
    print(page1)
    merger.append(fileobj=pdf1, pages=(page1, page1 + 1))

    # check if the merged document page is odd
    if index <= num_pages2:
      page2 = index
      if reverse2:
        page2 = num_pages2 - index
      merger.append(fileobj=pdf2, pages=(page2, page2 + 1))

  merger.write(output_pdf)
  

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--out', help='output file path', required=True)
  parser.add_argument('--in1', help='first input file path', required=True)
  parser.add_argument('--in2', help='second input file path', required=True)
  parser.add_argument('--reverse1', help='first input file path', action='store_true')
  parser.add_argument('--reverse2', help='second input file path', action='store_true')
  
  args = parser.parse_args()

  pdf1 = open(args.in1, 'rb')
  pdf2 = open(args.in2, 'rb')
  output_pdf = open(args.out, 'wb')

  write_merged_pdf(pdf1, pdf2, output_pdf, reverse1=args.reverse1, reverse2=args.reverse2)


