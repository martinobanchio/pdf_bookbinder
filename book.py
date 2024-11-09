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

if __name__ == "__main__":
    import booklet
else:
    from pdf_bookbinder import booklet

SHEET_NUMBER = 4


def gen_signatures(n: int, signature_length: int) -> list:
    """Returns a list of indices ordered for booklet printing, split in signatures"""

    if n <= signature_length:
        return booklet.gen_page_index(n)

    if n <= signature_length * 2:
        return booklet.gen_page_index(signature_length) + [
            x + signature_length if x >= 0 else -1
            for x in booklet.gen_page_index(n - signature_length)
        ]

    # All signatures except the last one
    number_signatures = n // signature_length

    # Last pages may end up in a separate signature or added to previous ones
    last_pages = n % signature_length

    last_signatures = 1
    first_signatures = number_signatures
    flag_lone_last_signature = True

    if last_pages <= signature_length / 2:
        flag_lone_last_signature = False
        last_signatures = math.ceil(last_pages / SHEET_NUMBER)
        first_signatures = max(number_signatures - last_signatures, 0)

    page_list = []
    for i in range(first_signatures):
        page_list = page_list + [
            x + i * signature_length for x in booklet.gen_page_index(signature_length)
        ]

    for i in range(last_signatures - 1):
        page_list = page_list + [
            x
            + (first_signatures * signature_length)
            + i * (signature_length + SHEET_NUMBER)
            for x in booklet.gen_page_index(signature_length + SHEET_NUMBER)
        ]

    if last_pages > 0:
        extra_pages_in_last_signature = (
            0 if flag_lone_last_signature or first_signatures == 0 else signature_length
        )

        # Special case where there is only one signature
        if number_signatures == last_signatures:
            extra_pages_in_last_signature = signature_length

        page_list = page_list + [
            (
                x
                + (first_signatures * signature_length)
                + (last_signatures - 1) * (signature_length + SHEET_NUMBER)
                if x >= 0
                else -1
            )
            for x in booklet.gen_page_index(extra_pages_in_last_signature + last_pages % 4)
        ]

    return page_list

def is_valid_signature(s: str):
    """Checks whether the user input is a valid signature length"""
    try:
        int(s)
    except ValueError:
        return False
    if int(s) % SHEET_NUMBER != 0 or int(s) > SHEET_NUMBER ** 2:
        return False
    return True

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python book.py <input_file>.pdf <signatures_size>")
        print("Output: <input_file>_output.pdf")
        exit()

    if not is_valid_signature(sys.argv[2]):
        sys.exit("Signature length must be one of 4, 8, 12, or 16.")

    with open(f"{sys.argv[1]}", "rb") as readfile:
        output_pdf = PdfWriter()
        input_pdf = PdfReader(readfile)
        n_page = len(input_pdf.pages)

        output_index_list = gen_signatures(n_page, int(sys.argv[2]))
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
