# coding: utf-8
# !/usr/bin/env python3
import os

from xlwt import *
from log import debug, info, error


class Excel(object):
    """将Nessus数据写入Excel"""

    headers = ['CVE编号', 'CVSS评分', '风险值', '主机', '协议', '端口', '漏洞名称', '漏洞概述', '描述', '解决方案']

    def __init__(self, excel_name, excel_path, vul_data):
        self.excel_name = excel_name
        self.excel_path = excel_path
        self.vul_data = vul_data

    def write_data(self):
        self.wbook = Workbook()
        self.wsheet = self.wbook.add_sheet('扫描结果')

        # 设置excel的格式
        col_style = easyxf(
            'font: bold on; align: wrap on, vert centre, horiz center')  # ('font: name Times New Roman, color-index black, bold on')
        row_style = easyxf('align: wrap on, vert centre, horiz center')
        fnt = Font()
        fnt.height = 2 * 20
        style = XFStyle()
        style.font = fnt

        row = 0
        for rows in self.vul_data:
            # info(rows)
            col = 0
            if row == 0:
                for column in self.headers:
                    self.wsheet.write(row, col, column, row_style)
                    col += 1
                row += 1
            else:
                for column in rows:
                    self.wsheet.write(row, col, column)
                    col += 1
                row += 1
        self.wbook.save(self.excel_name)
