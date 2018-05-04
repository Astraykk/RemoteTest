from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import DefaultStorage, default_storage, FileSystemStorage
from django.core.urlresolvers import reverse
from django.core.files.storage import DefaultStorage, default_storage, FileSystemStorage
from django.http import StreamingHttpResponse

from filebrowser.sites import site
from filebrowser.base import FileListing, FileObject
import os, json, re

# define
DONE = 2
LOADING = 1
UNDONE = 0
# end define

# Create your views here.

DIRECTORY = os.path.join(site.storage.location, "uploads")


def index(request):
	return HttpResponse("This is the file management page.")


def dict2json(List):
	"""
	Change a dict to a json.
	:param dict:
	:return json:
	"""
	return render(request, 'maintest/test.html', {
		'List': json.dumps(List),
	})


"""
arithmetic app functions
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


"""Main test template"""


def treeview_parser(root='', abspath=''):
	"""
	According to the given root, traverse its file tree and return a json object.
	:param root:
	:return dict:
	"""
	dataList = []
	path = os.path.join(DIRECTORY, root)
	filelisting = FileListing(path, sorting_by='date', sorting_order='desc')
	for item in filelisting.listing():
		fileobject = FileObject(os.path.join(path, item))
		newabspath = os.path.join(abspath, item)
		if fileobject.is_folder and not fileobject.is_empty:
			dataList.append({
				"text": item,
				"icon": "glyphicon glyphicon-folder-close",
				"nodes": treeview_parser(fileobject.path_relative_directory, newabspath)
			})
		else:
			dataList.append({
				"icon": "glyphicon glyphicon-file",
				"href": reverse('maintest:test') + "?file=" + newabspath,
				"text": item
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
	path = os.path.join(DIRECTORY, query_dir)
	result = treeview_parser(path)
	return HttpResponse(json.dumps(result), content_type='application/json')


def test(request):
	query = request.GET
	query_file = query.get('file', '')
	file_path = os.path.join(DIRECTORY, query_file)
	obj = treeview_parser()
	stream_status = [["Check", DONE], ["Build", LOADING], ["Test", UNDONE]]

	return render(request, 'maintest/test.html', {
		'file_path': file_path,
		'file_content': edit_file(file_path),
		'obj': json.dumps(obj),
		'stream_status': stream_status
	})


from django.views.decorators.csrf import csrf_exempt


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
	if os.path.isfile(file_path):
		# if os.path.splitext(file_path)[1] == '.bin':  # handle binary file
		# 	file_format = 'rb+'
		# else:
		# 	file_format = 'r+'
		# with open(file_path, file_format) as f:
		with open(file_path, 'r+') as f:
			content = f.read()
		# content.encode('utf-8').strip()
		return content
	else:
		return "edit your file here."


class MainTest(object):
	def __init__(self, storage=default_storage):
		self.storage = storage
		self.directory = DIRECTORY
		self.stream_status = [["Check", UNDONE], ["Build", UNDONE], ["Test", UNDONE]]

	def file_check(self, request):
		pass

	def syntax_check(self, request):
		pass

	def build(self, request):
		query = request.GET
		query_dir = query.get('path', '')
		path = os.path.join(self.directory, query_dir)
		os.popen("/path/to/patternGen.py")

	def test(self, request):
		pass

	def treeview_ajax(self, request):
		query = request.GET
		query_dir = query.get('dir', self.directory)
		path = os.path.join(self.directory, query_dir)
		result = treeview_parser(path)
		return HttpResponse(json.dumps(result), content_type='application/json')

	def edit_file(self, request):
		query = request.GET
		query_file = query.get('file', '')
		path = os.path.join(self.directory, query_file)
		with open(path, 'r+') as f:
			content = f.read()
		return HttpResponse(content)

	def index(self, request):
		obj = treeview_parser("myTest")

		return render(request, 'maintest/index.html', {
			'obj': json.dumps(obj),
			'stream_status': self.stream_status
		})


storage = DefaultStorage()

maintest = MainTest(storage=storage)
