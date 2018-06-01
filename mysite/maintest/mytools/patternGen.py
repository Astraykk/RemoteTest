import re, sys, os, struct
import bs4
from bs4 import BeautifulSoup
import time
from filebrowser.sites import site
# import timeit

# DIRECTORY = sys.path[0]   # /path/to/mysite/
DIRECTORY = os.path.join(site.storage.location, "uploads")   # /path/to/mysite/
PROJECT_PATH = ''         # /mysite/uploads/project/
INCLUDE_PATH = 'include'  # /mysite/tools/include/

# define operation code here
MASK_OP = 0x1
BITSTREAM_OP = 0x2
TESTBENCH_OP = 0x4
END_OP = 0x80
# enddefine

# define other global constants
BIN_WIDTH = 128
BIN_BYTE_WIDTH = int(BIN_WIDTH / 8)
BITSTREAM_WIDTH = 32
# end define

"""Tools"""


def timer(func):
	# decorator without parameter
	def _timer():
		start_time = time.time()
		func()
		end_time = time.time()
		print("\nTotal time: " + str(end_time-start_time))
	return _timer


def name_check(file, name):
	filename = os.path.splitext(file)[0]
	if filename == name:
		print(file + " name check pass!")
	else:
		print(file + " name mismatch!")


def get_soup(path, file):
	path = os.path.join(path, file)
	# print(path)
	with open(path, "r") as f:
		soup = BeautifulSoup(f.read(), "xml")
	return soup


def itm_parser(relpath, file):
	soup = get_soup(relpath, file)
	name_check(file, soup.ITEM['name'])
	return soup.find('CYCLE')['period']


"""Write operation, mask, or testbench"""


def write_content(fw, pos_dict):
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


def write_length(fw, length):
	if length:
		offset = - int(length * BIN_BYTE_WIDTH + 4)
		fw.seek(offset, 1)    # locate the beginning of testbench
		fw.write(struct.pack('>I', length))
		fw.seek(0, 2)         # return to end of file


def write_mask(fw, sig2pos, sig2pio):  # static
	numbers = [0xff] * 16
	write_operator(fw, MASK_OP, 1)
	for key, value in sig2pos.items():
		if sig2pio.setdefault(key, None) == 'input':  # TODO: maybe value in pio_dict should be 0/1?
			numbers[value[0] - 1] -= 2 ** value[1]
	for num in numbers:
		fw.write(struct.pack('B', num))


def get_sig_value(dictionary, tick=0):
	"""
	format:
		flag = 'const': value = 0/1, default = (don't care)
		flag = 'square': value = (don't care), default = 0/1
		flag = 'T': value=[[number1, 0/1], [number2, 0/1], ...], default = 0/1
	:param dictionary:
	:param tick:
	:return:
	"""
	value = dictionary.setdefault('value', 0)
	flag = dictionary.setdefault('flag', 'const')
	default = dictionary.setdefault('default', 0)
	if flag == 'const':
		return value
	if flag == 'square':
		return (tick + default) % 2
	if flag == 'T':
		vp = default
		for t, v in value:
			if tick >= t:
				vp = v
			else:
				return vp
		return vp


"""File Parsers"""


