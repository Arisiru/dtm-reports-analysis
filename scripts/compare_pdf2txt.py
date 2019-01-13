import PyPDF2 
import os

report_pdf = 'WEIR_A1-2016-2017-02-22.pdf'


report_name, ext = report_pdf.split('.')
txt_report_path = "%s.txt" % report_name
pdf_report_path = report_pdf
with open(pdf_report_path,'rb') as pdf_file:
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    if read_pdf.isEncrypted:
        print("%s encripted" % txt_report_path)
        try:
            read_pdf.decrypt('')
        except:
            command = ("cp " + report_pdf + " temp.pdf; qpdf --password='' --decrypt temp.pdf " + report_pdf + "; rm temp.pdf")
            os.system(command)
            pdf_file = open(pdf_report_path,'rb')
            read_pdf = PyPDF2.PdfFileReader(pdf_file)

    number_of_pages = read_pdf.getNumPages()
    total = 0
    with open("1-" + txt_report_path, 'w') as text_file:
        for page_number in range(number_of_pages):
            try:
                page = read_pdf.getPage(page_number)
                page_content = page.extractText()
                text_file.write(page_content)
                total += len(page_content)
            except:
                print("Can't read page %s of %s" % (page_number, pdf_report_path))    
    print("%s pages %s total chars %s" % (report_pdf, page_number, total))



command = "pdftotext %s %s" % (pdf_report_path, "2-" + txt_report_path)
os.system(command)
result_file = open(txt_report_path, 'r')
characters = sum(len(text_line) for text_line in result_file)
print("%s converted, len=%s" % (pdf_report_path, characters))