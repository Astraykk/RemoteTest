from Users.models import Users,Group,au4pj,user4report
from Users.models import Task,allTask4user,allTask4group,task_db,user_in_queue,user4serving

for iter in user4serving.objects.all():
	iter.delete()
for iter in user_in_queue.objects.all():
	iter.delete()
for iter in task_db.objects.all():
	iter.delete()
for iter in Task.objects.all():
	iter.delete()
for iter in user4report.objects.all():
	iter.delete()