#!/usr/bin/env python3

#import gene_counter as gc
import lib.data_loader as dl
import lib.arg_parser as ap
import lib.iter_gmap as ig
import sys

clp = ap.command_line_parser()
clp.parse_arguments()
csv_file = clp.get_csv_file()

csv = dl.data_query(csv_file)
batches = clp.get_batches()

all_sequences = csv.get_all_sequences()
elements = ['a', 'b', 'c', 'd', 'e']

mkq_iter = ig.mkq_iteration(elements, all_sequences=all_sequences)

def run_stage(batch):
    for i in range(batch[2]):
        for j in range(batch[0]):
            top_sequences = mkq_iter.iter_explore_B()
            mkq_iter.add_sequences(csv.sequences_to_data(top_sequences))
        for k in range(batch[1]):
            top_sequences = mkq_iter.iter_pred_A()
            mkq_iter.add_sequences(csv.sequences_to_data(top_sequences))
        mkq_iter.show_status(5)

for stage in batches:
    run_stage(stage)

