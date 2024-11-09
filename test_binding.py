""" 
Simple tests for the main functions of the bookbinding library.

Usage: pytest test_binding.py

Creator: martinobanchio
Date: 11-9-2024
"""

import sys
import pdf_bookbinder.booklet as booklet
import pdf_bookbinder.book as book


def test_gen_page_index():
    """Tests gen_page_index behavior"""
    assert booklet.gen_page_index(5) == [-1, 0, 1, -1, -1, 2, 3, 4]
    assert booklet.gen_page_index(3) == [-1, 0, 1, 2]
    assert booklet.gen_page_index(8) == [7, 0, 1, 6, 5, 2, 3, 4]


def test_gen_signatures():
    """Tests gen_signatures behavior"""
    assert book.gen_signatures(9, 4) == [3, 0, 1, 2, -1, 4, 5, -1, -1, 6, 7, 8]
    assert book.gen_signatures(9, 16) == booklet.gen_page_index(9)
    assert book.gen_signatures(5, 4) == [3, 0, 1, 2, -1, 4, -1, -1]
