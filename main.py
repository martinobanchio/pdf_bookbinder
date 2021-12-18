"""
a very simple python script for reordering a PDF file in a foldable booklet style. 
Two pdf pages per face, and you can fold the printed papers in the middle, and read it like a normal book. 

Usage: python main.py <input_file.pdf>

make sure you select printing on both side.

Creator: Furyton
Date: 12-18-2021
"""

import sys
import math
from PyPDF2 import PdfFileWriter, PdfFileReader

if len(sys.argv) == 1:
    print('Usage: python main.py <input_file.pdf>')
    print('Output: output_<input_file.pdf>')
    exit()

def gen_page_index(n: int) -> list:
    extend_n = math.ceil(n / 4) * 4

    temp_list = []
    swap = True
    for i in range(extend_n // 2):
        if swap:
            swap = False
            temp_list.append([extend_n - 1 - i, i])
        else:
            swap = True
            temp_list.append([i, extend_n - 1 - i])
    final_list = []

    for a in temp_list:
        final_list += a
    final_list = [x if x < n else -1 for x in final_list]

    return final_list

with open('%s' % sys.argv[1], 'rb') as readfile:
    output_pdf = PdfFileWriter()
    input_pdf = PdfFileReader(readfile)

    n_page = input_pdf.getNumPages()

    output_index_list = gen_page_index(n_page)
    a = input_pdf.getPage(0)
    width = a.mediaBox[2]
    height = a.mediaBox[3]
    
    for idx in output_index_list:
        if idx == -1:
            output_pdf.addBlankPage(width, height)
        else:
            output_pdf.addPage(input_pdf.getPage(idx))
    
    output_file = 'output_%s' % sys.argv[1]
    with open(r'%s' % output_file, "wb") as writefile:
        output_pdf.write(writefile)
    print('Created', n_page, 'pages %s' % output_file)
