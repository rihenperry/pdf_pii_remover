import pytest
import os
import pdfquery
from pii import erase_pii_from_pdf

erase_pii_from_pdf()
pdf = pdfquery.PDFQuery(os.path.join(os.getcwd()+"/output", "example2.op.pdf"))
pdf.load()

def test_visa_last_four_digits_pattern_should_be_absent():
    expected = 'Visa | Last digits:'

    lbl = pdf.pq('LTTextLineHorizontal:contains("digits:")')
    assert lbl.text() == expected
