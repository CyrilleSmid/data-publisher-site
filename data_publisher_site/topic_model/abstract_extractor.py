import PyPDF2

def read_pages(pdf_path, page_nums=[0]):
    with open(pdf_path,'rb') as f:   
        pdfReader = PyPDF2.PdfFileReader(f)
        text = ''
        for page_num in page_nums:
            pageObj = pdfReader.getPage(page_num)
            text += pageObj.extractText() + '\n'
        return text