from django.db import models

class Users(models.Model):
	username = models.CharField('username',max_length=20,primary_key=True, unique=True)
	password = models.CharField('password',max_length=20)
	authority = models.CharField('authority',max_length=20,default='common_user')
	email = models.CharField('email',max_length=50,null=True)
	subscribe = models.BooleanField(default = False)
	def __str__(self):
		return '%s'%(self.username)

# Create your models here.


class Group(models.Model):
	group_id = models.AutoField('group_id',primary_key=True, unique=True)
	group_name = models.CharField('group_name',max_length=50)
	
	def __str__(self):
		return '%s--%s' % (self.group_id,self.group_name)

class Group_item(models.Model):
	group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
	member = models.ForeignKey(Users, on_delete=models.CASCADE)
	authority = models.CharField('authority',max_length=1) # 1-super admin,2-admin,3-ordinary member,4-pj_admin
	#group_name = models.CharField('group_name',max_length=50,default="")
	
	def __str__(self):
		return '%s--%s' % (self.group_id.group_id,self.member.username)

class Task(models.Model):
	username = models.CharField('username',max_length=20)
	user_or_group = models.CharField('user_or_group',max_length=1) # 0 for user, 1 for group
	project_loc = models.CharField('project_loc',max_length=100)
	# authority = models.CharField('authority',max_length=20)
	request_serial_num = models.IntegerField('request_serial_num',primary_key=True, unique=True)
	# task_priority = models.IntegerField('task_priority')
	ptn_name = models.CharField('ptn_file_name',max_length=30,default="mul5")
	
	def __str__(self):
		return '%s'%(self.request_serial_num)
	# class Meta:
        # ordering = ['task_priority','request_serial_num']
		
class Invitation(models.Model):
	invitee = models.ForeignKey(Users, on_delete=models.CASCADE)
	group_id = models.IntegerField('group_id')
	inviter_name = models.CharField('username',max_length=20)
	invitee_au = models.CharField('authority',max_length=1)
	notes = models.CharField('notes',max_length=100)
	
	def __str__(self):
		return '%s' % (self.group_id)
		
#class History(models.Model):
class au4group(models.Model):
	group_id = models.IntegerField('group_id', primary_key=True, unique=True)
	au4admin = models.CharField('authority_of_admin',max_length=5,default="10110")
	au4pj_admin = models.CharField('authority_of_pj_admin',max_length=5,default="10100")
	#au4mem = models.CharField('authority_of_mem',max_length=3,default="000")
	def __str__(self):
		return '%s' % (self.group_id)

class au4pj(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	pj_name = models.CharField('project_name',max_length = 30)
	user = models.ForeignKey(Users, on_delete=models.CASCADE)
	user_au4pj = models.CharField('user_authority4pj',max_length = 3)
	tag = models.BooleanField('creator',default=False)

	def __str__(self):
		return '%s' % (self.group.group_id)
	
class user_in_queue(models.Model):
	user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
	x = models.IntegerField('x')
	serial = models.AutoField('serial',primary_key=True, unique=True)
	
	def __str__(self):
		if self.user:
			return '%s'%(self.user.username)
		else:
			return '%s'%(self.group.group_id)
	
class user4serving(models.Model):
	user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
	t = models.IntegerField('t',default = 1)
	x = models.IntegerField('x')
	x_current = models.IntegerField('x_current')
	w = models.FloatField('w')
	
	def __str__(self):
		if self.user:
			return '%s'%(self.user.username)
		else:
			return '%s'%(self.group.group_id)
	
class task_db(models.Model):
	user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
	username = models.CharField('username',max_length=20)
	user_or_group = models.CharField('user_or_group',max_length=1) # 0 for user, 1 for group
	project_loc = models.CharField('project_loc',max_length=100)
	#authority = models.CharField('authority',max_length=20)
	request_serial_num = models.IntegerField('request_serial_num')
	#task_priority = models.IntegerField('task_priority',default=0)
	ptn_name = models.CharField('ptn_file_name',max_length=30)
	
	def __str__(self):
		return '%s-%s   %s'%(self.username,self.user_or_group,self.project_loc)
	
class allTask4user(models.Model):
	user = models.ForeignKey(Users, on_delete=models.CASCADE)
	submit_time = models.DateTimeField('submit_time',auto_now_add=True)
	finish_time = models.DateTimeField('finish_time', auto_now = True)
	finish_tag = models.BooleanField('tag',default=False)
	project_loc = models.CharField('project_loc',max_length=100)
	ptn_name = models.CharField('ptn_file_name',max_length=30)
	
	def __str__(self):
		return '%s - %.21s'%(self.user.username,self.submit_time)
		
class allTask4group(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	submitter = models.CharField('username',max_length=20)
	submit_time = models.DateTimeField('submit_time',auto_now_add=True)
	finish_time = models.DateTimeField('finish_time', auto_now = True)
	finish_tag = models.BooleanField('tag',default=False)
	project_loc = models.CharField('project_loc',max_length=100)
	ptn_name = models.CharField('ptn_file_name',max_length=30)
	
	def __str__(self):
		return '%s - %s - %.21s'%(self.group.group_id,self.group.group_name,self.submit_time)