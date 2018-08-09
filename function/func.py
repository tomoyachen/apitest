#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 业务包：通用函数
import json
import time
import core.mysql as mysql
import core.log as log
import core.request as request
import core.config as conf
import constants as cs
import os
import requests

logging = log.get_logger()


class ApiTest:
	"""接口测试业务类"""

	def __init__(self):
		pass

	def prepare_data(self, host, user, password, db, sql):
		"""
		数据准备，添加测试数据
		:param host: 服务地址
		:param user: 用户
		:param password: 密码
		:param db: 数据库名
		:param sql: 执行的SQL
		:return:
		"""
		mysql.connect(host, user, password, db)
		res = mysql.execute(sql)
		mysql.close()
		logging.info("Run sql: the row number affected is %s" % res)
		return res

	def get_prepare_sql(self, filename, key):
		"""
		获取预备执行的SQL
		:param title: 配置文件头信息
		:param key: 配置文件值
		:return: Value
		"""
		try:
			conf.get_config(filename)
			value = conf.get_data(title=cs.TITLE, key=key)
			return value
		except Exception as e:
			logging.error("获取用例参数值失败 %s" % e)

	def reset_report(self, filename):
		"""
		这个方法主要是通过写入文件的方法，先打开cs.YML_REPORT也就是
		mkdocs.yml文件，判断文件中是否存在当前写入的内容。
		:param filename: 测试用例文件
		:return: 测试报告内容
		"""
		try:
			result = os.path.exists(cs.REPORT_PATH)
			if result == True:
				conf.get_config(filename)
				reportName = eval(conf.get_data(title=cs.REPORT_NAME, key=cs.REPORT))
				report_name = eval(conf.get_data(title=cs.REPORT_NAME, key=cs.R_NAME))
				# print(report_name)

				file = open(cs.YML_REPORT, 'r+')
				list_con = file.readlines()
				content = eval(str(list_con).encode("unicode-escape"))
				fileContent = "- [%s, %s]"
				row = "\n"
				_content = fileContent % (reportName + cs.NOW, report_name)
				con = row + _content

				if fileContent % (reportName + cs.NOW, report_name) not in content:
					f = open(cs.YML_REPORT, 'a+',encoding="utf-8")
					f.write(con)
				else:
					logging.info("内容已经存在 %s" % _content)
		except Exception as e:
			logging.error("3文件路径不存在 %s", e)

	def write_report(self, content):
		"""
		这个方法用于书写测试报告从而解决之前的通过
		logging方式写入导致其他的日志无法实现写入
		:param content: 传入文件的内容
		:return: None
		"""
		reportName = eval(str.encode(conf.get_data(title=cs.REPORT_NAME, key=cs.REPORT)))
		_reportName = reportName + cs.NOW
		filename = cs.REPORT_PATH + _reportName
		# print(filename)
		try:
			file = open(filename, 'a+',encoding="utf-8")
			file.writelines(content)
			file.close()
		except Exception as e:
			logging.error("2文件路径不存在 %s", e)

	def execute_case(self, filename):
		"""
		执行接口测试用例的方法
		:param filename: 用例文件名称
		:return: 测试结果
		"""
		conf.get_config(filename)
		list = eval(conf.get_title_list())
		# print("zheshi"+list)

		for i in range(1, len(list)):
			title = list[i]
			number = conf.get_data(title, key=cs.NUMBER)
			name = conf.get_data(title, key=cs.NAME)
			method = conf.get_data(title, key=cs.METHOD)
			url = conf.get_data(title, key=cs.URL)
			data = eval(conf.get_data(title, key=cs.DATA))
			_data = request.json.dumps(data, ensure_ascii=False, indent=4)
			headers = eval(conf.get_data(title, key=cs.HEADERS))
			_headers = request.json.dumps(headers, ensure_ascii=False, indent=4)
			testUrl = cs.TEST_URL + url
			actualCode = requests.request(method, testUrl, data=data, headers=headers)
			expectCode = conf.get_data(title, key=cs.CODE)
			# print(actualCode.status_code)
			response = json.loads(actualCode.text)
			if response["msg"] != expectCode:
				logging.info("新增一条接口失败报告")
				# response = json.loads(actualCode.text)
				# print(response)
				self.write_report(
					cs.API_TEST_FAIL % (name, number, method, testUrl, _headers, _data, expectCode, response["msg"],response))

			else:
				logging.info("新增一条接口成功报告")
				self.write_report(
					cs.API_TEST_SUCCESS % (name, number, method, testUrl, _headers, _data, expectCode, response["msg"],response))


	def run_test(self, filename):
		"""
		普通接口测试类方法
		:param filename: 接口的用例name
		:return: 测试报告
		"""
		reportName = eval(str.encode(conf.get_data(cs.REPORT_NAME, cs.REPORT)))
		_filename = cs.REPORT_PATH + str(reportName) + cs.NOW
		# fb = open(_filename, "wb+")
		try:
			if os.path.exists(_filename):
				os.remove(_filename)
				self.execute_case(filename)
				time.sleep(2)
			else:
				self.execute_case(filename)
		except Exception as e:
			logging.error("执行接口测试失败 %s", e)

	def write_report_result(self):
		"""
		这个方法用于书写测试报告结果
		:return: None
		"""
		reportName = eval(conf.get_data(title=cs.REPORT_NAME, key=cs.REPORT))
		_filename = cs.REPORT_PATH + str(reportName) + cs.NOW
		fb = open(_filename,"rt+")
		time.sleep(2)
		try:
			f = open(_filename)
			content = f.readline()
			if content != None:
				_count = content.count("Number")
				_fail = content.count("Case Fail")
				_pass = content.count("Case Pass")
				space = content.split('\n')
				space.insert(0, cs.RESULT_CONTENT % (_count, _pass, _fail))
				_content_ = '\n'.join(space)
				# fp = open(_filename, 'r')
				# fb.write(bytes(_content_))
				# fb.close()

		except Exception as e:
			logging.error("1文件路径不存在 %s", e)
