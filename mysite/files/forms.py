import os
import re

from django import forms
from django.utils.translation import ugettext_lazy as _

'''
from filebrowser.settings import FOLDER_REGEX
from filebrowser.utils import convert_filename
'''


class UploadFileForm(forms.Form):

	# title = forms.CharField(max_length=50)
	
	file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	

class CreateDirForm(forms.Form):
	"""
	Form for creating a folder.
	"""

	name = forms.CharField(
		widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, 
		max_length=50, min_length=3)), 
		label=_(u'Name'), 
		help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'), 
		required=True
		)


class ChangeForm(forms.Form):
	"""
	Form for creating a folder.
	"""

	name = forms.CharField(
		widget=forms.TextInput(attrs=dict({'class': 'vTextField'},
		max_length=50, min_length=3)),
		label=_(u'Name'),
		help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'),
		required=True
		)