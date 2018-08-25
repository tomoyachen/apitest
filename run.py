# !/usr/bin/python
# -*- coding: UTF-8 -*-
# 执行包：runscript
import unittest

import function.func as func

ApiTest = func.ApiTest()

# test_dir = "C:\\Users\\user\\Desktop\\pythonTest\\apicode\\api4code-master\\case"
FILENAME = 'user.ini'
WHAT = 'task_lists.ini'
WHO = 'try.ini'


"""1.新建测试报告目录"""
ApiTest.reset_report(filename=func.cs.CASE_PATH+FILENAME)
# ApiTest.reset_report(filename=func.cs.CASE_PATH+WHAT)
ApiTest.reset_report(filename=func.cs.CASE_PATH+WHO)

"""2.执行测试用例"""
ApiTest.run_test(filename=func.cs.CASE_PATH+FILENAME)
# ApiTest.run_test(filename=func.cs.CASE_PATH+WHAT)
ApiTest.run_test(filename=func.cs.CASE_PATH+WHO)


"""3.统计测试报告结果"""
ApiTest.write_report_result()
