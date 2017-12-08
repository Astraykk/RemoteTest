from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import UploadFileForm

from filebrowser.sites import site
from filebrowser.base import FileListing, FileObject
import os

print(site.storage.location)

# Create your views here.

def index(request):
	return HttpResponse("This is the file management page.")

def handle_uploaded_file(f):
	with open('./uploads/'+f.name, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponse('upload succed!')
	else:
		form = UploadFileForm()
	return render(request, 'files/upload.html', {
			'form': form
		})

class MyFileBrowser(object):
	#filelisting_class = FileListing

	def __init__(self):
		self.directory = os.path.abspath('uploads')
		

	def file_browse(self, request):
		#filelisting = FileListing(site.storage.location + "/uploads/", sorting_by='date', sorting_order='desc')
		query = request.GET.copy()
		path = u'%s' % os.path.join(self.directory, query.get('dir', ''))
		filelisting = FileListing(path, sorting_by='date', sorting_order='desc')
		fileobjects = []
		for path in filelisting.listing():
			fileobject = FileObject(os.path.join(self.directory, path))
			fileobjects.append(fileobject)
		return render(request, 'files/index.html', {
			'filelisting': filelisting,
			'fileobjects': fileobjects
			})

	def create_dir(self, request):
		
		from .forms import CreateDirForm

		if request.method == 'POST':
			form = CreateDirForm(request.POST)
			if form.is_valid():
				path = os.path.join(self.directory, form.cleaned_data['name'])
				os.mkdir(path)
				#return HttpResponse('upload succed!')
			redirect_url = reverse("files:browse")
			return HttpResponseRedirect(redirect_url)
		else:
			form = CreateDirForm()

		return render(request, 'files/createdir.html', {
            'form': form,
        })

		#return HttpResponse("You can create new directory here.")

	def upload(self, request):
		pass

site = MyFileBrowser()