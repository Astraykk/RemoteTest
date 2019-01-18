from django.db import models


class Users(models.Model):
	username = models.CharField('username',max_length=20,primary_key=True, unique=True)
	password = models.CharField('password',max_length=20)
	authority = models.CharField('authority',max_length=20,default='common_user')
	email = models.CharField('email',max_length=50,null=True)

	def __str__(self):
		return '%s' % self.username

# Create your models here.


class Task(models.Model):
	username = models.CharField('username',max_length=20)
	project_name = models.CharField('project_name',max_length=100)
	authority = models.CharField('authority',max_length=20)
	request_serial_num = models.IntegerField('request_serial_num',primary_key=True, unique=True)
	task_priority = models.IntegerField('task_priority')
	
	def __str__(self):
		return '%s'%(self.request_serial_num)
	# class Meta:
        # ordering = ['task_priority','request_serial_num']
		
#class History(models.Model):
	