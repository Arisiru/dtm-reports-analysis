import glob, os, re

dir = os.path.join('..', 'data_raw', 'reports_txt', 'FTSE')
check_report_name_reg_exp = '(?P<ticker>[A-Z1-9]+)_(?P<type>[A-Z]+)_(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})'

for ticker in os.listdir(dir):
    dir_ticker = os.path.join(dir, ticker)
    if os.path.isdir(dir_ticker):
        for file_name in os.listdir(dir_ticker):
            report_name, ext = os.path.splitext(os.path.basename(file_name))
            match = re.search(check_report_name_reg_exp, report_name)
            if not match:
                print("%s doesn'd match the regexp" % file_name)
            else:
                new_file_name = "%s_%s-%s_%s-%s-%s%s" % (
                    match.group('ticker'),
                    match.group('type'),
                    match.group('year'),
                    match.group('year'),
                    match.group('month'),
                    match.group('day'),
                    ext)
                old_path = os.path.join(dir_ticker, file_name)    
                new_path = os.path.join(dir_ticker, new_file_name)
                os.rename(old_path, new_path)
