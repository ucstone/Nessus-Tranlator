# coding: utf-8
# !/usr/bin/env python
reload(__import__('sys')).setdefaultencoding('utf-8')
import csv
import os, os.path
import sys
from lib.translator_excel import *
from lib.translator_txt import *
import argparse


def read_csv(file_path):
    # 要转换的Nessus导出的csv文档
    with open(file_path, 'rb') as f:
        nessus = csv.reader(f)
        vules = [] # 风险级别，漏洞名， 端口, 描述，解决方案
        new_nessus = [] # 存放存在CVE漏洞编号且风险级别大于LOW的漏洞

        zz = [row for row in nessus] #判断是否为Nessus导出的csv
        check_csv = ['Plugin ID', 'CVE', 'CVSS', 'Risk', 'Host', 'Protocol', 'Port', 'Name', 'Synopsis', 'Description',\
                     'Solution', 'See Also', 'Plugin Output']
        if zz[0] != check_csv:
                print u'非Nessus导出结果文件'
                sys.exit()

        for row in zz:
            if len(row[1]) > 3 and row[3] in ['Critical', 'High', 'Medium']:
                # 1cve 4host 7name 9description 10solution
                risk_name = row[3] + ',,' + row[6] + ',,' + row[7] + ',,' + row[9] + ',,' + row[10] # risk port name des solu
                vules.append(risk_name)
                new_nessus.append(row)
        # print list(set(vules))
        # 漏洞名称去重操作
        vul_names = list(set(vules))
        # print vul_names
        return vul_names,new_nessus
        # print len(vul_names)

def get_args():
    parser = argparse.ArgumentParser(prog='nessusor', description=u'默认在程序目录下生成xls格式文档')
    parser.add_argument("-path", help=u"输入报告所在目录", type=str)
    parser.add_argument("-type", help=u"转换器转换为文本文档(txt)或者Excel(xls)，默认生成在程序路径下", type=str)
    args = parser.parse_args()

    return vars(args)

if __name__ == "__main__":
    args = get_args()
    current_path = args['path']
    output_type = args['type']

    if current_path is None or output_type is None:
        print """
            Usage: nessusor -path "d:\\nessus csv" -type txt 
            help : nessusor -h
            Author QQ: 2778695270
            """
        sys.exit(0)

    files = []
    # print current_path
    if os.path.exists(current_path) == False:
        print u'{}目录不存在'.format(current_path)
        sys.exit(1)

    if os.path.exists(current_path):
        for csv_file in os.listdir(current_path):
            # print csv_file
            if csv_file.endswith('.csv'):
                files.append(csv_file)

    if output_type == "txt":
        for file_path in files:
            vul_names, new_nessus = read_csv(current_path + os.path.sep + file_path)
            # 输出到txt文档
            csv_to_txt(vul_names, new_nessus, file_path.split('.')[0])
        sys.exit(1)
    elif output_type == "xls":
        for file_path in files:
            vul_names, new_nessus = read_csv(current_path + os.path.sep + file_path)
            # 输出到excel文档
            csv_to_excel(vul_names, new_nessus, file_path.split('.')[0])
        sys.exit(1)