import pandas as pd
import numpy as np


def get_return_on_investment(path_return_coeficients='', weights={}, tickers=[], number_of_topics=0, year_series=[], initial_amount_to_invest=1):
    # weights[year][ticker] = [weight per topic]

    df_returns_koef = pd.read_csv(path_return_coeficients)
    df_returns_koef.rename(index=str, columns={
                           'Unnamed: 0': 'Date'}, inplace=True)
    df_returns_koef['Date'] = pd.to_datetime(df_returns_koef['Date'])

    df_returns_invest = df_returns_koef[['Date']].copy()

    topic_names = ['Topic %s' % i for i in range(number_of_topics)]

    for topic_id in range(number_of_topics):
        investition = initial_amount_to_invest
        return_year_topic_invest = []

        for year in year_series:
            current_year = year + 1
            topic_name = 'Topic %s' % topic_id

            df_weights = pd.DataFrame.from_dict(
                weights[year], orient='index', columns=topic_names)
            weights_topic_year = df_weights[topic_name].to_numpy()

            return_year_stocks_koef = (
                df_returns_koef[df_returns_koef['Date'].dt.year == current_year][tickers]).to_numpy()
            return_year_topic_koef = return_year_stocks_koef.dot(
                np.transpose(weights_topic_year))

            for koef in return_year_topic_koef:
                investition *= koef
                return_year_topic_invest.append(investition)

        df_returns_invest[topic_names[topic_id]] = return_year_topic_invest

    df_returns_invest.set_index('Date', inplace=True)
    # print(df_returns_invest.tail())

    return df_returns_invest


def get_final_return(returns={}, number_of_topics=0):
    final_returns = []
    for topic_id in range(number_of_topics):
        final_returns.append(
            returns['Topic %s' % topic_id][len(returns['Topic %s' % topic_id]) - 1])

    return final_returns
