import PyPDF2
import regex as re

START_PATTERN = r'a ?b ?s ?t ?r ?a ?c ?t' 
END_PATTERN = ' Elsevier Ltd.'

def read_pages(pdf_path, page_nums=[0]):
    with open(pdf_path,'rb') as f:   
        pdfReader = PyPDF2.PdfFileReader(f)
        text = ''
        for page_num in page_nums:
            pageObj = pdfReader.getPage(page_num)
            text += pageObj.extractText() + '\n'
        return text

def extract_abstract_text(pdf_path):
    first_page = read_pages(pdf_path)
    first_page = first_page.replace('  ', ' ')
    first_page = first_page.replace('\n', ' ')

    re_expr = f'(?<={START_PATTERN}).*(?={END_PATTERN})'
    abstract_text = re.search(re_expr, first_page)
    if abstract_text: 
        abstract_text = abstract_text.group() 
        abstract_text = abstract_text.lower()
        return abstract_text
    return abstract_text
    
    # TODO: Replace faulty characters
    # replacement_dict = {'' : 'ic',
    #                     '': 'ie'}

    # for word, replacement in replacement_dict.items():
    #     strValue = strValue.replace(word, replacement)

# extract_abstract_text(r'C:\Users\Cyril\YandexDisk\Work\2022-2023\ПиКПО\Data\Articles\1.pdf')