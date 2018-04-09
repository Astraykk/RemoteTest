import re


def _file_process(file, regex):
	dict = {}
	with open(file, "r") as fp:
		for line in fp.readlines():
			# print(line)
			m = regex.match(line)
			if m:
				dict[m.group(1)] = m.group(2)
	print(dict)
	return dict


def data_parser(file):
	regex = re.compile(r'(data\d): (\d+)')
	return _file_process(file, regex)


def operator_parser(file):
	regex = re.compile(r'(operator): (0x80{6}\d)')
	return _file_process(file, regex)


def app_execution(data1, data2, operator):
	return_value = os.popen('/path/to/arithmetic_intr_mmap_test_app'+ data1 + data2 + operator).read()
	return return_value



print(data_parser("data"))
a = operator_parser("operator")
print(hex(int(a["operator"], 16)))  # turn hex string to hex
