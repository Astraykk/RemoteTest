from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import DefaultStorage, default_storage, FileSystemStorage
from django.core.urlresolvers import reverse
from django.core.files.storage import DefaultStorage, default_storage, FileSystemStorage
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from filebrowser.sites import site
from filebrowser.base import FileListing, FileObject
import os, json, re
from .mytools.patternGen import PatternGen
from .mytools.mytools import VcdFile, vcd_merge

import time

# patternGen.prepare()

# define
DONE = 2
LOADING = 1
UNDONE = 0
# end define

# Create your views here.

DIRECTORY = os.path.join(site.storage.location, "Users","all_users")  # /path/to/mysite/uploads/
#DIRECTORY = os.path.join("Users","all_users")
"""
Arithmetic app functions
"""


def _file_process(file, regex):
	dict = {}
	with open(file, "r") as fp:
		for line in fp.readlines():
			# print(line)
			m = regex.match(line)
			if m:
				dict[m.group(1)] = m.group(2)
	return dict


def data_parser(file):
	regex = re.compile(r'(data\d): (\d+)')
	return _file_process(file, regex)


def operator_parser(file):
	regex = re.compile(r'(operator): (0x80{6}\d)')
	return _file_process(file, regex)


def app_execution(data1, data2, operator):
	return_value = os.popen('sudo /BR0101/arith_math/arithmetic_intr_mmap_test_app' + data1 + data2 + operator).read()
	return return_value


def arithmetic_app(request):
	# TODO: ugly code.
	dataFile = os.path.join(DIRECTORY, "myTest/data")
	operatorFile = os.path.join(DIRECTORY, "myTest/operator")
	dataDict = data_parser(dataFile)
	operator = operator_parser(operatorFile)['operator']
	result = app_execution(dataDict['data1'], dataDict['data2'], operator)
	# result = app_execution(dataDict["data1"], dataDict["data2"], operator)
	return HttpResponse(result)


"""
Main test template
"""


def treeview_parser(root='', abspath='', relpath='', flag='C'):
	"""
	According to the given root, traverse its file tree and return a json object.
	:param root:
	:param abspath:
	:param flag: 'C'-> Complete file tree, 'O'-> file tree used in open project
	:return:
	"""
	dataList = []
	path = os.path.join(DIRECTORY, root)
	filelisting = FileListing(path, sorting_by='date', sorting_order='desc')
	for item in filelisting.listing():
		fileobject = FileObject(os.path.join(path, item))
		newabspath = os.path.join(abspath, item)
		# print(newabspath)
		if flag == 'O':
			dataList.append({
				"text": item,
				"icon": "glyphicon glyphicon-folder-close",
				# "selectedIcon": "glyphicon glyphicon-folder-open",
				"nodes": treeview_parser(fileobject.path_relative_directory, newabspath, flag=flag),
				"href": reverse('maintest:index') + "?path=" + newabspath
			})
		elif fileobject.is_folder:  # and not fileobject.is_empty:
			dataList.append({
				"text": item,
				"icon": "glyphicon glyphicon-folder-close",
				# "selectedIcon": "glyphicon glyphicon-folder-open",
				"nodes": treeview_parser(fileobject.path_relative_directory, newabspath, flag=flag)
			})
		elif flag == 'C':
			dataList.append({
				"text": item,
				"icon": "glyphicon glyphicon-file",
				"href": reverse('maintest:index') + "?file=" + newabspath + "&path=" + relpath
				# "href": "#edit-text"
			})
	return dataList


def clr_status(request):
	for item in request.session['stream_status']:
		item[1] = UNDONE


def file_check(request):
	pass


def syntax_check(request):
	pass


def check(request):
	query = request.GET
	# self.tfo_path = os.path.join(DIRECTORY, query.get('path', ''))
	request.session['tfo_path'] = request.session['directory']
	request.session['tfo_name'] = query.get('tfo', '')
	print('tfo_path =', request.session['tfo_path'])
	print('tfo_name =', request.session['tfo_name'])
	# tfo_file = 'tfo_demo.tfo'
	# TODO: Check file integrity and syntax.
	request.session['stream_status'][0][1] = DONE  # Check status
	return HttpResponse('check success')