class PatternGen(object):
	# path and file
	path = '.'
	include_path = os.path.join(DIRECTORY, INCLUDE_PATH)
	file_list = {'TCF': 'F93K.tcf', 'ATF': 'pin_test.atf'}

	# variable
	tick = 0      # write clock
	bs_start = 0  # start of bitstream

	# signal dictionary
	cmd2spio = {}
	cmd2pos = {}
	cmd2flag = {}
	pos2data = {}
	nop = {}

	sig2pio = {}
	sig2pos = {}
	entri_dict = {}

	def __init__(self, path, tfo_file):
		self.path = os.path.join(DIRECTORY, path)
		self.tfo_parser(tfo_file)
		self.atf_parser(self.file_list['ATF'])

		# initialize bitstream info
		self.cmd2spio, whatever = self.pio_parser(self.include_path, self.file_list['SPIO'])
		cmd2pin = self.ucf_parser(self.include_path, self.file_list['SUCF'])
		cmd2channel = self.lbf_parser(self.file_list['LBF'], cmd2pin)
		self.cmd2pos = self.tcf_parser(self.file_list['TCF'], cmd2channel)
		self.sbc_parser(self.file_list['SBC'])

		# initialize testbench info
		self.sig2pio, self.entri_dict = self.pio_parser(self.path, self.file_list['PIO'])
		sig2pin = self.ucf_parser(self.path, self.file_list['UCF'])
		sig2channel = self.lbf_parser(self.file_list['LBF'], sig2pin)
		self.sig2pos = self.tcf_parser(self.file_list['TCF'], sig2channel)

	def tfo_parser(self, file):
		"""
		TODO: Multiple TEST tag, different attr 'name' and 'path'.
		TODO: Return file_dict like {test1:{path:'path', file1:'file1', ...}, test2:{...}, ...}.
		Format: {"lbf":"LB010tf1", dut:"LX200", "test":{"pin_test":{"path":".", }}}
		:param file:
		:return file_dict:
		"""
		soup = get_soup(self.path, file)
		name_check(file, soup.TFO['name'])
		self.file_list['LBF'] = soup.TFO.LBF['type'] + '.lbf'
		test_tag = soup.find('TEST')
		self.file_list['BIN'] = test_tag['name'] + '.bin'
		# self.path = test_tag['path']
		for child in test_tag.children:
			if type(child) == bs4.element.Tag:
				if child.name == 'DWM' or child.name == 'BIT':
					self.file_list[child.name] = child['name']
				else:
					self.file_list[child.name] = child['name'] + '.' + child.name.lower()

	@staticmethod
	def pio_parser(path, file):
		pio_dict = {}
		entri_dict = {}
		path = os.path.join(path, file)
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

	@staticmethod
	def ucf_parser(path, file):
		sig2pin = {}
		path = os.path.join(path, file)
		regex = re.compile(r'NET\s+"(.+)"\s+LOC =(.+);', re.I)
		with open(path, "r") as f:
			for line in f.readlines():
				m = regex.match(line)
				if m:
					sig2pin[m.group(1)] = m.group(2).strip()
		return sig2pin

	def atf_parser(self, file):
		# print(self.path)
		soup = get_soup(self.path, file)
		name_check(file, soup.ATF['name'])
		dwm_tag = soup.ATF.LIST.DWM
		for child in dwm_tag.children:
			if type(child) == bs4.element.Tag:
				self.file_list[child.name] = child['name'] + '.' + child.name.lower()

	def lbf_parser(self, file, sig2pin):
		soup = get_soup(self.include_path, file)
		name_check(file, soup.LBF['name'])
		# dut_tag = soup.find('DUT').children
		sig2channel = {}
		for key in sig2pin:
			connect_tag = soup.find(pin=sig2pin[key])
			if connect_tag:  # collect exception
				sig2channel[key] = connect_tag['channel']
			else:
				sig2channel[key] = None
		return sig2channel

	def tcf_parser(self, file, sig2channel):
		soup = get_soup(self.include_path, file)
		name_check(file, soup.TCF['name'])
		sig2pos = {}
		for key, value in sig2channel.items():
			# FRAME & ASSEMBLY tag
			connect_tag = soup.find(pogo=value[:3])
			assembly_name = connect_tag['assembly']  # should search by 'AS0101',
			wire_tag = soup.find(code=assembly_name).find(pogopin=value[3:])  # not this
			channel = connect_tag['plug'] + wire_tag['plugpin']

			# SIGMAP tag
			mapping_tag = soup.find(channel=channel)
			byte = int(mapping_tag['byte'])
			bit = int(mapping_tag['bit'])
			sig2pos[key] = (byte, bit)
		return sig2pos

	def vcd_parser(self, fw):
		tick = -1         # current tick
		tb_counter = -1   # length of testbench in operation code
		def_state = True  # definition state
		sym2sig = {}      # {symbolic_in_vcd: signal_name}
		pos2val = {}      # {position(bit): signal(1|0|z|x)}
		path = os.path.join(self.path, self.file_list['VCD'])
		write_path = os.path.join(self.path, self.file_list['BIN'])
		regex1 = re.compile(r'\$var .+ \d+ (.) (.+) \$end', re.I)  # match signal name
		regex2 = re.compile(r'#(\d+)')                             # match period
		regex3 = re.compile(r'([0|1|x|z])(.)')                     # match testbench

		if not os.path.exists(write_path):
			os.mknod(write_path)
		with open(path, "r") as f:
			for line in f.readlines():
				# end of file
				if line == '$dumpoff':
					break

				# definition stage, return sym2sig = {symbol:signal, ...}
				if def_state:
					m1 = regex1.match(line)
					if m1:
						sym2sig[m1.group(1)] = m1.group(2)
					else:
						if re.match(r'\$upscope', line):
							def_state = False
					continue
				else:
					# match next tick; write last tick to file
					m2 = regex2.match(line)
					if m2:
						vcd_tick = m2.group(1)
						while True:
							write_content(fw, pos2val)  # Write testbench to binary file.
							tb_counter += 1
							tick += 1
							if tick == int(vcd_tick):
								break
						continue

					# match testbench
					m3 = regex3.match(line)
					if m3:
						value = m3.group(1)
						key = m3.group(2)
						pos2val[self.sig2pos.setdefault(sym2sig[key], None)] = value
						if sym2sig[key] in self.entri_dict:
							entri = sym2sig[key]
							if pos2val[self.sig2pos[entri]] == '1':
								self.sig2pio[self.entri_dict[entri]] = 'output'
							else:
								self.sig2pio[self.entri_dict[entri]] = 'input'
							write_length(fw, tb_counter)
							write_mask(fw, self.sig2pos, self.sig2pio)
							write_operator(fw, TESTBENCH_OP, 0)
							tb_counter = 0
			write_length(fw, tb_counter)

	def sbc_parser(self, file):
		soup = get_soup(self.include_path, file)
		name_check(file, soup.SBC['name'])

		# Handle SIG tag
		for element in soup.find_all('SIG'):
			ele_value = element['value']
			regex1 = re.compile(r'(const)([0|1])')  # flag = const
			m1 = regex1.search(ele_value)  # const has the highest priority
			if m1:
				flag, value = m1.groups()
				value = int(value)
			else:
				regex2 = re.compile(r'^(square)(\d+)T$')  # flag = square
				m2 = regex2.match(ele_value)
				if m2:
					flag, value = m2.groups()
					value = int(value)
				else:
					regex3 = re.compile(r'(\d+)T([0|1])')  # flag = T
					m3 = regex3.findall(ele_value)
					if m3:
						value = [list(map(int, x)) for x in m3]
						flag = 'T'
					else:  # collect default
						flag = ''
						value = 0
			default = int(element['default'])
			self.cmd2flag[element['name']] = {'value': value, 'flag': flag, 'default': default}

		# Handle BTC tag
		btc_tag = soup.find('BTC')
		self.bs_start = int(btc_tag['start'][:-1])
		for child in btc_tag.find_all('DATA'):
			num = (int(child['byte']) - 1) * 8 + 7 - int(child['bit'])
			self.pos2data[num] = child['name']

		# Handle NOP tag
		nop_tag = soup.find('NOP')
		self.nop['start'] = nop_tag['start']
		self.nop['cycle'] = int(nop_tag['cycle'][:-1])

	def rbt_generator(self, file):
		"""
		Generator, yield the position of bitstream.
		:return:
		"""
		path = os.path.join(self.path, file)
		with open(path, 'r') as f:
			for i in range(7):  # skip the first 7 lines
				f.readline()
			while True:
				line = f.readline()
				if not line:
					break
				yield line

	def write_command(self, fw):
		pos2val = {}
		for key, flag in self.cmd2flag.items():
			value = get_sig_value(flag, self.tick)
			pos2val[self.cmd2pos[key]] = value
		write_content(fw, pos2val)

	def write_bitstream(self, fw):
		pos2val = {}
		gen = self.rbt_generator('pin_test.rbt.bak')
		# gen = self.rbt_generator(self.file_list['BIT'] + '.rbt')
		for line in gen:
			# print(self.tick, line)
			for key, flag in self.cmd2flag.items():
				value = get_sig_value(flag, self.tick)
				pos2val[self.cmd2pos[key]] = value
			for i, value in enumerate(line.strip('\n')):
				# if i >= 32:  # TODO: UGLY CODE!!!
				# 	break
				# print(i, value)
				sig = self.pos2data[i]
				pos = self.cmd2pos[sig]
				pos2val[pos] = value
			write_content(fw, pos2val)
			self.tick += 1

	def write_nop(self, fw):
		start = self.nop['start']
		cycle = self.nop['cycle']
		# print(start, cycle)
		fw.seek(-BIN_BYTE_WIDTH, 1)
		line = fw.read()
		fw.seek(0, 2)
		if start == 'AFB':
			for i in range(cycle):
				fw.write(line)
				self.tick += 1
		else:
			start = int(start)
			while self.tick <= start:
				fw.write(line)
				self.tick += 1
		write_length(fw, self.tick)

	def write(self):
		path = os.path.join(self.path, self.file_list['BIN'])
		with open(path, 'wb+') as fw:
			write_mask(fw, self.cmd2pos, self.cmd2spio)
			write_operator(fw, BITSTREAM_OP, 0)
			while self.tick < self.bs_start:
				# print(self.tick)
				self.write_command(fw)
				self.tick += 1

			self.write_bitstream(fw)
			self.write_nop(fw)

			self.vcd_parser(fw)
			write_operator(fw, END_OP, 0)
			print("Finished!")


"""Main process and test"""


@timer
def test():
	# from patternGen import PatternGen
	pattern = PatternGen(PROJECT_PATH, 'tfo_demo.tfo')
	pattern.write()
	# print('path = ' + pattern.path)
	# print('include path = ' + pattern.include_path)
	# print('file list = ' + str(pattern.file_list))
	# print('cmd2spio = ' + str(pattern.cmd2spio))
	# print('cmd2pos = ' + str(pattern.cmd2pos))
	# print('cmd2flag = ' + str(pattern.cmd2flag))
	# print('bs_start = ' + str(pattern.bs_start))
	# print('pos2data = ' + str(pattern.pos2data))
	# print('nop = ' + str(pattern.nop))
	# print('sig2pio = ' + str(pattern.sig2pio))
	# print('entri_dict = ' + str(pattern.entri_dict))
	# print('sig2pos = ' + str(pattern.sig2pos))

	print('\n'.join(['%s = %s' % item for item in pattern.__dict__.items()]))
	print(pattern.__dir__())
	# pattern.write()


if __name__ == "__main__":
	test()