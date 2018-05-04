import re, sys, os, struct
import bs4
from bs4 import BeautifulSoup
import timeit


DIRECTORY = os.path.join(sys.path[0], "pin_test")
signal = {}

# define operation code here
MASK_OP = 0x1
TESTBENCH_OP = 0x4
BITSTREAM_OP = None
# enddefine

# define other global constants
BIN_WIDTH = 128
BIN_BYTE_WIDTH = BIN_WIDTH / 8
# enddefine


def name_check(file, name):
	filename = os.path.splitext(file)[0]
	if filename == name:
		print(file + " name check pass!")
	else:
		print(file + " name mismatch!")


def get_soup(file):
	path = os.path.join(DIRECTORY, file)
	with open(path, "r") as f:
		soup = BeautifulSoup(f.read(), "xml")
	return soup


def file_check(file_dict):
	"""
	Check file integrity.
	:return:
	"""
	pass


"""Write operation, mask, or testbench"""


def write_testbench(fw, pos_dict):
	if not pos_dict:
		# print("Nothing")
		return
	numbers = [0] * 16
	for key, value in pos_dict.items():
		if key:
			numbers[key[0]-1] += 2 ** key[1] * int(value)
			# numbers[key[0]-1] += int(value) << key[1]  # shift operation is faster?
	for num in numbers:
		fw.write(struct.pack('B', num))
	# print("write success")


def write_operator(fw, operator, length):
	fw.write(struct.pack('B', operator))  # 1 byte
	for i in range(11):                   # length takes 4 bytes
		fw.write(struct.pack('B', 0xff))
	fw.write(struct.pack('>I', length))    # 4 bytes, big-endian


def write_tb_op(fw, tb_counter):
	if tb_counter:
		offset = - int((tb_counter + 1) * BIN_BYTE_WIDTH)
		fw.seek(offset, 1)    # locate the beginning of testbench
		write_operator(fw, TESTBENCH_OP, tb_counter)
		fw.seek(0, 2)         # return to end of file


def write_mask(fw, sig_dict, pio_dict, tb_counter):
	"""
	Run at the beginning of the process, and anytime en_tri changes.
	Write mask (pin input/output/inout status) to file.
	If there is any testbench written before, write op code for it.
	(Abandon) entri_dict: a dict contain the en_tri pin status, {en_tri1:0, en_tri2:1, ...}
	:return:
	"""
	numbers = [0xff] * 16
	write_tb_op(fw, tb_counter)
	write_operator(fw, MASK_OP, 1)
	for key, value in sig_dict.items():
		if pio_dict.setdefault(key, None) == 'input':  # TODO: maybe value in pio_dict should be 0/1?
			numbers[value[0]-1] -= 2 ** value[1]
	for num in numbers:
		fw.write(struct.pack('B', num))
	write_operator(fw, TESTBENCH_OP, 0)


"""File Parsers"""


def tcf_parser(file, sig2pin):
	soup = get_soup(file)
	name_check(file, soup.TCF['name'])
	for key, value in sig2pin.items():
		# FRAME & ASSEMBLY tag
		connect_tag = soup.find(pogo=value[:3])
		# TODO: Change the search parameter, or change attr 'name' to 'id'.
		assembly_name = connect_tag['assembly']                 # should search by 'AS0101',
		wire_tag = soup.find(code=assembly_name).find(pogopin=value[3:])  # not this
		# print(wire_tag)
		channel = connect_tag['plug'] + wire_tag['plugpin']

		# SIGMAP tag
		mapping_tag = soup.find(channel=channel)
		byte = int(mapping_tag['byte'])
		bit = int(mapping_tag['bit'])
		sig2pin[key] = (byte, bit)


"""
def tcf_parser(file, sig2pin):
	soup = get_soup(file)
	name_check(file, soup.TCF['name'])
	# FRAME tag
	for key, value in sig2pin.items():
		# FRAME tag
		channel = soup.find(pogo=value[:3])['plug'] + value[3:]
		# SIGMAP tag
		mapping_tag = soup.find(channel=channel)
		byte = int(mapping_tag['byte'])
		bit = int(mapping_tag['bit'])
		sig2pin[key] = (byte, bit)
"""


def lbf_parser(file, sig2pin):
	soup = get_soup(file)
	name_check(file, soup.LBF['name'])
	# dut_tag = soup.find('DUT').children
	for key in sig2pin:
		sig2pin[key] = soup.find(pin=sig2pin[key])['channel']
	# print(sig2pin)
	return sig2pin


def itm_parser(file):
	soup = get_soup(file)
	name_check(file, soup.ITEM['name'])
	return soup.find('CYCLE')['period']


