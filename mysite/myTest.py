import os


os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from filebrowser.sites import site
from filebrowser.base import FileListing
from filebrowser.base import FileObject

'''
print(site.storage.location)
filelisting = FileListing(site.storage.location + "/uploads/", sorting_by='date', sorting_order='desc')
for item in filelisting.listing():
	print(item)
'''
print(site.directory)
file = FileObject(os.path.join(site.directory,"test"))
print(file.path_relative_directory)

'''
pring(os.path)
'''