import argparse

class command_line_parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Process some parameters and batches.')
        self.configure_arguments()
        self.args = None

    def configure_arguments(self):
        # 定义需要解析的参数
        self.parser.add_argument('--csv', type=str, required=True, help='CSV file composed with sequences and km values.')
        self.parser.add_argument('batches', metavar='N', type=int, nargs='+',
                                 help='A list of integers representing batches')

    def parse_arguments(self):
        # 解析命令行输入的参数
        self.args = self.parser.parse_args()
        return self.args

    def get_csv_file(self):
        return self.args.csv
    def get_batches(self):
        batches = [] # [(4, 0, 3), (4, 0, 3), (4, 0, 3), (3, 1, 3), (3, 1, 3)]

        for exp in self.args.batches:
            batches.append((exp, 4-exp, 3))
        return batches
