from . import gene_counter as gc
import random
class mkq_iteration:
    def __init__(self, elements, all_sequences = None):
        self.tested_sequence = []
        self.tested_data = []
        self.elements = elements
        if all_sequences == None:
            self.all_sequences = gc.permutations_of_n_elements(elements, len(elements))
        else:
            self.all_sequences = all_sequences

        self.gmap = gc.gene_map(elements)

    def iter_explore_A(self, number = 1):
        untested_sequences = list(filter(lambda sequence: sequence not in self.tested_sequence, self.all_sequences))
        random.shuffle(untested_sequences)

        if(self.gmap.map_no_nan_A(self.gmap.gene_pos_map_var)):
            sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_var_A)
            top_sequences = sorted_sequences[-number:]
        elif(self.gmap.map_no_nan_A(self.gmap.gene_pos_map)):
            sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_source_num_A)
            top_sequences = sorted_sequences[:number]
        else:
            sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_unfilled_A)
            top_sequences = sorted_sequences[-number:]
        return top_sequences

    def iter_explore_B(self, number = 1):
        untested_sequences = list(filter(lambda sequence: sequence not in self.tested_sequence, self.all_sequences))
        random.shuffle(untested_sequences)

        if(self.gmap.map_no_nan_B(self.gmap.gene_map_var)):
            sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_var_B)
            top_sequences = sorted_sequences[-number:]
        elif(self.gmap.map_no_nan_B(self.gmap.gene_map)):
            sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_source_num_B)
            top_sequences = sorted_sequences[:number]
        else:
            sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_unfilled_B)
            top_sequences = sorted_sequences[-number:]
        return top_sequences

    def iter_explore_mixed(self, number = 1):
        untested_sequences = list(filter(lambda sequence: sequence not in self.tested_sequence, self.all_sequences))
        random.shuffle(untested_sequences)
        if all(self.gmap.rank_of_sequence_unfilled_A(x) == 0 for x in untested_sequences):
            if(self.gmap.map_no_nan_B(self.gmap.gene_map_var)):
                sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_var_B)
                top_sequences = sorted_sequences[-number:]
            elif(self.gmap.map_no_nan_B(self.gmap.gene_map)):
                sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_source_num_B)
                top_sequences = sorted_sequences[:number]
            else:
                sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_unfilled_B)
                top_sequences = sorted_sequences[-number:]
        else:
            sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_unfilled_A)
            top_sequences = sorted_sequences[-number:]
        return top_sequences
    def iter_pred_A(self, number = 1):
        untested_sequences = list(filter(lambda sequence: sequence not in self.tested_sequence, self.all_sequences))
        random.shuffle(untested_sequences)
        sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_pred_A)
        top_sequences = sorted_sequences[:number]
        #print(f"iter_pred_A: {list(map(self.gmap.rank_of_sequence_pred_A, sorted_sequences))}")
        return top_sequences

    def iter_pred_B(self, number = 1):
        untested_sequences = list(filter(lambda sequence: sequence not in self.tested_sequence, self.all_sequences))
        random.shuffle(untested_sequences)
        sorted_sequences = sorted(untested_sequences, key = self.gmap.rank_of_sequence_pred_B)
        top_sequences = sorted_sequences[:number]

        return top_sequences

    def iter_random(self, number = 1):
        untested_sequences = list(filter(lambda sequence: sequence not in self.tested_sequence, self.all_sequences))
        random.shuffle(untested_sequences)
        top_sequences = untested_sequences[:number]
        return top_sequences

    def add_sequences(self, data_array):
        for data in data_array:
            sequence, value = data
            self.gmap.add_data(sequence, value)
            self.tested_data.append(data)
            self.tested_sequence.append(sequence)
        self.gmap.update_gene_pos_map()

    def show_status(self, best_n):
        sorted_tested = sorted(self.tested_data, key= lambda data: data[1])
        print(f"{len(self.tested_data)},", end="")
        for index in range(min(len(sorted_tested), best_n)):
            print(f"{sorted_tested[index][1]},", end="")
        print("")
