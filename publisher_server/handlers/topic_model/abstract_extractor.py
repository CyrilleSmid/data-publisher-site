import PyPDF2
import re

START_PATTERN = 'a b s t r a c t'
END_PATTERN = ' Elsevier Ltd.'

def extract_abstract_text(pdf_path):
    with open(pdf_path,'rb') as f:  
        pdfReader = PyPDF2.PdfFileReader(f)
        pageObj = pdfReader.getPage(0)
        first_page = pageObj.extractText()


        idx1 = first_page.find(START_PATTERN)
        idx2 = first_page.find(END_PATTERN)
        abstract_text = first_page[idx1 + len(START_PATTERN) + 1: idx2]
        abstract_text = abstract_text.lower()
        abstract_text = abstract_text.replace('\n', ' ')

        return abstract_text



        # TODO: Replace faulty characters
        # replacement_dict = {'' : 'ic',
        #                     '': 'ie'}

        # for word, replacement in replacement_dict.items():
        #     strValue = strValue.replace(word, replacement)
extract_abstract_text(r'C:\Users\Cyril\YandexDisk\Work\2022-2023\ПиКПО\Data\Articles\1.pdf')