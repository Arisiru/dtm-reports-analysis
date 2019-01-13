import PyPDF2 
import os
import multiprocessing

dir_data_raw = os.path.join('..', 'data_raw')
dir_data_pdf = os.path.join(dir_data_raw, 'reports_pdf')
dir_data_txt = os.path.join(dir_data_raw, 'reports_txt')

def convert(findex, ticker):
    dir_ticker_pdf = os.path.join(dir_data_pdf, findex, ticker)
    if os.path.isdir(dir_ticker_pdf):
        for report_pdf in os.listdir(dir_ticker_pdf):
            if '.pdf' in report_pdf:
                report_name, ext = report_pdf.split('.')
                txt_report_path = os.path.join(dir_data_txt, findex, ticker, "%s.txt" % report_name)
                if os.path.exists(txt_report_path):
                    print("%s exists" % txt_report_path)
                else:
                    pdf_report_path = os.path.join(dir_ticker_pdf, report_pdf)
                    print("work on %s" % pdf_report_path)
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
                        with open(txt_report_path, 'w') as text_file:
                            for page_number in range(number_of_pages):
                                try:
                                    page = read_pdf.getPage(page_number)
                                    page_content = page.extractText()
                                    text_file.write(page_content)
                                    total += len(page_content)
                                except:
                                    print("Can't read page %s of %s" % (page_number, pdf_report_path))    
                        print("%s pages %s total chars %s" % (report_pdf, page_number, total))

for findx in os.listdir(dir_data_pdf):
    dir_findx = os.path.join(dir_data_pdf, findx)
    if os.path.isdir(dir_findx):
        #for ticker in os.listdir(dir_findx):
        #    convert(findx, ticker)
        with multiprocessing.Pool(processes=4) as pool:
            pool.starmap(convert, [(findx, ticker) for ticker in os.listdir(dir_findx)])

