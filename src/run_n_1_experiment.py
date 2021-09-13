import os
from construct_dtm_input.dtm_input import construct_data_minus_ticker_input
from ticker_ops import tickers_io
from dtm_ops import run_dtm

SUCCESS_CODE = 0
RUN_TO_BASE = 'run_19-ext_22'
T = 22

DIRS = {}
DIRS['root'] = '..'
DIRS['experiment'] = os.path.join(DIRS['root'], 'data_n-1_experiment')
DIRS['run to base'] = os.path.join(DIRS['root'], 'data_runs', RUN_TO_BASE)


FILES = {}
FILES['errors tickers'] = os.path.join(
    DIRS['experiment'], 'errored_tickers.dat')
FILES['processed tickers'] = os.path.join(
    DIRS['experiment'], 'processed_tickers.dat')
FILES['all tickers'] = os.path.join(
    DIRS['experiment'], 'all_tickers.dat')
FILES['dtm command'] = os.path.join(
    DIRS['root'], DIRS['root'], DIRS['root'], 'cpp', 'dtm', 'dtm', 'main')


tickers = tickers_io.get_tickers(FILES['all tickers'])
processed_tickers = tickers_io.get_processed_tickers(
    FILES['processed tickers'])

for ticker in tickers:
    if ticker in processed_tickers:
        continue

    run_code = 'run-%s' % ticker

    construct_data_minus_ticker_input(
        ticker,
        DIRS['run to base'],
        DIRS['experiment'],
        run_code)

    if run_dtm.run(
            t=T,
            dtm_path=FILES['dtm command'],
            data_path=DIRS['experiment'],
            run_code=run_code) == SUCCESS_CODE:

        processed_tickers = tickers_io.update_processed_tickers(
            ticker,
            processed_tickers,
            FILES['processed tickers'])
    else:
        print('Return form run %s' % ticker)
        tickers_io.update_errors_tickers(ticker, FILES['errors tickers'])


# EOF