def build(request):
	from maintest.mytools.batch import batch_build
	query = request.GET
	path = query.get('path', '')
	print('initialization success!')
	tfo_path = request.session['tfo_path']
	tfo_name = request.session['tfo_name']
	print('path = {}\ntfo = {}'.format(tfo_path, tfo_name))
	batch_build(tfo_path, tfo_name)
	print('write success!')
	request.session['stream_status'][1][1] = DONE  # Build status
	return HttpResponse("Build Success!")


def test(request):
	from maintest.mytools.batch import batch_test
	try:
		tfo_path = request.session['tfo_path']
		tfo_name = request.session['tfo_name']
		print('path = {}\ntfo = {}'.format(tfo_path, tfo_name))
		batch_test(tfo_path, tfo_name)
		request.session['stream_status'][2][1] = DONE
		return HttpResponse('Test Success!')
	except Exception as err:
		return HttpResponse(err)


def report(request):
	from maintest.mytools.batch import batch_trf2vcd, batch_merge
	try:
		tfo_path = request.session['tfo_path']
		tfo_name = request.session['tfo_name']
		print(tfo_path, tfo_name)
		batch_trf2vcd(tfo_path, tfo_name)
		batch_merge(tfo_path, tfo_name)
		request.session['stream_status'][3][1] = DONE
		return HttpResponse('Report ready!')
	except Exception as err:
		return HttpResponse(err)


def treeview_ajax(request):
	username = request.session.get("username",None)
	if username:
		query = request.GET
		query_dir = query.get('dir', '')
		query_flag = query.get('flag', '')
		path = os.path.join(DIRECTORY, username ,query_dir)
		request.session['directory'] = path  # change root directory of the page
		# print('ajax_path', request.session['directory'])
		request.session['project_name'] = query_dir
		#request.session['wave_path'] = os.path.join(site.storage.location, "maintest/static/maintest/img", username ,query_dir)
		#request.session['wave_path'] = os.path.join("maintest/static/maintest/img", username ,query_dir)
		clr_status(request)
		# if not os.path.exists(request.session['wave_path']):
			# os.mkdir(request.session['wave_path'])
		result = treeview_parser(path, flag=query_flag)
	else:
		result = [{"text":"login first!"}]
	return HttpResponse(json.dumps(result), content_type='application/json')
	


def edit_file(file_path):
	import binascii
	if os.path.isfile(file_path):
		with open(file_path, 'rb+') as f:
			content = f.read()
			if os.path.splitext(file_path)[1] == '.ptn':
				pattern = re.compile('.{32}')
				content = str(binascii.hexlify(content)).lstrip("b'").upper()
				content = '\t'.join(re.findall(r'.{4}', content))
				content = '\n'.join(re.findall(r'.{40}', content))
		# print(type(content))
		return content
	else:
		return "edit your file here."


@csrf_exempt  # WTF
def save_file(request):
	if request.method == 'POST':
		try:
			# print(request.POST)
			content = request.POST['text']
			path = request.POST['path']
			with open(path, 'w') as f:
				f.write(content)
			return HttpResponse("Success!")
		except Exception as exc:
			return HttpResponse(exc)


