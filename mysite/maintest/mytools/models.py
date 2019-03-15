import time
import os
import json


class Project(object):
	def __init__(self, name, user, path):
		self.name = name
		self.user = user
		self.path = path
		self.start_time = time.time()
		self.last_modified = time.time()
		self.status = {'check': 0, 'build': 0, 'test': 0, 'report': 0}
		self.major_files = {}
		self.minor_files = {}
		self.generated_files = {}

	def close(self):
		self.last_modified = time.time()
		# format time: time.asctime(time.localtime(time.time()))
		data_path = os.path.join(self.path, 'project_data.json')
		with open(data_path, "w+") as f:
			json.dump(self.__dict__, f)

	def details(self):
		print('\n'.join(['%s = %s' % item for item in self.__dict__.items()]))

	def destroy(self):
		pass


def test():
	project = Project('counter', 'kcl', '.')
	project.details()
	project.close()


if __name__ == '__main__':
	test()