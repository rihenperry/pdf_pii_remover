import pytest
import os
import pdfquery
from pii import erase_pii_from_pdf

erase_pii_from_pdf()
pdf = pdfquery.PDFQuery(os.path.join(os.getcwd()+"/output", "example1.op.pdf"))
pdf.load()

def test_visa_last_four_digits_pattern_should_be_absent():
    expected = 'Visa | Last digits:'

    lbl = pdf.pq('LTTextLineHorizontal:contains("digits:")')
    assert lbl.text() == expected



def test_visa_ending_with_four_digits_pattern_should_be_absent():
    expected = ''

    lbl = pdf.pq('LTTextLineHorizontal:contains("1234")')
    assert lbl.text() == expected

def test_email_address_should_be_absent():
    expected = ''

    lbl = pdf.pq('LTTextLineHorizontal:contains("@")')
    assert lbl.text() == expected


