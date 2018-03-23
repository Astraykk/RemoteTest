from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.storage import DefaultStorage, default_storage, FileSystemStorage
from django.http import StreamingHttpResponse


from filebrowser.sites import site
from filebrowser.base import FileListing, FileObject
import os, json

# Create your views here.


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


def treeview_parser(root):
	"""
	According to the given root, traverse its file tree and return a json object.
	:param root:
	:return dict:
	"""


def test(request):
	List = ['key', 'value']
	Dict = {'site': 'aaa', 'author': 'bbb'}
	obj = [
		{
			"text": "Parent 1",
			"nodes": [
				{
					"text": "Child 1",
					"nodes": [
						{
							"text": "Grandchild 1"
						},
						{
							"text": "Grandchild 2"
						}
					]
				},
				{
					"text": "Child 2"
				}
			]
		},
		{
			"text": "Parent 2"
		},
		{
			"text": "Parent 3"
		},
		{
			"text": "Parent 4"
		},
		{
			"text": "Parent 5"
		}
	]
	return render(request, 'maintest/test.html', {
		'List': json.dumps(List),
		'obj': json.dumps(obj),
		'Dict': json.dumps(Dict)
	})


def treeview_parser():
	pass

