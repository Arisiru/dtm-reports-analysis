import os

SUCCESS_CODE = 0

DIRS = {}
DIRS['root'] = '..'
DIRS['experiment'] = os.path.join(DIRS['root'], 'data_n-1_experiment')

FILES = {}
FILES['errors tickers'] = os.path.join(
    DIRS['experiment'], 'errored_tickers.dat')
FILES['processed tickers'] = os.path.join(
    DIRS['experiment'], 'processed_tickers.dat')
FILES['all tickers'] = os.path.join(
    DIRS['experiment'], 'all_tickers.dat')
FILES['dtm command'] = os.path.join(
    DIRS['root'], DIRS['root'], DIRS['root'], 'cpp', 'dtm', 'dtm', 'main')


def get_tickers():
    tickers = set()
    with open(FILES['all tickers'], 'r') as f:
        for text in f:
            tickers.add(text.strip())

    return sorted(tickers)


def get_processed_tickers():
    tickers = set()
    with open(FILES['processed tickers'], 'r') as f:
        for text in f:
            tickers.add(text.strip())

    return tickers


def update_processed_tickers(ticker, tickers):
    tickers.add(ticker)
    with open(FILES['processed tickers'], 'w') as f:
        for processed_ticker in sorted(tickers):
            f.write('%s\n' % processed_ticker)

    return tickers


def update_errors_tickers(ticker):
    with open(FILES['errors tickers'], 'a') as f:
        f.write('%s\n' % ticker)

    return None


def construct_dtm_run_without_ticker(ticker):
    data = {}
    # todo implement construction
    # void
    return data


def run_dtm(ticker, n=22, init_lda=False, seed=193748, prefix='19_22', iter_lda_min=1, iter_lda_max=1, iter_lda_em_max=1):
    run_code = 'run_%s-%s' % (prefix, ticker)
    command = '%s \
        --ntopics=%s \
        --mode=fit \
        --rng_seed=%s \
        --initialize_lda=%s \
        --corpus_prefix=%s \
        --outname=%s \
        --top_chain_var=0.015 \
        --alpha=0.01 \
        --lda_sequence_min_iter=%s \
        --lda_sequence_max_iter=%s \
        --lda_max_em_iter=%s' % (
        FILES['dtm command'],
        n,
        seed,
        'true' if init_lda else 'false',
        os.path.join(DIRS['experiment'], run_code, run_code),
        os.path.join(DIRS['experiment'], run_code, 'results'),
        iter_lda_min,
        iter_lda_max,
        iter_lda_em_max
    )

    return os.system(command)


tickers = get_tickers()
processed_tickers = get_processed_tickers()

for ticker in tickers:
    if ticker in processed_tickers:
        continue

    construct_dtm_run_without_ticker(ticker)
    if run_dtm(ticker) == SUCCESS_CODE:
        processed_tickers = update_processed_tickers(ticker, processed_tickers)
    else:
        print('Return form run %s' % ticker)
        update_errors_tickers(ticker)


# EOF