def index(request):
	"""
	:param request:
	:return: file path,
	"""
	# initialize session
	status = [
		["Check", UNDONE],
		["Build", UNDONE],
		["Test", UNDONE],
		["Report", UNDONE]
	]
	request.session.setdefault('stream_status', status)
	username = request.session.get("username",None)
	if username:
		
		#request.session.setdefault('directory', DIRECTORY)
		
		query = request.GET
		query_file = query.get('file', 'open file')
		# print('query_file(in index)=', query_file)
		directory = request.session.get('directory', username)
		file_path = os.path.join(directory, query_file)
		# print('file_path(in index)=', file_path)
		# print(query_file, file_path)
		query_path = query.get('path', '')
		obj = treeview_parser(directory, relpath=query_path)
		# print(obj)
		tv_dir = treeview_parser(os.path.join(DIRECTORY, username), flag='O')
		# print(self.directory)
		#wave_path = os.path.join('maintest/static/maintest/img', username, '/wave.jpg')
		return render(request, 'maintest/test.html', {
			'DIRECTORY': DIRECTORY,
			'current_path': username,   # directory is Bad URL
			'file_content': edit_file(file_path),  # file to display in <textarea>
			'file_path': file_path,  # path of the above
			'file_name': query_file,
			# 'wave_path': request.session.get("wave_path",wave_path),  # can't deal with it
			'obj': json.dumps(obj),  # default treeview object
			'tv_dir': json.dumps(tv_dir),
			'stream_status': request.session.get('stream_status', []),  # stream status
			'username':username,
		})
	else:
		return render(request, 'maintest/test.html', {
			'stream_status': request.session.get('stream_status', [])  # stream status
		})


