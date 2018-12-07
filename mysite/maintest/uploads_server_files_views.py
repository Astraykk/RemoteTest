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

# patternGen.prepare()

# define
DONE = 2
LOADING = 1
UNDONE = 0
# end define

# Create your views here.

DIRECTORY = os.path.join(site.storage.location, "uploads")  # /path/to/mysite/uploads/
SELFDIRECTORY = DIRECTORY


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


def treeview_parser(root='', abspath='', flag='C'):
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
		if fileobject.is_folder:  # and not fileobject.is_empty:
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
				"href": reverse('maintest:test') + "?file=" + newabspath
			})
	return dataList


def treeview_ajax(request):
	"""
	Receive the request, return treeview format of the target.
	:param request:
	:return:
	"""
	query = request.GET
	query_dir = query.get('dir', '')
	query_flag = query.get('flag', '')
	path = os.path.join(DIRECTORY, query_dir)
	global SELFDIRECTORY  # replaced by self.directory
	SELFDIRECTORY = query_dir
	result = treeview_parser(path, query_flag)
	return HttpResponse(json.dumps(result), content_type='application/json')


def test(request):
	query = request.GET
	query_file = query.get('file', '')
	file_path = os.path.join(DIRECTORY, query_file)
	query_path = query.get('path', '')
	# print(SELFDIRECTORY)
	obj = treeview_parser(SELFDIRECTORY)
	tv_dir = treeview_parser(DIRECTORY, flag='O')
	stream_status = [["Check", DONE], ["Build", LOADING], ["Test", UNDONE]]

	return render(request, 'maintest/test.html', {
		'file_path': file_path,
		'file_content': edit_file(file_path),
		'obj': json.dumps(obj),
		'tv_dir': json.dumps(tv_dir),
		'stream_status': stream_status
	})


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


def edit_file(file_path):
	import binascii
	if os.path.isfile(file_path):
		# if os.path.splitext(file_path)[1] == '.bin':  # handle binary file
		# 	file_format = 'rb+'
		# else:
		# 	file_format = 'r+'
		# with open(file_path, file_format) as f:
		with open(file_path, 'rb+') as f:
			content = f.read()
			if os.path.splitext(file_path)[1] == '.bin':
				# print('ok')
				content = binascii.hexlify(content)
				# print(type(content))
		return content
	else:
		return "edit your file here."


class MainTest(object):
	pattern = 0
	wave_path = ''
	project_name = ''

	def __init__(self, storage=default_storage):
		self.storage = storage
		self.directory = DIRECTORY
		self.stream_status = [["Check", UNDONE], ["Build", UNDONE], ["Test", UNDONE]]  # TODO: extend the item.

	def file_check(self, request):
		pass

	def syntax_check(self, request):
		pass

	def check(self, request):
		self.stream_status[0][1] = DONE  # Check status
		return HttpResponse('check success')

	def build(self, request):
		query = request.GET
		path = query.get('path', '')
		# tfo_file = query.get('tfo', '')
		print('path= ', path)
		tfo_file = 'tfo_demo.tfo'
		self.pattern = PatternGen(path, tfo_file)
		print('initialization success!')
		try:
			self.pattern.write()
			self.pattern.save_temp()
			print('write success!')
			self.stream_status[1][1] = DONE  # Build status
			return HttpResponse("Build Success!")
		except Exception as err:
			return err

	def test(self, request):
		query = request.GET
		print(self.directory)
		path = os.path.join(self.directory)  # query.get('path', ''))
		# path = query.get('path', '')
		rpt_name = query.get('rpt_name', 'test_result')
		i_file = os.path.join(DIRECTORY, path, self.project_name+'.ptn')
		o_file = os.path.join(DIRECTORY, path, rpt_name + '.trf')
		vcd_file = os.path.join(DIRECTORY, path, rpt_name + '.vcd')
		print('i_file = {}\no_file = {}\nvcd_file = {}\n'.format(i_file, o_file, vcd_file))
		print('wave_path = ' + self.wave_path)
		try:
			msg = os.popen('sudo ~/BR0101/z7_v4_com/z7_v4_ip_app {} {} 1 1 1'.format(i_file, o_file)).read()
			print('msg = ', msg)
			self.stream_status[2][1] = DONE  # Build status
			# TODO: self.pattern.trf2vcd(o_file, vcd_file)
			self.pattern.trf2vcd(o_file, vcd_file)
			from .mytools.vcd2pic.vcd2pic import vcd2pic
			pic_path = os.path.join(self.wave_path, self.project_name) + '.jpg'
			print(pic_path)
			vcd2pic(vcd_file, pic_path)
			os.popen("sudo echo 3 > /proc/sys/vm/drop_caches")
			return HttpResponse(msg)
		except Exception as err:
			return HttpResponse(err)
			# return HttpResponse('error')

	def treeview_ajax(self, request):
		query = request.GET
		query_dir = query.get('dir', '')
		query_flag = query.get('flag', '')
		path = os.path.join(DIRECTORY, query_dir)
		# if os.path.exists(path):
		# 	return HttpResponse('Project already exits!')
		# self.directory = os.path.join(self.directory, query_dir)  # change root directory of the page
		self.directory = query_dir  # change root directory of the page
		self.project_name = query_dir
		self.wave_path = os.path.join(site.storage.location, "maintest/static/maintest/img", query_dir)
		if not os.path.exists(self.wave_path):
			os.mkdir(self.wave_path)
		result = treeview_parser(path, query_flag)
		return HttpResponse(json.dumps(result), content_type='application/json')

	def edit_file(self, file_path):
		import binascii
		if os.path.isfile(file_path):
			with open(file_path, 'rb+') as f:
				content = f.read()
				if os.path.splitext(file_path)[1] == '.bin':
					# print('ok')
					content = binascii.hexlify(content)
			# print(type(content))
			return content
		else:
			return "edit your file here."

	@csrf_exempt  # WTF
	def save_file(self, request):
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

	def index(self, request):
		"""
		:param request:
		:return: file path,
		"""
		query = request.GET
		query_file = query.get('file', '')
		file_path = os.path.join(self.directory, query_file)
		query_path = query.get('path', '')
		obj = treeview_parser(self.directory)
		tv_dir = treeview_parser(DIRECTORY, flag='O')
		print(self.directory)
		wave_path = os.path.join('maintest/img/', self.directory, '/wave.jpg')
		return render(request, 'maintest/test.html', {
			'DIRECTORY': DIRECTORY,
			'current_path': self.directory,
			'file_content': self.edit_file(file_path),   # file to display in <textarea>
			'file_path': file_path,                 # path of the above
			'wave_path': wave_path,
			'obj': json.dumps(obj),                 # default treeview object
			'tv_dir': json.dumps(tv_dir),
			'stream_status': self.stream_status     # stream status
		})


storage = DefaultStorage()

maintest = MainTest(storage=storage)
