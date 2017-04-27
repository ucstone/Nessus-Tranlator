# coding: utf-8
# !/usr/bin/env python
reload(__import__('sys')).setdefaultencoding('utf-8')
from baidu_traslate import *
import time

# 保存文件。
def csv_to_txt(vul_names, new_nessus, res_name='result'):
    res = open(res_name+'.txt', 'w+')
    for vul_name in vul_names:  # 遍历漏洞名
        host_list = []  # 影响主机列表，一个漏洞影响多个主机
        cve_list = []  # 漏洞的cve列表，一个漏洞对应多个CVE编号
        for new_vul in new_nessus:  # 提取每个漏洞对应的影响主机，提取对应的cve编号
            if new_vul[7] == vul_name.split(',,')[2]:
                host_list.append(new_vul[4])
                cve_list.append(new_vul[1])
                # print new_vul[1]

        name = vul_name.split(',,')[2]
        hosts = ','.join(list(set(host_list)))
        port = u'影响端口: ' + vul_name.split(',,')[1]
        cves = ','.join(list(set(cve_list)))
        Description = vul_name.split(',,')[3].replace('\n', ' ')
        Solution = vul_name.split(',,')[4].replace('\n', ' ')

        # 执行翻译功能
        tranlsate_info = name + '\t------------\t' + Description.replace('\n',' ') + '\t------------\t' + Solution.replace('\n', ' ')
        time.sleep(3)
        cn_res = translate(tranlsate_info).split('------------')
        print cn_res
        print len(cn_res)
        cn_name = cn_res[0]
        cn_Description = cn_res[1]
        cn_Solution = cn_res[2]

        write_name = u'漏洞名称: ' + cn_name
        write_risk = u'风险级别: '+ vul_name.split(',,')[0]
        write_host = u'影响主机: ' + hosts
        write_cve = u'CVE编号: ' + cves
        write_Des = u'漏洞描述: ' + cn_Description
        write_Solution = u'修复方案: ' + cn_Solution

        res.writelines(write_name + '\n')
        res.writelines(write_risk + '\n')
        res.writelines(write_host + '\n')
        res.writelines(port + '\n')
        res.writelines(write_cve + '\n')
        res.writelines(write_Des + '\n')
        res.writelines(write_Solution + '\n')
        res.writelines('\n')

    res.close()