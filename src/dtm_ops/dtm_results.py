from reports_ops.reports import get_ticker_from_report_name, get_year_from_report_name
import os
import numpy as np


def get_reports(dtm_path='..', run_prefix=''):
    """
        report = {
            'name': 'test',
            'length': 10,
            'year': 2009,
            'ticker': 'test'
        }
    """

    reports_list = []
    with open(os.path.join(dtm_path, "%s-documents.dat" % run_prefix), 'r') as f_r:
        for text_line in f_r:
            report_name = text_line.strip()
            if len(report_name):
                reports_list.append(report_name)

    report_length = []
    with open(os.path.join(dtm_path, "%s-mult.dat" % run_prefix), 'r') as f_r:
        for text_line in f_r:
            bow = text_line.strip()
            if len(bow):
                report_length.append(int(bow.split(' ')[0]))

    reports = []
    for i, report_name in enumerate(reports_list):
        report = {
            'name': report_name,
            'length': report_length[i],
            'year': get_year_from_report_name(report_name),
            'ticker': get_ticker_from_report_name(report_name)
        }
        reports.append(report)

    return reports


def get_gammas(reports=[], dtm_path='..', number_of_topics=1, weght_by_report_length=False):
    gamma_for_reports = {}
    with open(os.path.join(dtm_path, 'results', 'lda-seq', 'gam.dat'), 'r') as f_r:
        distributions = f_r.readlines()
        report_id = 0
        # for each term read one line
        for report in reports:
            # for each topic
            normalization_sum = 0
            topics_probabilities = []
            topics_probabilities_normalize = []

            for _topic in range(number_of_topics):
                float_text = distributions[report_id].strip()

                topic_probability = None
                if weght_by_report_length:
                    topic_probability = float(float_text) * report['length']
                else:
                    topic_probability = float(float_text)

                topics_probabilities.append(topic_probability)
                normalization_sum += topic_probability
                report_id += 1

            for prob in topics_probabilities:
                topics_probabilities_normalize.append(prob / normalization_sum)
            gamma_for_reports[report['name']] = topics_probabilities_normalize

    return gamma_for_reports


def aggregate_gammas(gammas={}, reports=[]):
    reports_dict = {}
    final_gammas = {}
    for report in reports:

        if report['ticker'] not in reports_dict:
            reports_dict[report['ticker']] = {}
        if report['year'] not in reports_dict[report['ticker']]:
            reports_dict[report['ticker']][report['year']] = []

        reports_dict[report['ticker']][report['year']].append(
            gammas[report['name']])

    for ticker, reports_by_years in reports_dict.items():
        for year, reports in reports_by_years.items():
            m = np.array(reports)
            means = m.mean(axis=0)
            normalized = means / np.sum(means)

            if year not in final_gammas:
                final_gammas[year] = {}

            final_gammas[year][ticker] = normalized

    return final_gammas
