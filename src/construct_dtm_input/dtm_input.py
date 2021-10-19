import os
import shutil
from reports_ops.reports import get_ticker_from_report_name, get_year_from_report_name


def silent_remove(filename):
    if os.path.exists(filename):
        os.remove(filename)


def construct_data_minus_ticker_input(
        ticker_to_deduct,
        dir_to_base,
        run_code_to_base,
        dir_output,
        run_code):

    dir_run = os.path.join(dir_output, run_code)

    # clone base under new name
    if os.path.exists(dir_run):
        shutil.rmtree(dir_run)

    shutil.copytree(dir_to_base, dir_run)

    amount_documents_in_series_dict = dict()
    documents_name_list = []
    documents_bow_list = []
    reports_mask = []

    # prepare report names and sequence data
    with open(os.path.join(dir_run, run_code_to_base + '-documents.dat'), 'r') as f_r:
        for line in f_r:
            report_name = line.strip()
            report_ticker = get_ticker_from_report_name(
                report_name)
            report_year = get_year_from_report_name(
                report_name)

            if report_ticker == ticker_to_deduct:
                reports_mask.append(False)
            else:
                documents_name_list.append(report_name)
                reports_mask.append(True)
                if report_year not in amount_documents_in_series_dict:
                    amount_documents_in_series_dict[report_year] = 0
                amount_documents_in_series_dict[report_year] += 1

    # prepare reports bow data
    with open(os.path.join(dir_run, run_code_to_base + '-mult.dat'), 'r') as f_r:
        for line in f_r:
            report_bow = line.strip()
            documents_bow_list.append(report_bow)

    # store new data
    # store seq.dat
    with open(os.path.join(dir_run, run_code + '-seq.dat'), 'w') as f:
        f.write("%s\n" % len(amount_documents_in_series_dict.keys()))
        for year in sorted(amount_documents_in_series_dict.keys()):
            f.write("%s\n" % amount_documents_in_series_dict[year])

    # store documents.dat
    with open(os.path.join(dir_run, run_code + '-documents.dat'), 'w') as f:
        for document in documents_name_list:
            f.write("%s\n" % document)

    # store mult.dat
    with open(os.path.join(dir_run, run_code + '-mult.dat'), 'w') as f:
        for i, document in enumerate(documents_bow_list):
            if reports_mask[i]:
                f.write("%s\n" % document)

    # remove staff
    shutil.rmtree(os.path.join(dir_run, 'interpretation'))
    silent_remove(os.path.join(
        dir_run, run_code_to_base + '-industry-returns.csv'))
    silent_remove(os.path.join(dir_run, run_code_to_base + '-mult.dat'))
    silent_remove(os.path.join(dir_run, run_code_to_base +
                  '-preprocesssing_settings.dat'))
    silent_remove(os.path.join(dir_run, run_code_to_base + '-returns.csv'))
    silent_remove(os.path.join(dir_run, run_code_to_base + '-terms.dat'))
    silent_remove(os.path.join(dir_run, run_code_to_base + '-documents.dat'))
    silent_remove(os.path.join(dir_run, run_code_to_base + '-seq.dat'))

    # recreate staff
    os.makedirs(os.path.join(dir_run, 'interpretation'))

    print("Run data is prepared for %s" % ticker_to_deduct)

    return True
