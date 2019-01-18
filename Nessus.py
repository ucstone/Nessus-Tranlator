# coding: utf-8
# !/usr/bin/env python3

import csv
import os, os.path
import sys
import argparse

from WriteExcel import Excel
from log import debug, info, error
from baidu_traslate import *


class Nessus(object):
    """处理Nessus扫描结果"""

    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.all_csv_res = []

        if os.path.isfile(self.csv_name):
            os.chdir(os.path.dirname(os.path.abspath(self.csv_name)))
            self.read_csv(self.csv_name)
        else:
            os.chdir(self.csv_name)
            self.file_list = [file for file in os.listdir() if os.path.isfile(file) and file.endswith('.csv')]
            for file in self.file_list:
                debug(file)
                self.read_csv(file)

    def __len__(self):
        return len(self.all_csv_res)

    def __iter__(self):
        return iter(self.all_csv_res)

    def __next__(self):
        pass

    def read_csv(self, file):
        with open(file, 'r') as csv_file:
            csv_res = csv.reader(csv_file)
            debug(csv_res)
            for row in csv_res:
                debug(row)
                if row not in self.all_csv_res:
                    self.all_csv_res.append(row)
        all_res = self.all_csv_res
        return all_res


def check_risk(risk):
    if risk == 'None':
        return 'None'
    elif risk == 'Low':
        return '低危'
    elif risk == 'Medium':
        return '中危'
    elif risk == 'High':
        return '高危'
    elif risk == 'Critical':
        return '严重'


def get_args():
    parser = argparse.ArgumentParser(prog='nessusor', description='默认在程序目录下生成xls格式文档')
    parser.add_argument("-p", help="输入报告所在目录或Nessus所在的完整路径", type=str)
    parser.add_argument("-s", help="保存的文件名称", type=str)
    args = parser.parse_args()

    return vars(args)


if __name__ == '__main__':
    args = get_args()
    path = args['p']
    output = args['s']

    if path is None or output is None:
        print("""python3 Nessus.py -p /path/nessus.csv or /path -s xxx""")
        sys.exit(0)
    try:

        # nessus = Nessus('/Users/m1k3/127_0_0_1_yi2b5q.csv')
        nessus = Nessus(path)
        new_nessus = []

        for i in nessus:
            risk = check_risk(i[3])
            if risk == 'None':
                pass
            # CVE	CVSS	Risk	Host	Protocol	Port	Name	Synopsis	Description	Solution
            else:
                name = translate(i[7])
                synopsis = translate(i[8])
                description = translate(i[9])
                solution = translate(i[10])

                row = (i[1], i[2], risk, i[4], i[5], i[6], name, synopsis, description, solution)
                # info(list(row))
                new_nessus.append(list(row))

        excel = Excel(output + '.xls', '/Users/m1k3', new_nessus)
        excel.write_data()
    except (Exception,KeyboardInterrupt) as e:
        error(e)
