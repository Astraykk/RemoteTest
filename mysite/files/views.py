from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.storage import DefaultStorage, default_storage, FileSystemStorage
from django.http import StreamingHttpResponse

from .forms import UploadFileForm

from filebrowser.sites import site
from filebrowser.base import FileListing, FileObject
import os

# print(site.storage.location)

# Create your views here.


from django.views.generic.edit import FormView
from .forms import UploadFileForm


class FileFieldView(FormView):
	form_class = UploadFileForm
	template_name = 'files/upload.html'  # Replace with your template.
	success_url = '...'  # Replace with your URL or reverse().

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')
		if form.is_valid():
			for f in files:
				...  # Do something with each file.
			return self.form_valid(form)
		else:
			return self.form_invalid(form)


def index(request):
	return HttpResponse("This is the file management page.")


def handle_uploaded_file(dir, f):
	with open(os.path.join('./uploads/', dir, f.name), 'wb+') as destination:
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
			'form': form,
			'query': query,
			'breadcrumbs': get_Breadcrumbs(query.get('dir', ''))
		})


def get_Breadcrumbs(query):
	# Return a breadcrumb-style navigation bar
	breadcrumbs = []
	temp_path = ''
	if query:
		for item in os.path.split(query):
			temp_path = os.path.join(temp_path, item)
			breadcrumbs.append([item, temp_path])
	return breadcrumbs


class MyFileBrowser(object):
	# filelisting_class = FileListing

	def __init__(self, storage=default_storage):
		self.directory = os.path.abspath('uploads')
		self.storage = storage

	def file_browse(self, request):
		query = request.GET
		query_dir = query.get('dir', '')
		path = u'%s' % os.path.join(site.directory, query_dir)
		# print(site.directory)

		# Return a file list:hehe
		filelisting = FileListing(path, sorting_by='date', sorting_order='desc')
		fileobjects = []
		for filepath in filelisting.listing():
			fileobject = FileObject(os.path.join(site.directory, query_dir, filepath))
			# print(fileobject.path_relative_directory)
			fileobjects.append(fileobject)
		return render(request, 'files/index.html', {
			'query': query,
			'query_dir': query_dir,
			'filelisting': filelisting,
			'breadcrumbs': get_Breadcrumbs(query_dir),
			'fileobjects': fileobjects
			})

	def upload_file(self, request):
		query = request.GET
		query_dir = query.get('dir', '')
		if request.method == 'POST':
			form = UploadFileForm(request.POST, request.FILES)
			print(request.FILES.getlist('file'))
			if form.is_valid():
				handle_uploaded_file(query_dir, request.FILES['file'])
				redirect_url = reverse("files:browse") + '?dir=' + query.get('dir', '')
				return HttpResponseRedirect(redirect_url)
		else:
			form = UploadFileForm()
		return render(request, 'files/upload.html', {
			'form': form,
			'query': query,
			'breadcrumbs': get_Breadcrumbs(query.get('dir', ''))
		})

	def create_dir(self, request):
		
		from .forms import CreateDirForm

		query = request.GET
		query_dir = query.get('dir', '')
		# print(query_dir)
		path = u'%s' % os.path.join(self.directory, query_dir)

		if request.method == 'POST':
			form = CreateDirForm(request.POST)
			if form.is_valid():
				mkdir_path = os.path.join(path, form.cleaned_data['name'])
				os.mkdir(mkdir_path)
				# return HttpResponse('upload succed!')
			redirect_url = reverse("files:browse")
			return HttpResponseRedirect(redirect_url)
		else:
			form = CreateDirForm()

		# return HttpResponse("You can create new directory here.")
		return render(request, 'files/createdir.html', {
			'form': form,
			'query': query,
			'breadcrumbs': get_Breadcrumbs(query.get('dir', ''))
		})

	def delete(self, request):
		"""Delete existing File/Directory."""
		query = request.GET
		path = u'%s' % os.path.join(self.directory, query.get('dir', ''))
		fileobject = FileObject(os.path.join(path, query.get('filename', '')))
		if request.GET:
			try:
				fileobject.delete()
			except OSError:
				# TODO: define error-message
				pass
		redirect_url = reverse("files:browse") + '?dir=' + query.get('dir', '')
		return HttpResponseRedirect(redirect_url)

	def download(self, request):
		query = request.GET
		file_path = u'%s' % os.path.join(site.directory, query.get('dir', ''), query.get('filename', ''))

		def file_iterator(file_name, chunk_size=512):
			with open(file_name, 'rb') as f:
				while True:
					c = f.read(chunk_size)
					if c:
						yield c
					else:
						break

		response = StreamingHttpResponse(file_iterator(file_path))
		response['Content-Type'] = 'application/octet-stream'
		response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path)

		return response

	def upload(self, request):
		pass

	def detail(self, request):
		query = request.GET
		path = u'%s' % os.path.join(site.directory, query.get('dir', ''))
		fileobject = FileObject(os.path.join(path, query.get('filename', '')))

		from .forms import ChangeForm

		if request.method == 'POST':
			form = ChangeForm(request.POST)
			# print(form.cleaned_data['name'])
			if form.is_valid():
				new_name = form.cleaned_data['name']
				self.storage.move(fileobject.path, os.path.join(fileobject.head, new_name))
				# return HttpResponse('upload succed!')
			redirect_url = reverse("files:browse")+'?dir='+query.get('dir', '')
			return HttpResponseRedirect(redirect_url)
		else:
			form = ChangeForm()

		return render(request, 'files/detail.html', {
			'form': form,
			'query': query,
			'fileobject': fileobject,
			'breadcrumbs': get_Breadcrumbs(query.get('dir', ''))
		})


myFBsite = MyFileBrowser()
