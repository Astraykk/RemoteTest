# -*- coding:utf-8 -*-
"""
batch.py ver_1.0.1
For batch operation: build, test, trf2vcd

Dependencies:
beautiful soup

Path:

Usage:
$ python batch_operation.py
Choose operation: build(0), test(1), trf2vcd(2), merge(3)
(If you want execute multiple operations in a row, input the corresponding digits
like 01, 12, or 012)
(Enter to quit)
build
Input tfo file path:
tfo_demo.tfo
"""
import os
import sys
import bs4
import time
import _thread
if __name__ == '__main__':
	from patternGen import PatternGen
	from mytools import vcd_merge
else:
	from maintest.mytools.patternGen import PatternGen
	from maintest.mytools.mytools import vcd_merge
	from filebrowser.sites import site

if __name__ == '__main__':
	FILE_ROOT_PATH = sys.path[0]
else:
	# FILE_ROOT_PATH = '/home/linaro/mysite/uploads'
	FILE_ROOT_PATH = os.path.join(site.storage.location, "uploads")
app_path = '/home/linaro/BR0101/z7_v4_com/z7_v4_ip_app'
base_command = 'sudo {} {} {} 1 1 1'
if not os.path.exists(app_path):
	app_path = '/home/keylab/BR0101/z7_v4_com/z7_v4_ip_app.py'
	base_command = 'python3 {} {} {}'


def name_check(file, name):
	filename = os.path.splitext(file)[0]
	if filename == name:
		print(file + " name check pass!")
	else:
		print(file + " name mismatch!")


def get_soup(path, file):
	path = os.path.join(path, file)
	# print(path)
	with open(path, "r") as f:
		soup = bs4.BeautifulSoup(f.read(), "xml")
	return soup


def report(file, key='', value=''):
	# if not os.path.isfile(file):
	# 	os.mknod(file)
	with open(file, 'a') as f:
		localtime = time.asctime(time.localtime(time.time()))
		f.write(str(localtime) + '\t')
		f.write(key + '\t')
		f.write(str(value) + '\n')


def get_file_list(path, tfo):
	tfo_path = os.path.join(path, tfo)
	i_list = []
	o_list = []
	# print(path)
	with open(tfo_path, "r") as f:
		soup = bs4.BeautifulSoup(f.read(), "xml")
	for test_tag in soup.find_all('TEST'):
		project_path = test_tag['path']
		base_path = os.path.join(path, project_path, test_tag['name'])
		print(base_path)
		i_list.append(base_path + '.ptn')
		o_list.append(base_path + '.trf')
	return i_list, o_list


def tfo_parser(path, file):
	"""
	:param path:
	:param file:
	:return file_list_list:
	"""
	# file_list_list = {}
	# print(path)
	file_list_list = []
	print("-----------"+file+"s----------")
	soup = get_soup(path, file)
	name_check(file, soup.TFO['name'])
	for test_tag in soup.find_all('TEST'):
		file_list = {
			'PTN': test_tag['name'] + '.ptn',
			'LBF': soup.TFO.LBF['type'] + '.lbf',
			'TCF': 'F93K.tcf'
		}
		project_name = test_tag['name']
		for child in test_tag.children:
			if type(child) == bs4.element.Tag:
				if child.name == 'DWM' or child.name == 'BIT':
					file_list[child.name] = child['name']
				else:
					file_list[child.name] = child['name'] + '.' + child.name.lower()
		# file_list_list[test_tag['path']] = (project_name, file_list)
		if test_tag['path'] == ".":
			file_list_list.append([path, (project_name, file_list)])
		else:
			file_list_list.append([os.path.join(path, test_tag['path'][2:]), (project_name, file_list)])
		# file_list_list.append([test_tag['path'], (project_name, file_list)])
	print(file_list_list)
	return file_list_list


def batch_build(path, tfo):
	# from multiprocessing import Process
	start_time = time.time()
	print('Start batch build')
	file_list_list = tfo_parser(path, tfo)
	report_file = os.path.join(path, tfo.rstrip('.tfo') + '_report.log')
	print('path =', path)
	print('report_path =', report_file)
	print('ROOT =', FILE_ROOT_PATH)
	report(report_file, 'Batch build for '+tfo)
	for project_path, file_list in file_list_list:
		#try:
		s_time = time.time()
		pattern = PatternGen(project_path, file_list=file_list)
		pattern.write()
		e_time = time.time()
		key = 'Build time for {:<30}:'.format(pattern.project_name)
		value = e_time - s_time
		report(report_file, key, value)
		# try:
		# 	_thread.start_new_thread(pattern.write, ())
		# except Exception:
		# 	print("Error: unable to start thread")
		# proc = Process(target=pattern.write, args=())
		# proc.start()
		# proc.join()
		# except Exception as err:
			# key = 'An exception occurs in {}:'.format(project_path)
			# report(report_file, key, err)
	print('Batch build finished')
	end_time = time.time()
	report(report_file, 'Total build time:', end_time - start_time)
	print("\nTotal time: " + str(end_time - start_time))


