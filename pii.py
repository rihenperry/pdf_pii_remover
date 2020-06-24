import os
from fpdf import FPDF
import pdftotext
import io
import re

path = os.getcwd()
folder = os.listdir(path+"/input")

def erase_pii_from_pdf():
    for doc in folder:
        print()
        # open the input file
        f = open(os.path.join(path+"/input", doc), 'rb')
        print('now reading.... {0}'.format(os.path.join(path+"/input", doc)))
        mem_file = io.BytesIO(f.read())
        f.close()
        txt = pdftotext.PDF(mem_file)

        # initialize empty list of index which will be processed by nested loop
        sub_index_lst = []

        # create a empty document and configure with font
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 12)

        txt_r_strip = txt[0].rstrip()
        txt_strip = txt_r_strip.strip()
        lines = txt_strip.split('\n')

        # check for following string patterns on every line of the extracted text
        print('erasing PII text......')
        for i in range(len(lines)):
            # check for email addresses
            l = lines[i]
            l = re.sub(r'[\w\.-]+@[\w\.-]+', '', l, re.IGNORECASE)

            # check for name in from pattern following from:
            m = re.search(r'From:\s+', l)
            if isinstance(m, re.Match):
                l = m.group(0)

            # erase the last 4 digits of visa in first occurrence
            m = re.search(r'^Visa[\w\s]+\|[\w\s]+:\s+', l)
            if isinstance(m, re.Match):
                l = m.group(0)

            # erase the last 4 digits of visa card in second occurrence
            l = re.sub(r'Visa[\w\s]+ending[\w\s]+in\s\d{4}', 'Visa ending in', l, re.IGNORECASE)

            # erase the address lines following the pattern beginning with shipping or billing
            m = re.search(r'(Billing\s+address)|(Shipping\s+Address)', l)
            if isinstance(m, re.Match):
                pdf.cell(200, 5, txt = l, ln = 1, align = 'L')
                i += 1
                l = lines[i] #get the next line following shipping and billing address

                no_blank_start = re.search(r'^\s{0,2}(\w{1,50})[:#.\s\w,]{0,50}\s{0,5}', l) # only erase lines beginning with at most 0 spaces followed by alphanumeric chars
                spcl_char_in_txt = re.search(r'([$-]+)|(^\s+$)', l) # do not erase lines containing $ -
                spcl_marker_in_txt = re.search(r'^(\s*)Credit', l) # tightly coded maker for a edge case in document 1 which terminates the while loop

                while (isinstance(no_blank_start, re.Match) or isinstance(spcl_char_in_txt, re.Match)) and not isinstance(spcl_marker_in_txt, re.Match):
                    if isinstance(no_blank_start, re.Match):
                        l = re.sub(r'^\s{0,2}(\w{1,50})[:#.\s\w,]{0,50}\s{0,5}', " ", l, re.IGNORECASE)
                    pdf.cell(200, 5, txt = l, ln = 1, align = 'L')
                    sub_index_lst.append(i)
                    i += 1
                    l = lines[i]
                    no_blank_start = re.search(r'^\s{0,2}(\w{1,50})[:#.\s\w,]{0,50}\s{0,5}', l)
                    spcl_char_in_txt = re.search(r'([$-]+)|(^\s*$)', l)
                    spcl_marker_in_txt = re.search(r'^(\s*)Credit', l)
            elif i in sub_index_lst:
                # skip indexes which are already processed by the while loop
                continue
            else:
                # Any lines that do not match the patterns are written to the document
                pdf.cell(200, 5, txt = l, ln = 1, align = 'L')

        # finally, persist the desired text to document
        output_fname = os.path.basename(os.path.join(path+"/input", doc)).split('.')[0] + ".op.pdf"
        output_path = os.path.join(path+"/output/") + output_fname
        print('writing pdf.... {0}'.format(output_path))
        pdf.output(output_path, 'F')
