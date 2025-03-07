#!/usr/bin/env python3

import lib.data_loader as dl
import lib.arg_parser as ap
import lib.iter_gmap as ig
import sys

clp = ap.command_line_parser()
clp.parse_arguments()
csv_file = clp.get_csv_file()

csv = dl.data_query(csv_file)
#batches = clp.get_batches()

all_sequences = csv.get_all_sequences()
elements = ['a', 'b', 'c', 'd', 'e', 'f']

mkq_iter = ig.mkq_iteration(elements, all_sequences=all_sequences)

def run_stage():
    top_sequences = mkq_iter.iter_random(4)
    mkq_iter.add_sequences(csv.sequences_to_data(top_sequences))
    mkq_iter.show_status(5)

for stage in range(25):
    run_stage()
