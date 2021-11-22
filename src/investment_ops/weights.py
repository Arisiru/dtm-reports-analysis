import numpy as np
import scipy


def get_weights(gammas={}, tickers=[], number_of_topics=0, bounds=None):
    # gammas[year][ticker] = normalized
    weights = {}

    for year, tickers_gammas in gammas.items():
        filtered_tickers = []

        for ticker in tickers:
            if ticker in tickers_gammas:
                filtered_tickers.append(ticker)
            else:
                print("Ticker: %s is extra" % ticker)

        A_list = []
        for ticker in filtered_tickers:
            A_list.append(tickers_gammas[ticker])

        A = np.transpose(np.array(A_list))
        x_lstsq_fn_lists = []

        for t in range(number_of_topics):
            b = np.zeros(number_of_topics)
            b[t] = 1.0

            if bounds:
                x_lstsq = scipy.optimize.lsq_linear(A, b, bounds=bounds)
                x_lstsq_fn_lists.append([x for x in x_lstsq['x']])
            else:
                x_lstsq = np.linalg.lstsq(A, b, rcond=None)
                x_lstsq_fn_lists.append([x for x in x_lstsq[0]])

        weights[year] = {}
        for ticker_i, ticker in enumerate(filtered_tickers):
            weights[year][ticker] = []
            for t in range(number_of_topics):
                weights[year][ticker].append(x_lstsq_fn_lists[t][ticker_i])

    # weights[year][ticker] = [weight per topic]
    return weights
