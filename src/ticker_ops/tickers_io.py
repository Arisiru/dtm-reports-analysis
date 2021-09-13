def get_tickers(fileName):
    tickers = set()
    with open(fileName, 'r') as f:
        for text in f:
            tickers.add(text.strip())

    return sorted(tickers)


def get_processed_tickers(fileName):
    tickers = set()
    with open(fileName, 'r') as f:
        for text in f:
            tickers.add(text.strip())

    return tickers


def update_processed_tickers(ticker, tickers, fileName):
    tickers.add(ticker)
    with open(fileName, 'w') as f:
        for processed_ticker in sorted(tickers):
            f.write('%s\n' % processed_ticker)

    return tickers


def update_errors_tickers(ticker, fileName):
    with open(fileName, 'a') as f:
        f.write('%s\n' % ticker)

    return None
