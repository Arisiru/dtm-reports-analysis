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
                try:
                    report_name, ext = report_pdf.split('.')
                    txt_report_path = os.path.join(dir_data_txt, findex, ticker, "%s.txt" % report_name)
                except:
                    print("Bad file name %s" % report_pdf)

                if not os.path.exists(txt_report_path):
                    pdf_report_path = os.path.join(dir_ticker_pdf, report_pdf)
                    command = "pdftotext %s %s" % (pdf_report_path, txt_report_path)
                    os.system(command)
                    if os.path.exists(txt_report_path):
                        result_file = open(txt_report_path, 'r')
                        characters = sum(len(text_line) for text_line in result_file)
                        print("%s converted, len=%s" % (pdf_report_path, characters))
                    else:
                        print("No file after conversion %s" % txt_report_path)                      
                #else: 
                    #print("%s exists" % txt_report_path)       

for findx in os.listdir(dir_data_pdf):
    dir_findx = os.path.join(dir_data_pdf, findx)
    if os.path.isdir(dir_findx):
        #for ticker in os.listdir(dir_findx):
        #    convert(findx, ticker)
        with multiprocessing.Pool(processes=4) as pool:
            pool.starmap(convert, [(findx, ticker) for ticker in os.listdir(dir_findx)])

