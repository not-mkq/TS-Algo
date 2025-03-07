
import pandas as pd

class data_query:
    def __init__(self, filename):
        # 自动检测列数，不设置列名
        self.df = pd.read_csv(filename, header=None)

    def find_value(self, order):
        # 检查数组长度是否正确
        if len(order) != self.df.shape[1] - 1:
            print("Error: The length of the input array must be exactly one less than the number of columns in the table.")
            return None

        # 遍历DataFrame每一行，检查是否匹配
        for index, row in self.df.iterrows():
            if all(row[i] == order[i] for i in range(len(order))):
                return row.iloc[-1]
        return None
    
    def get_all_sequences(self):
        # 返回所有行的前n-1个元素构成的列表
        return self.df.iloc[:, :-1].values.tolist()

    def get_all_values(self):
        # 返回所有行的最后一个元素构成的列表
        return self.df.iloc[:, -1].tolist()
    def get_all_data(self):
        all_data = []
        all_sequences = self.get_all_sequences()
        for sequence in all_sequences: #gc.permutations_of_n_elements(elements, len(elements)):
            value = self.find_value(sequence)
            if value != None:
                all_data.append((sequence, value))
        return all_data

    def sequences_to_data(self, sequences):
        data = []
        for sequence in sequences:
            value = self.find_value(sequence)
            if value != None:
                data.append((sequence, value))
        return data
# 示例使用
# query = DataQuery('yourfile.csv')
# value = query.find_value(['a', 'b', 'c', 'd'])  # 正确长度
# print(value)

### test ###

# import sys

# csv_file = sys.argv[1]
# csv = data_query(csv_file)
# print(f"csv all sequences({len(csv.get_all_sequences())}): \n{csv.get_all_sequences()}")
# a = csv.find_value(['a', 'b', 'd', 'e', 'c'])
# print(f"km of sequence {['a', 'b', 'd', 'e', 'c']}: \nkm: {a}")
