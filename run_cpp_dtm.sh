# Run the dynamic topic model.
../../cpp/dtm/dtm/main \
 --ntopics=18 \
 --mode=fit \
 --rng_seed=1250139 \
 --initialize_lda=true \
 --corpus_prefix=data_runs/run_18_18/run_18_18 \
 --outname=data_runs/run_18_18/results \
--top_chain_var=0.005 \
--alpha=0.01 \
--lda_sequence_min_iter=6 \
--lda_sequence_max_iter=51 \
--lda_max_em_iter=10

# Run the influence model.
# ../dtm/dtm/main \
#     --mode=fit \
#     --rng_seed=0 \
#     --model=fixed \
#     --initialize_lda=true \
#     --corpus_prefix=run_16_18/run_16_18 \
#     --outname=run_16_18/results \
#     --time_resolution=1 \
#     --influence_flat_years=5 \
#     --top_obs_var=0.5 \
#     --top_chain_var=0.005 \
#     --sigma_d=0.0001 \
#     --sigma_l=0.0001 \
#     --alpha=0.01 \
#     --lda_sequence_min_iter=5 \
#     --lda_sequence_max_iter=30 \
#     --save_time=-1 \
#     --ntopics=18 \
#     --lda_max_em_iter=30

