# coding: utf-8
# !/usr/bin/env python
reload(__import__('sys')).setdefaultencoding('utf-8')

import time

from baidu_traslate import *
from xlwt import *


def csv_to_excel(vul_names, new_nessus, file_name= 'result'):
    cols_name = [u'漏洞名称', u'影响主机', u'端口', u'CVE编号', u'风险级别', u'漏洞描述', u'修复方案']
    wbook = Workbook()
    # print file_name.encode('utf-8')
    wsheet = wbook.add_sheet('sheet')

    # 设置excel的格式
    col_style = easyxf('font: bold on; align: wrap on, vert centre, horiz center')#('font: name Times New Roman, color-index black, bold on')
    row_style = easyxf('align: wrap on, vert centre, horiz center')
    fnt = Font()
    fnt.height = 2 * 20
    style = XFStyle()
    style.font = fnt

    row_info = []
    for vul_name in vul_names:  # 遍历漏洞名
        host_list = []  # 影响主机列表，一个漏洞影响多个主机
        cve_list = []  # 漏洞的cve列表，一个漏洞对应多个CVE编号
        for new_vul in new_nessus:  # 提取每个漏洞对应的影响主机，提取对应的cve编号
            if new_vul[7] == vul_name.split(',,')[2]:
                host_list.append(new_vul[4])
                cve_list.append(new_vul[1])
                # print new_vul[1]

        name = vul_name.split(',,')[2]
        hosts = '\n'.join(list(set(host_list)))
        port = vul_name.split(',,')[1]
        cves = '\n'.join(list(set(cve_list)))
        risk = vul_name.split(',,')[0]
        Description = vul_name.split(',,')[3]#.replace('\n', ' ')
        Solution = vul_name.split(',,')[4]#.replace('\n', ' ')
        tranlsate_info = name+'\t------------\t'+Description.replace('\n', ' ')+'\t------------\t'+Solution.replace('\n', ' ')
        time.sleep(3)
        cn_res = translate(tranlsate_info).split('------------')
        print cn_res
        print len(cn_res)
        cn_name = cn_res[0]
        cn_Description = cn_res[1]
        cn_Solution = cn_res[2]
        # print tranlsate
        print '--'*50
        # row_info.append(list((name, hosts, cves, risk, Description, Solution)))
        row_info.append(list((cn_name, hosts, port, cves, risk, cn_Description, cn_Solution)))


    #写入Excel操作
    for row in row_info:
        for row_num in xrange(len(row_info) + 1):
            for col_num in xrange(len(cols_name)):
                    if row_num == 0:
                        try:
                            wsheet.write(row_num, col_num, cols_name[col_num], col_style)
                        except:
                            pass
                    else:
                        try:
                            wsheet.write(row_num, col_num, row[col_num], row_style)
                            wsheet.row(col_num).set_style(style)
                            wsheet.col(col_num).width = 0x2400 + col_num
                        except:
                            pass
    wbook.save(file_name+'.xls')