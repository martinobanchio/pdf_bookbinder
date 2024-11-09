#!/usr/bin/env python3

"""
A very simple python script for reordering a PDF file in a foldable booklet style. 
Two pdf pages per face, and you can fold the printed papers in the middle, 
and read it like a normal book. 

Usage: python booklet.py <input_file.pdf>

The PDF is ready for two-sided flip-on-short-side printing.

Creator: Furyton
Updated by: martinobanchio
Date: 11-7-2024
"""

import sys
import os
import math
from pypdf import PdfWriter, PdfReader

SHEET_NUMBER = 4

def gen_page_index(n: int) -> list:
    """Return a list of indices ordered for booklet printing"""
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


def main():
    """Main function"""
    if len(sys.argv) == 1:
        print("Usage: python booklet.py <input_file>.pdf")
        print("Output: <input_file>_output.pdf")
        exit()

    with open(f"{sys.argv[1]}", "rb") as readfile:
        output_pdf = PdfWriter()
        input_pdf = PdfReader(readfile)
        n_page = len(input_pdf.pages)

        output_index_list = gen_page_index(n_page)
        a = input_pdf.pages[0]
        width = a.mediabox[2]
        height = a.mediabox[3]

        for idx in output_index_list:
            if idx == -1:
                output_pdf.add_blank_page(width, height)
            else:
                output_pdf.add_page(input_pdf.pages[idx])

        input_file = sys.argv[1]
        output_file = os.path.join(
            os.path.dirname(input_file),
            os.path.splitext(os.path.basename(input_file))[0]
            + "_output"
            + os.path.splitext(os.path.basename(input_file))[1],
        )
        with open(rf"{output_file}", "wb") as writefile:
            output_pdf.write(writefile)
        print("Created", n_page, f"pages {output_file}")


if __name__ == "__main__":
    main()
