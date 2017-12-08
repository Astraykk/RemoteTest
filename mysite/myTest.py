import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from filebrowser.sites import site
from filebrowser.base import FileListing

print(site.storage.location)
filelisting = FileListing(site.storage.location + "/uploads/", sorting_by='date', sorting_order='desc')
for item in filelisting.listing():
	print(item)