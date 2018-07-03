import os


DIRECTORY = os.path.join(site.storage.location, "uploads")   # /path/to/mysite/
PROJECT_PATH = ''         # /mysite/uploads/project/
INCLUDE_PATH = 'include'  # /mysite/tools/include/


class FileCheck(object):
	path = ''

	def __init__(self, path):
		self.path = os.path.join(DIRECTORY, path)

	def completion_check(self):
		return 1

	def syntax_check(self):
		return 1


def test():
	pass


if __name__ == "__main__":
	test()