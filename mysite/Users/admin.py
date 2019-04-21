import admin
from .models import Users,allTask4user,allTask4group
from .models import Task,Group,Group_item,Invitation,au4pj,au4group,task_db,user_in_queue,user4serving
# Register your models here.
admin.site.register(Users)
admin.site.register(Task)
admin.site.register(task_db)
admin.site.register(allTask4user)
admin.site.register(allTask4group)
admin.site.register(Group)
admin.site.register(Group_item)
admin.site.register(Invitation)
admin.site.register(au4pj)
admin.site.register(au4group)
admin.site.register(user_in_queue)
admin.site.register(user4serving)

