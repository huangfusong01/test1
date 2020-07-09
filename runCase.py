#!/usr/bin/python
# -*- coding:utf-8 -*-
#pytest执行入口
import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
print(BASE_PATH)
import sys
sys.path.append(BASE_PATH)
print(sys.path)
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
from common import HTMLTestReportCN
import smtplib
#import pytest
import time
import unittest
#import xmlrunner as xmlrunner
from configs.settings import TESTCASE_PATH,REPORT_PATH
from common.send_email import new_report, report_path, send_email


now = time.strftime("%Y-%m-%d_%H_%M_%S")


def add_case(casePath = TESTCASE_PATH,rule = "test_*.py"):

    '''加载所有的测试用例,构造测试用例集'''
    discover = unittest.defaultTestLoader.discover(casePath,pattern=rule)

    return discover


def run_case(all_case ,reportPath= REPORT_PATH):
    ''' 定义测试报告的地址 '''
    htmlreport = reportPath + '/' + r'%s_test_report.html'%now
    #print(htmlreport)
    with open(htmlreport,'wb') as  f:
        HTMLTestReportCN.HTMLTestRunner(stream=f,verbosity=2,title='parcels接口冒烟测试报告',description='用例执行情况').run(all_case)
        #xmlrunner.XMLTestRunner(output=reportPath).run(all_case)配合jenkins使用时得生成xml文佳

if __name__ == '__main__':

    # -v,-q,-s,分别是pytest框架带的参数
    #-v，详细输出
    #-q，简单输出
    #-s, 输出日志
    #pytest.main(['-v','-s','./test_case/test_case.py','--html=report/{}_report.html'.format(now) ])
    all_case = add_case()#添加测试用例
    run_case(all_case)#执行测试用例
    #发送测试报告
    report = new_report(report_path)
    try:
        send_email(report)
        print('邮件已发送！请查收')
    except smtplib.SMTPException as Error:
        print("Error:邮件发送失败0100")
        print(Error.decode('UTF-8'))
        print("Error:邮件发送失败")