# class MainTest(object):
# 	wave_path = ''
# 	project_name = ''
#
# 	def __init__(self, storage=default_storage):
# 		self.directory = DIRECTORY
# 		self.stream_status = [
# 			["Check", UNDONE],
# 			["Build", UNDONE],
# 			["Test", UNDONE],
# 			["Report", UNDONE]
# 		]  # TODO: extend the item.
#
# 	def clr_status(self):
# 		for item in self.stream_status:
# 			item[1] = UNDONE
#
# 	def file_check(self, request):
# 		pass
#
# 	def syntax_check(self, request):
# 		pass
#
# 	# def check(self, request):
# 	# 	query = request.GET
# 	# 	# self.tfo_path = os.path.join(DIRECTORY, query.get('path', ''))
# 	# 	self.tfo_path = self.directory
# 	# 	self.tfo_name = query.get('tfo', '')
# 	# 	print('path = {}\ntfo = {}'.format(self.tfo_path, self.tfo_name))
# 	# 	print('directory =', self.directory)
# 	# 	# tfo_file = 'tfo_demo.tfo'
# 	# 	# self.pattern = PatternGen(self.tfo_path, self.tfo_name)
# 	# 	# TODO: Check file integrity and syntax.
# 	# 	self.stream_status[0][1] = DONE  # Check status
# 	# 	return HttpResponse('check success')
#
# 	def check(self, request):
# 		query = request.GET
# 		# self.tfo_path = os.path.join(DIRECTORY, query.get('path', ''))
# 		request.session['tfo_path'] = self.directory
# 		request.session['tfo_name'] = query.get('tfo', '')
# 		print('directory =', self.directory)
# 		# tfo_file = 'tfo_demo.tfo'
# 		# self.pattern = PatternGen(self.tfo_path, self.tfo_name)
# 		# TODO: Check file integrity and syntax.
# 		self.stream_status[0][1] = DONE  # Check status
# 		return HttpResponse('check success')
#
# 	def build(self, request):
# 		from maintest.mytools.batch import batch_build
# 		query = request.GET
# 		path = query.get('path', '')
# 		# print(path)
# 		# tfo_file = query.get('tfo', '')
# 		# print('path= ', path)
# 		# tfo_file = 'tfo_demo.tfo'
# 		# self.pattern = PatternGen(path, tfo_file)
# 		print('initialization success!')
# 		# try:
# 		# 	# self.pattern.write()
# 		# 	batch_build(self.tfo_path, self.tfo_name)
# 		# 	print('write success!')
# 		# 	self.stream_status[1][1] = DONE  # Build status
# 		# 	return HttpResponse("Build Success!")
# 		# except Exception as err:
# 		# 	return err
# 		# self.pattern.write()
# 		print('path = {}\ntfo = {}'.format(self.tfo_path, self.tfo_name))
# 		batch_build(self.tfo_path, self.tfo_name)
# 		print('write success!')
# 		self.stream_status[1][1] = DONE  # Build status
# 		return HttpResponse("Build Success!")
#
# 	# def test(self, request):
# 	# 	query = request.GET
# 	# 	print(self.directory)
# 	# 	path = os.path.join(self.directory)  # query.get('path', ''))
# 	# 	# path = query.get('path', '')
# 	# 	rpt_name = query.get('rpt_name', 'test_result')
# 	# 	i_file = os.path.join(DIRECTORY, path, self.pattern.file_list['BIT']+'.ptn')
# 	# 	o_file = os.path.join(DIRECTORY, path, rpt_name + '.trf')
# 	# 	vcd_file = os.path.join(DIRECTORY, path, rpt_name + '.vcd')
# 	# 	ref_vcd_path = os.path.join(DIRECTORY, path, self.pattern.file_list['VCD'])
# 	# 	timescale = self.pattern.digital_param['period']
# 	# 	print('i_file = {}\no_file = {}\nvcd_file = {}\n'.format(i_file, o_file, vcd_file))
# 	# 	print('wave_path = ' + self.wave_path)
# 	# 	try:
# 	# 		start_time = time.time()
# 	# 		print('Start batch build')
# 	# 		msg = os.popen('sudo /home/linaro/BR0101/z7_v4_com/z7_v4_ip_app {} {} 1 1 1'.format(i_file, o_file)).read()
# 	# 		# msg = 'test success'
# 	# 		print('msg = ', msg)
# 	# 		end_time = time.time()
# 	# 		print("\nTest time: " + str(end_time - start_time))
# 	# 		self.stream_status[2][1] = DONE  # Build status
# 	# 		self.pattern.trf2vcd(rpt_name + '.trf', rpt_name + '.vcd', flag='bypass')
# 	# 		# from .mytools.vcd2pic.vcd2pic import vcd2pic
# 	# 		# pic_path = os.path.join(self.wave_path, self.project_name) + '.jpg'
# 	# 		# print(pic_path)
# 	# 		# vcd2pic(vcd_file, pic_path)
# 	#
# 	# 		# vcd merge
# 	# 		vcd1 = VcdFile(ref_vcd_path, period=timescale)  # reference vcd
# 	# 		# print('vcd1 = ', vcd1.vcd_info)
# 	# 		vcd1.get_vcd_info()
# 	# 		vcd2 = VcdFile(vcd_file, period='1ps')
# 	# 		# print('vcd2 = ', vcd2.vcd_info)
# 	# 		vcd2.get_vcd_info()
# 	# 		vcdm = vcd_merge(vcd1, vcd2, os.path.join(DIRECTORY, path, rpt_name + '_merge.vcd'))
# 	# 		print(vcdm.sym2sig)
# 	# 		# vcd2.gen_vcd('pin_test/p1_merge.vcd')
# 	# 		vcdm.gen_vcd(vcdm.path)
# 	#
# 	# 		return HttpResponse(msg)
# 	# 	except Exception as err:
# 	# 		return HttpResponse(err)
# 	# 		# return HttpResponse('error')
#
# 	def test(self, request):
# 		from maintest.mytools.batch import batch_test
# 		query = request.GET
# 		# print(self.directory)
# 		path = os.path.join(self.directory)  # query.get('path', ''))
# 		try:
# 			batch_test(self.tfo_path, self.tfo_name)
# 			self.stream_status[2][1] = DONE
# 			return HttpResponse('Test Success!')
# 		except Exception as err:
# 			return HttpResponse(err)
# 			# return HttpResponse('error')
#
# 	def report(self, request):
# 		from maintest.mytools.batch import batch_trf2vcd, batch_merge
# 		try:
# 			tfo_path = request.session['tfo_path']
# 			tfo_name = request.session['tfo_name']
# 			print(tfo_path, tfo_name)
# 			batch_trf2vcd(tfo_path, tfo_name)
# 			batch_merge(tfo_path, tfo_name)
# 			self.stream_status[3][1] = DONE
# 			return HttpResponse('Report ready!')
# 		except Exception as err:
# 			return HttpResponse(err)
#
# 	# def report(self, request):
# 	# 	from maintest.mytools.batch import batch_trf2vcd, batch_merge
# 	# 	try:
# 	# 		# print(self.tfo_path, self.tfo_name)
# 	# 		batch_trf2vcd(self.tfo_path, self.tfo_name)
# 	# 		batch_merge(self.tfo_path, self.tfo_name)
# 	# 		self.stream_status[3][1] = DONE
# 	# 		return HttpResponse('Report ready!')
# 	# 	except Exception as err:
# 	# 		return HttpResponse(err)
#
# 	def treeview_ajax(self, request):
# 		query = request.GET
# 		query_dir = query.get('dir', '')
# 		query_flag = query.get('flag', '')
# 		path = os.path.join(DIRECTORY, query_dir)
# 		# if os.path.exists(path):
# 		# 	return HttpResponse('Project already exits!')
# 		# self.directory = os.path.join(self.directory, query_dir)  # change root directory of the page
# 		# self.directory = query_dir  # change root directory of the page
# 		self.directory = path  # change root directory of the page
# 		# print('ajax_path', self.directory)
# 		self.project_name = query_dir
# 		self.wave_path = os.path.join(site.storage.location, "maintest/static/maintest/img", query_dir)
# 		self.clr_status()
# 		if not os.path.exists(self.wave_path):
# 			os.mkdir(self.wave_path)
# 		result = treeview_parser(path, flag=query_flag)
# 		return HttpResponse(json.dumps(result), content_type='application/json')
#
# 	def edit_file(self, file_path):
# 		import binascii
# 		# print('directory=', self.directory)
# 		# print('file_path=', file_path)
# 		if os.path.isfile(file_path):
# 			with open(file_path, 'rb+') as f:
# 				content = f.read()
# 				if os.path.splitext(file_path)[1] == '.ptn':
# 					pattern = re.compile('.{32}')
# 					content = str(binascii.hexlify(content)).lstrip("b'").upper()
# 					content = '\t'.join(re.findall(r'.{4}', content))
# 					content = '\n'.join(re.findall(r'.{40}', content))
# 			# print(type(content))
# 			return content
# 		else:
# 			return "edit your file here."
#
# 	@csrf_exempt  # WTF
# 	def save_file(self, request):
# 		if request.method == 'POST':
# 			try:
# 				# print(request.POST)
# 				content = request.POST['text']
# 				path = request.POST['path']
# 				with open(path, 'w') as f:
# 					f.write(content)
# 				return HttpResponse("Success!")
# 			except Exception as exc:
# 				return HttpResponse(exc)
#
# 	def index(self, request):
# 		"""
# 		:param request:
# 		:return: file path,
# 		"""
# 		query = request.GET
# 		query_file = query.get('file', 'open file')
# 		# print('query_file(in index)=', query_file)
# 		file_path = os.path.join(self.directory, query_file)
# 		# print('file_path(in index)=', file_path)
# 		# print(query_file, file_path)
# 		query_path = query.get('path', '')
# 		# self.directory = os.path.join(DIRECTORY, query_path)
# 		# print('index_path', self.directory)
# 		obj = treeview_parser(self.directory, relpath=query_path)
# 		# print(obj)
# 		tv_dir = treeview_parser(DIRECTORY, flag='O')
# 		# print(self.directory)
# 		wave_path = os.path.join('maintest/img/', self.directory, '/wave.jpg')
# 		return render(request, 'maintest/test.html', {
# 			'DIRECTORY': DIRECTORY,
# 			'current_path': self.directory,
# 			'file_content': self.edit_file(file_path),   # file to display in <textarea>
# 			'file_path': file_path,                 # path of the above
# 			'file_name': query_file,
# 			'wave_path': wave_path,
# 			'obj': json.dumps(obj),                 # default treeview object
# 			'tv_dir': json.dumps(tv_dir),
# 			'stream_status': self.stream_status     # stream status
# 		})
#
#
# storage = DefaultStorage()
#
# maintest = MainTest(storage=storage)