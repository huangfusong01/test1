#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 获取项目路径
import os


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_PATH)
# 定义测试用例的路径
TESTCASE_PATH =  os.path.join(BASE_PATH,'test_case')
print(TESTCASE_PATH)
#定义测试数据的路径
TESTCASE_EXCLE_PATH =  os.path.join(BASE_PATH,'config','test.xlsx')

# 定义测报告的路径
REPORT_PATH =  os.path.join(BASE_PATH,'report')
print(REPORT_PATH)
# 定义日志文件的路径
LOG_PATH = os.path.join(BASE_PATH,'log/log.txt')

# 连接MysSQL
USER_NAME = 'parcels_test'
USER_PASSWORD = '123456'
DB_IP = '192.168.8.168'
DB_NAME = 'parcels_17feia_merge3'
port = 3306

import pymysql
from common.logger import Logger
logger = Logger().logger

def assertEquals(actual, expected):
    '''
    断言是否相等
    :param actual: 实际值
    :param expected: 期望值
    :return:
    '''
    try:
        assert actual == expected
        logger.info('断言成功,实际值:{} 等于预期值:{}'.format(actual, expected))

    except AssertionError as e:
        logger.info('断言失败,实际值:{} 不等于预期值:{}'.format(actual, expected))
        raise e

def opera_db(order_on):
    expect = 1
    db = pymysql.connect(host=DB_IP, port=3306, user=USER_NAME, passwd=USER_PASSWORD, db=DB_NAME, charset='utf8')
    try:
        with db.cursor() as cursor:

            sql = "SELECT i.orde_order_inside_no,i.is_payed,o.finace_order_no,o.is_payed,p.finance_order_package_no,p.is_payed FROM fina_finance_order_item i LEFT JOIN fina_finance_order o ON i.finance_order_id = o.id LEFT JOIN fina_finance_order_package p ON p.id = o.finance_order_package_id WHERE i.orde_order_inside_no = '{}'".format(order_on)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            for result in results:
                print(result)
                resultStaus =[]
                resultStaus.append(int(result[1][0]))
                resultStaus.append(int(result[3][0]))
                resultStaus.append(int(result[5][0]))
                print(resultStaus)
                assertEquals(resultStaus[0],expect)


    except AssertionError as e:
        print("no search data:{}".format(e))

    finally:
        db.close()



if __name__ == "__main__":
    print(TESTCASE_EXCLE_PATH)