def pio_parser(file):
	pio_dict = {}
	entri_dict = {}
	path = os.path.join(DIRECTORY, file)
	regex = re.compile(r'NET\s+"(.+)"\s+DIR\s*=\s*(input|output|inout)(.*);', re.I)
	regex2 = re.compile(r'.*"(.*)"\s*')
	with open(path, "r") as f:
		for line in f.readlines():
			m = regex.match(line)
			if m:
				# print(m.groups())
				io = m.group(2).lower()
				pio_dict[m.group(1)] = io
				if io == 'inout':
					tri = regex2.match(m.group(3)).group(1)
					# print(1, tri)
					entri_dict[tri] = m.group(1)
	# print(pio_dict, entri_dict)
	return pio_dict, entri_dict


def ucf_parser(file):
	sig2pin = {}
	path = os.path.join(DIRECTORY, file)
	regex = re.compile('NET "(.+)" LOC = (.+);', re.I)
	with open(path, "r") as f:
		for line in f.readlines():
			m = regex.match(line)
			if m:
				sig2pin[m.group(1)] = m.group(2)
	return sig2pin


def vcd_parser(file, sig_dict, pio_dict, entri_dict={}):
	tick = -1         # current tick
	tb_counter = -1    # length of testbench in operation code
	def_state = True  # definition state
	sym_dict = {}     # {symbolic_in_vcd: signal_name}
	pos_dict = {}     # {position(bit): signal(1|0|z|x)}
	path = os.path.join(DIRECTORY, file)
	write_path = os.path.join(DIRECTORY, os.path.splitext(file)[0] + ".bin")
	regex1 = re.compile(r'\$var .+ \d+ (.) (.+) \$end', re.I)   # match signal name
	regex2 = re.compile(r'#(\d+)')                              # match period
	regex3 = re.compile(r'([0|1|x|z])(.)')                      # match testbench

	if not os.path.exists(write_path):
		os.mknod(write_path)
	with open(path, "r") as f, open(write_path, "r+b") as fw:
		for line in f.readlines():
			# end of file
			if line == '$dumpoff':
				break

			# definition stage, return {symbol:signal, }
			if def_state:
				m1 = regex1.match(line)
				if m1:
					sym_dict[m1.group(1)] = m1.group(2)
				else:
					if re.match(r'\$upscope', line):
						def_state = False
				continue
			else:
				# write last tick to file
				m2 = regex2.match(line)
				if m2:
					vcd_tick = m2.group(1)
					while True:  # WARNING
						# if not pos_dict:  # ugly code
						# 	break
						# print(pos_dict)
						write_testbench(fw, pos_dict)  # Write testbench to binary file.
						print("#"+str(tick))
						tb_counter += 1
						tick += 1
						if tick == int(vcd_tick):
							# pos_dict = {}
							break
					continue

				# match testbench
				m3 = regex3.match(line)
				if m3:
					value = m3.group(1)
					key = m3.group(2)
					pos_dict[sig_dict.setdefault(sym_dict[key], None)] = value
					# print(sym_dict[key])
					# TODO: interrupt when en_tri signal changes.
					if sym_dict[key] in entri_dict:
						entri = sym_dict[key]  # TODO: change entri_dict
						# print(pos_dict[sig_dict[entri]])
						if pos_dict[sig_dict[entri]] == '1':
							pio_dict[entri_dict[entri]] = 'output'
						else:
							pio_dict[entri_dict[entri]] = 'input'
						# print(pio_dict)
						write_mask(fw, sig_dict, pio_dict, tb_counter)
						tb_counter = 0
		write_tb_op(fw, tb_counter)


def tfo_parser(file):
	"""
	TODO: Multiple TEST tag, different attr 'name' and 'path'.
	TODO: Return file_dict like {test1:{path:'path', file1:'file1', ...}, test2:{...}, ...}.
	Format: {"lbf":"LB010tf1", dut:"LX200", "test":{"pin_test":{"path":".", }}}
	:param file:
	:return file_dict:
	"""
	soup = get_soup(file)
	name_check(file, soup.TFO['name'])
	file_dict = {}
	test_tag = soup.find('TEST')
	for child in test_tag.children:
		if type(child) == bs4.element.Tag:
			file_dict[child.name] = child['name'] + '.' + child.name.lower()
	return file_dict


def prepare(file):
	pass


"""Main process and test"""


def main():
	period = itm_parser("pin_test.itm")
	signal = ucf_parser("pin_test.ucf")
	lbf_parser("LB0101.lbf", signal)
	tcf_parser("F93K.tcf", signal)
	print(signal)
	pio_dict = pio_parser("pin_test.pio")
	write_mask(pio_dict)
	vcd_parser("pin_test.vcd", signal)


def test():
	pio_dict, entri_dict = pio_parser("pin_test.pio")
	print("pio_dict = "+str(pio_dict))
	print("entri_dict = "+str(entri_dict))
	signal = ucf_parser("pin_test.ucf")
	print(signal)
	lbf_parser("LB0101.lbf", signal)
	print(signal)
	tcf_parser("F93K.tcf", signal)
	print("sig_dict = "+str(signal))
	vcd_parser("pin_test.vcd", signal, pio_dict, entri_dict)
	print("Finished")


test()
# print(timeit.Timer("test()", "from __main__ import test").timeit(10))
