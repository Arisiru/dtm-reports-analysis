import os


def run(t=5, dtm_path='..', data_path='..', init_lda=False, seed=193748, run_code='data', iter_lda_min=1, iter_lda_max=1, iter_lda_em_max=1):
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
        dtm_path,
        t,
        seed,
        'true' if init_lda else 'false',
        os.path.join(data_path, run_code, run_code),
        os.path.join(data_path, run_code, 'results'),
        iter_lda_min,
        iter_lda_max,
        iter_lda_em_max
    )

    return os.system(command)
