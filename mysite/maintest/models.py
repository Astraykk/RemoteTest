from django.db import models


class Project(models.Model):
	user = models.CharField(max_length=30)  # Use user model
	project_name = models.CharField(max_length=30)
	start_time = models.TimeField()  # DateField, DateTimeField, TimeField
	last_modified_time = models.TimeField()
	status = models.CharField(max_length=4)
	major_files = models.TextField()
	minor_files = models.TextField()
	generated_files = models.TextField()
