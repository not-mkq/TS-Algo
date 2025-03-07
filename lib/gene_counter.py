import itertools

def permutations_of_n_elements(lst, n):
    # 使用 itertools.permutations 生成 lst 中任取 n 个元素的所有排列
    permutations = list(itertools.permutations(lst, n))
    # 对生成的排列进行排序
    sorted_permutations = sorted(permutations)
    return list(sorted_permutations)

import numpy as np
class gene_map:
    def __init__(self, elements):
        self.poses = list(range(len(elements) - 1))
        self.genes = permutations_of_n_elements(elements, 2)
        # gmaps
        self.gene_pos_map = np.full((len(self.genes), (len(self.poses))), np.nan)
        self.gene_pos_map_var = np.full((len(self.genes), (len(self.poses))), np.nan)
        self.gene_pos_map_source_num = np.full((len(self.genes), (len(self.poses))), 0)
        self.gene_map = np.full((len(self.genes), 1), np.nan)
        self.gene_map_var = np.full((len(self.genes), 1), np.nan)
        self.gene_map_source_num = np.full((len(self.genes), 1), 0)
        self.data_known = []
    def add_data(self, sequence, value):
        self.data_known.append((sequence, value))
    def gene_in_pos(self, gene, pos, sequence):
        return (sequence[pos] == gene[0] and sequence[pos+1] == gene[1])
    def gene_in(self, gene, sequence):
        re = False
        for pos in self.poses:
            re = re or self.gene_in_pos(gene, pos, sequence)
        return re
    def get_mean(self, data_list):
        if(len(data_list) == 0):
            return np.nan
        values = [data[1] for data in data_list]
        return np.mean(values)
    def get_var(self, data_list):
        if(len(data_list) < 2):
            return np.nan
        values = [data[1] for data in data_list]
        return np.var(values, ddof=1)

    # 或者说这里该加上学习率之类的设定?
    def update_gene_pos_map(self):

        for gene_index, gene in enumerate(self.genes):
            # method B
            data_selected = list(filter(lambda data_item: self.gene_in(gene, data_item[0]), self.data_known))
            self.gene_map[gene_index][0] = self.get_mean(data_selected)
            self.gene_map_var[gene_index][0] = self.get_var(data_selected)
            self.gene_map_source_num[gene_index][0] = len(data_selected)
            for pos in self.poses:
                # method A
                data_selected = list(filter(lambda data_item: self.gene_in_pos(gene, pos, data_item[0]), self.data_known))
                self.gene_pos_map[gene_index][pos] = self.get_mean(data_selected)
                self.gene_pos_map_var[gene_index][pos] = self.get_var(data_selected)
                self.gene_pos_map_source_num[gene_index][pos] = len(data_selected)
        return self.gene_pos_map

    # 对于km来说, 越小越好
    def rank_of_sequence_pred_A(self, sequence):
        mean_all = self.get_mean(self.data_known)
        #print(f"mean_all:{mean_all}")
        rank = 1
        for pos in self.poses:
            for gene_index, gene in enumerate(self.genes):
                if self.gene_in_pos(gene, pos, sequence):
                    if (np.isnan(self.gene_pos_map[gene_index][pos])):
                        gene_buffs = [self.gene_pos_map[gene_index][pos_i] for pos_i in self.poses]
                        #print(f"rank pred A: gene_buffs: {gene_buffs}")
                        gene_buff_filited = list(filter(lambda x: not np.isnan(x), gene_buffs))
                        #print(f"rank pred A: gene_buffs_filited: {gene_buff_filited}")
                        if len(gene_buff_filited) == 0:
                            rank = rank * mean_all
                        else:
                            rank = rank * np.mean(gene_buff_filited)
                        #rank = rank * mean_all
                    else:
                        rank = rank * self.gene_pos_map[gene_index][pos]
        return rank
    def rank_of_sequence_pred_B(self, sequence):
        mean_all = self.get_mean(self.data_known)
        #print(f"mean_all:{mean_all}")
        rank = 1

        for gene_index, gene in enumerate(self.genes):
            if self.gene_in(gene, sequence):
                #if (np.isnan(self.gene_pos_map[gene_index][pos])):
                gene_buff = self.gene_map[gene_index][0]
                #print(self.gene_map)
                if np.isnan(gene_buff):
                    rank = rank * mean_all
                else:
                    rank = rank * gene_buff
                        #rank = rank * mean_all
                    #else:
                        #rank = rank * self.gene_pos_map[gene_index][pos]
        return rank

    # 越大越好
    def rank_of_sequence_unfilled_A(self, sequence):
        rank = 0
        for pos in self.poses:
            for gene_index, gene in enumerate(self.genes):
                if self.gene_in_pos(gene, pos, sequence):
                    if (np.isnan(self.gene_pos_map[gene_index][pos])):
                        rank = rank + 1
        return rank

    def rank_of_sequence_unfilled_B(self, sequence):
        rank = 0
        for gene_index, gene in enumerate(self.genes):
            if self.gene_in(gene, sequence):
                if (np.isnan(self.gene_map[gene_index][0])):
                    rank = rank + 1
        return rank
    # 越小越好
    def rank_of_sequence_source_num_A(self, sequence):
        rank = 0
        for pos in self.poses:
            for gene_index, gene in enumerate(self.genes):
                if self.gene_in_pos(gene, pos, sequence):
                    rank = rank + self.gene_pos_map_source_num[gene_index][pos]
        return rank

    def rank_of_sequence_source_num_B(self, sequence):
        rank = 0
        for gene_index, gene in enumerate(self.genes):
            if self.gene_in(gene, sequence):
                rank = rank + self.gene_map_source_num[gene_index][0]
        return rank

    # 越大越好
    def rank_of_sequence_var_A(self, sequence):
        rank = 0
        for pos in self.poses:
            for gene_index, gene in enumerate(self.genes):
                if self.gene_in_pos(gene, pos, sequence):
                    if np.isnan(self.gene_pos_map_var[gene_index][pos]):
                        return np.nan
                    rank = rank + self.gene_pos_map_var[gene_index][pos]
        return rank

    def rank_of_sequence_var_B(self, sequence):
        rank = 1
        for gene_index, gene in enumerate(self.genes):
            if self.gene_in(gene, sequence):
                #print(f"rank of sequence var B: self.gene_map_var[{gene_index}][0] {self.gene_map_var[gene_index][0]}")
                if np.isnan(self.gene_map_var[gene_index][0]):
                    return np.nan
                rank = rank * self.gene_map_var[gene_index][0]
        return rank

    def map_no_nan_A(self, gmap):
        for pos in self.poses:
            for gene_index, gene in enumerate(self.genes):
                #print(f"map_no_nan: {gmap[gene_index][pos]}")
                if np.isnan(gmap[gene_index][pos]):
                    #print(f"nan!")
                    return False
        return True

    def map_no_nan_B(self, gmap):
        for gene_index, gene in enumerate(self.genes):
            if np.isnan(gmap[gene_index][0]):
                return False
        return True
