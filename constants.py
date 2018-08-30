#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 脚本功能：全部变量

import sys
import time
from imp import reload

reload(sys)


TEST_URL ='https://uathome.uuabc.com/'

REPORT_NAME = 'Test report'
TITLE = '所有数据准备SQL'

METHOD = 'method'
URL = 'url'
DATA = 'data'
NAME = 'name'
NUMBER = 'number'
CODE = 'code'
HEADERS = 'headers'
REPORT = 'report'
R_NAME = 'reportName'

REPORT_PATH = "C:\\Users\\Administrator\\PycharmProjects\\apitest\\report\\docs\\"
YML_REPORT = "C:\\Users\\Administrator\\PycharmProjects\\apitest\\report\mkdocs.yml"


CASE_PATH = "C:\\Users\\Administrator\\PycharmProjects\\apitest\\case\\"

#测试报告内容
API_TEST_FAIL = """
```
 %s Case Fail
 Number: %s
 Method: %s
 Url: %s
 Headers:
 %s
 Data : 
 %s
 expected code : %s
 actual code : %s
 response : %s
```
"""

API_TEST_SUCCESS = """
```
 %s Case Pass
 Number: %s
 Method: %s
 Url: %s
 Headers:
 %s
 Data : 
 %s
期望值 : %s
实际值 : %s
 response : %s
```
"""

#报告结果统计
RESULT_CONTENT = """
测试结果如下：
<table border="3" width="500px">
  <tr>
    <th style="color: #787878">All</th>
    <th style="color: #3cc8b4">Pass</th>
    <th style="color: #FFB5C5">Fail</th>
  </tr>
  <tr>
    <th style="color: #787878">%s</th>
    <th style="color: #3cc8b4">%s</th>
    <th style="color: #FFB5C5">%s</th>
  </tr>
</table>
"""
NOW = '_' + time.strftime('%Y%m%d', time.localtime(time.time())) + '.md'
PROJECT_TIME = time.strftime('%Y%m%d', time.localtime(time.time()))