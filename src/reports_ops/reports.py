def get_ticker_from_report_name(report_name):
    ticker = report_name.strip().split('-')[0]

    return ticker


def get_year_from_report_name(report_name):
    seq_code = report_name.strip().split('-')[1]
    year = int(seq_code.split('_')[0])

    return year