def batch_test(path, tfo):
	i_file_list, o_file_list = get_file_list(path, tfo)
	print('Start batch test')
	start_time = time.time()
	report_file = os.path.join(FILE_ROOT_PATH, path, tfo.rstrip('.tfo') + '_report.log')
	report(report_file, 'Batch Test for ' + tfo)
	for i in range(len(i_file_list)):
		i_file = i_file_list[i]
		o_file = o_file_list[i]
		file_name = os.path.basename(i_file).rstrip('.ptn')
		try:
			s_time = time.time()
			msg = os.popen(base_command.format(app_path, i_file, o_file)).read()
			print(msg)
			e_time = time.time()
			key = 'Test time for {:<30}:'.format(file_name)
			value = e_time - s_time
			report(report_file, key, value)
		except Exception as err:
			key = 'An exception occurs in {}:'.format(file_name)
			report(report_file, key, err)
	print('Batch test finished')
	end_time = time.time()
	report(report_file, 'Total test time:', end_time - start_time)
	print("\nTotal time: " + str(end_time - start_time))


def batch_trf2vcd(path, tfo):
	print('Start batch trf2vcd')
	file_list_list = tfo_parser(path, tfo)
	print(file_list_list)
	start_time = time.time()
	#report_file = os.path.join(FILE_ROOT_PATH, path, tfo.rstrip('.tfo') + '_report.log')
	report_file = os.path.join(path, tfo.rstrip('.tfo') + '_report.log')
	report(report_file, 'Batch trf2vcd for ' + tfo)
	for project_path, file_list in file_list_list:
		# try:
		temp_path = os.path.join(project_path, 'temp.json')
		if os.path.isfile(temp_path):
			s_time = time.time()
			pattern = PatternGen(project_path, file_list=file_list)
			trf = pattern.project_name + '.trf'
			vcd = pattern.project_name + '_trf.vcd'
			pattern.trf2vcd(trf, vcd, flag='bypass')
			e_time = time.time()
			key = 'Trf2vcd time for {:<30}:'.format(pattern.project_name)
			value = e_time - s_time
			report(report_file, key, value)
		else:
			print('temp.json not found. Please build ptn first.')
		# except Exception as err:
			# key = 'An exception occurs in {}:'.format(project_path)
			# report(report_file, key, err)
	print('Batch trf2vcd finished')
	end_time = time.time()
	report(report_file, 'Total trf2vcd time:', end_time - start_time)
	print("\nTotal time: " + str(end_time - start_time))


def batch_merge(path, tfo):
	print('Start batch merge')
	file_list_list = tfo_parser(path, tfo)
	# print(file_list_list)
	start_time = time.time()
	# report_file = os.path.join(FILE_ROOT_PATH, path, tfo.rstrip('.tfo') + '_report.log')
	report_file = os.path.join(path, tfo.rstrip('.tfo') + '_report.log')
	report(report_file, 'Batch merge for ' + tfo)
	for project_path, file_list in file_list_list:
		# try:
		# pattern = PatternGen(os.path.join(path, project_path), file_list=file_list)
		pattern = PatternGen(project_path, file_list=file_list)
		s_time = time.time()
		period = pattern.digital_param['period']
		# print(type(period))
		vcd1 = os.path.join(project_path, pattern.file_list['VCD'])
		vcd2 = os.path.join(project_path, pattern.project_name + '_trf.vcd')
		vcdm_path = os.path.join(project_path, pattern.project_name + '_merge.vcd')
		vcd_merge(vcd1, vcd2, period, vcdm_path)
		e_time = time.time()
		key = 'Merge time for {:<30}:'.format(pattern.project_name)
		value = e_time - s_time
		report(report_file, key, value)
		# except Exception as err:
			# key = 'An exception occurs in {}:'.format(project_path)
			# report(report_file, key, err)
	print('Batch merge finished')
	end_time = time.time()
	report(report_file, 'Total merge time:', end_time - start_time)
	print("\nTotal time: " + str(end_time - start_time))


string = """
Choose operation: build(0), test(1), trf2vcd(2), merge(3):
(If you want execute multiple operations in a row, input the corresponding digits
like 01, 12, or 012)
(Enter to quit)
"""


def test():
	batch_merge('tfo', 'bugs2.tfo')
	# batch_merge('.', 'bugs2.tfo')
	batch_trf2vcd('tfo', 'chen.tfo')


if __name__ == "__main__":
	while True:
		if len(sys.argv) == 2:
			if sys.argv[1] == 'test':
				test()
				break
		print(string)
		mode = input()
		if mode == '':
			break
		print('Input project path')
		path = input()
		print('Input tfo file name')
		tfo = input()
		for item in list(mode):
			if item == 'build' or item == '0':
				batch_build(path, tfo)
			elif item == 'test' or item == '1':
				# i_list, o_list = get_file_list(path, tfo)
				batch_test(path, tfo)
			elif item == 'trf2vcd' or item == '2':
				batch_trf2vcd(path, tfo)
			elif item == 'merge' or item == '3':
				batch_merge(path, tfo)
