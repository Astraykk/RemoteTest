#!/usr/bin/python3
# -*- coding:utf-8 -*-
import re
import sys
import time
import os
import json


def merge_ptn(ptn, *ptn_tuple):
	with open(ptn, 'rb+') as fw:
		for file in ptn_tuple:
			with open(file, 'rb') as fr:
				fw.write(fr.read())


def compare_ptn(file_1, file_2):
	line_cnt = 0
	with open(file_1, 'rb') as f1, open(file_2, 'rb') as f2:
		while True:
			line_cnt += 1
			line1 = f1.read(16)
			line2 = f2.read(16)
			if line1 != line2:
				print("Files differ at line %d\n" % line_cnt)
				print("{}: {}\n".format(file_1, line1))
				print("{}: {}\n".format(file_2, line2))
				break
			if not line1:
				break
		print("Comparison finished!")


def timescale_op(ts):
	regex = re.compile(r'(\d+)(\w*)', re.I)
	m = regex.match(ts)
	if m:
		unit = m.group(2)
		if unit == 'p' or unit == 'ps':
			multiplier = 1
		elif unit == 'n' or unit == 'ns':
			multiplier = 1000
		else:
			multiplier = 1000000
		ts_int = int(m.group(1)) * multiplier
	else:
		ts_int = 1
	return ts_int


def test_json(path):
	a = [1, 2, 3]
	b = {1: 1, 2: 2, 3: 3}
	d = dict(a=a, b=b)
	print(d)
	with open(path, 'r') as f:
		# json.dump(d, f)
		data2 = json.load(f)
		print(data2)


class VcdFile(object):
	# Define waveform state
	ZERO_ZERO = 1
	ZERO_ONE = 2
	ONE_ZERO = 3
	ONE_ONE = 4
	BUS_SINGLE = 5
	BUS_START = 6
	BUS_BODY = 7
	BUS_END = 8

	path = ''
	module_name = ''
	timescale = 1
	total_length = 0
	sym2sig = {}
	entri_dict = {}
	header = {'timescale': '1ps', 'version': 'ModelSim Version 10.1c', 'date': ''}
	wave_state = []
	vcd_info = []
	# vcd_info = [
	# 	{
	# 		'symbol': '!', 'sig': 'clk', 'type': 'wire', 'wave_info': [0, 1, 0, 1], 'width': 1,
	# 		'wave_state': [ZERO_ZERO, ZERO_ONE, ONE_ZERO, ZERO_ONE]
	# 	},
	# 	{
	# 		'symbol': '"', 'sig': 'a', 'type': 'reg', width: 4,
	#       'wave_info': ['0000', '0001', '0001', '0010', '0010', '0010', '0010'],
	# 		'wave_state': [BUS_SINGLE, BUS_START, BUS_END, BUS_START, BUS_BODY, BUS_BODY, BUS_END]
	# 	}
	# ]

	def __init__(self, path, period='1ps'):
		self.vcd_info = []
		self.path = path
		self.period = period
		self.get_header()

	def get_header(self):
		self.timescale = int(timescale_op(self.period) / timescale_op('1ps'))
		# TODO: find timescale in vcd file

	def get_vcd_info(self):
		vcd_tick = 0
		# timescale = int(timescale_op(self.period) / timescale_op(self.header['timescale']))
		regex1 = re.compile(r'\$var\s+(\w+)\s+(\d+)\s+(.)\s+(\w+)\s*(\[(\d+)(:?)(\d*)\])?\s+\$end', re.I)
		# $var 'type' 'width' 'symbol' 'signal' $end
		regex2 = re.compile(r'#(\d+)')                # match period
		regex3 = re.compile(r'(b?)([0|1|x|z]+)\s*(.)')  # match testbench
		with open(self.path, "r") as f:
			content = f.read()  # TODO: match signal definitions here.
			self.module_name = re.findall(r'\$scope module (\w+) \$end', content)[0]
			f.seek(0)
			for line in f.readlines():
				# print(self.vcd_info)
				m3 = regex3.match(line)
				if m3:
					base, value, key = m3.groups()
					# print(key, value)
					i = ord(key) - 33  # ASCII value, start from '!'(33)
					if key not in self.sym2sig:
						continue
					if isinstance(self.sym2sig[key], tuple):
						bus_ele = self.sym2sig[key]
						bus_width = bus_ele[1] - bus_ele[2]
						# print("{} {}".format(bus_width, bus_ele))
						# bus_signal = bus_width > 0 and 1 or -1
						value = base + '0' * (abs(bus_width) + 1 - len(value)) + value  # Fill 0 on the left
						# for i in range(0, bus_width + bus_signal, bus_signal):
						# 	bus_sig = '{}[{}]'.format(bus_ele[0], str(bus_ele[1] - i))
						# 	# print("tick={} {} {}".format(tick, bus_sig, self.sig2pos))
						# 	# print("i={}, value={}".format(i, value))
						# 	pos2val[self.sig2pos.setdefault(bus_sig, None)] = value[abs(i)]
					# print('ok')
					# print('signal = %s, value = %s' % (bus_sig, value[abs(i)]))
					# else:
					# 	if value == 'x':
					# 		value = x_val
					# 	if value == 'z':
					# 		value = z_val
					# 	pos2val[self.sig2pos.setdefault(self.sym2sig[key], None)] = value
					if vcd_tick + 1 == len(self.vcd_info[i]['wave_info']):
						self.vcd_info[i]['wave_info'][-1] = value
					else:
						self.vcd_info[i]['wave_info'].append(value)
					continue

				# match next tick; write last tick to file
				m2 = regex2.match(line)
				if m2:
					vcd_tick_raw = int(m2.group(1))
					if vcd_tick_raw == 0 or vcd_tick_raw % self.timescale:  # small delay, skip the write operation
						continue
					else:
						vcd_tick = int(vcd_tick_raw / self.timescale)
					# if tick < vcd_tick:
					for sig_dict in self.vcd_info:
						# print(sig_dict)
						last_val = sig_dict['wave_info'][-1]
						sig_dict['wave_info'] += [last_val] * (vcd_tick-len(sig_dict['wave_info']))
					continue

				m = regex1.match(line)
				if m:
					type = m.group(1)
					width = int(m.group(2))  # Warning: which type?
					sym = m.group(3)
					if m.group(7):  # Combined bus
						msb = int(m.group(6))
						lsb = int(m.group(8))
						sig = m.group(4)
						self.sym2sig[sym] = (sig, msb, lsb)  # symbol => (bus, MSB, LSB)
					elif m.group(5):
						sig = m.group(4) + m.group(5)
						self.sym2sig[sym] = sig
					else:
						sig = m.group(4)
						self.sym2sig[sym] = sig
					sig_dict = {'symbol': sym, 'signal': sig, 'type': type, 'width': width, 'wave_info': [], 'wave_state': []}
					self.vcd_info.append(sig_dict)
					# print(self.vcd_info, len(self.vcd_info))
					continue
				if re.search(r'\$dumpoff', line):
					break
			# print(vcd_tick)
			for sig_dict in self.vcd_info:
				last_val = sig_dict['wave_info'][-1]
				sig_dict['wave_info'] += [last_val] * (vcd_tick + 1 - len(sig_dict['wave_info']))
				# print(len(sig_dict['wave_info']))

	def get_wave_info(self):
		pass

	def get_tick(self):
		pass

	def gen_waveform(self, path, mode):
		pass

	def gen_vcd(self, path):
		self.header['date'] = time.asctime(time.localtime(time.time()))
		with open(path, 'w') as f:
			for header in ['date', 'version', 'timescale']:
				f.write('${}\n\t{}\n$end\n'.format(header, self.header[header]))
			f.write('$scope module {}_tb $end\n'.format(self.module_name))
			for sig_dict in self.vcd_info:
				f.write('$var {} {} {} {} $end\n'.format(sig_dict['type'], sig_dict['width'], sig_dict['symbol'], sig_dict['signal']))
			f.write('$upscope $end\n$enddefinitions $end\n')
			f.write('#0\n$dumpvars\n')
			content = ''
			for sig_dict in self.vcd_info:
				content += '{}{}\n'.format(sig_dict['wave_info'][0], sig_dict['symbol'])
			f.write(content + '$end\n')
			for i in range(1, len(self.vcd_info[0]['wave_info'])):
				content = '#{}\n'.format(i)
				for sig_dict in self.vcd_info:
					wave_info = sig_dict['wave_info']
					# print(wave_info, sig_dict['symbol'], len(wave_info))
					if wave_info[i] != wave_info[i-1]:
						content += '{}{}\n'.format(wave_info[i], sig_dict['symbol'])
				f.write(content)
			f.write('$dumpoff\n')


def vcd_merge(vcd_ref, vcd_file, path='.', compare=True):
	"""
	Merge vcd files.
	"""
	def compare_value(x, y):
		return (x == y or x == 'x' or x == 'z') and '0' or '1'

	def and_value(x, y):
		return (x == '0' and y == '0') and '0' or '1'
	fr = open(os.path.splitext(path)[0] + '.rpt', 'w')
	vcd_m = VcdFile(path, vcd_ref.period)
	for sig_dict in vcd_ref.vcd_info[:]:
		sig = sig_dict['signal'] + '_ref'
		# print(sig)
		new_dict = sig_dict.copy()
		# print(new_dict)
		new_dict['signal'] = sig
		# print(new_dict)
		# print(sig_dict)
		vcd_m.vcd_info.append(new_dict)
		vcd_m.sym2sig[sig_dict['symbol']] = sig
	offset = len(vcd_ref.vcd_info)
	for sig_dict in vcd_file.vcd_info[:]:
		sym = chr(ord(sig_dict['symbol']) + offset)
		new_dict = sig_dict.copy()
		new_dict['symbol'] = sym
		vcd_m.sym2sig[sym] = new_dict['signal']
		vcd_m.vcd_info.append(new_dict)
	# print(vcd_merge.vcd_info)
	if compare:  # generate error signal
		sym = chr(len(vcd_m.vcd_info) + 33)
		sig = 'error'  # TODO: check signal name clash
		wave_info = ['0'] * len(vcd_ref.vcd_info[0]['wave_info'])
		# for i in range(len(vcd_ref.vcd_info)):  # directly compare 2 lists
		# 	ref_dict = vcd_ref.vcd_info[i]['wave_info']
		# 	act_dict = vcd_file.vcd_info[i]['wave_info']
		# 	compare_result = list(map(compare_value, ref_dict, act_dict))
		# 	wave_info = list(map(and_value, wave_info, compare_result))
		# print(len(vcd_ref.vcd_info))
		for i in range(len(vcd_ref.vcd_info[0]['wave_info'])):  # tick
			for j in range(len(vcd_ref.vcd_info)):  # signal
				# print(i, j)
				x = vcd_ref.vcd_info[j]['wave_info'][i]
				y = vcd_file.vcd_info[j]['wave_info'][i]
				sig_ref = vcd_ref.vcd_info[j]['signal']
				sig_act = vcd_file.vcd_info[j]['signal']
				if x != 'x' and x != 'z' and x != y:
					fr.write('Line {}: {}_ref = {}, {} = {}\n'.format(i, sig_ref, x, sig_act, y))  # report
					wave_info[i] = '1'  # generate wave info for error_dict
		# print(wave_info)
		error_dict = {
			'symbol': sym, 'signal': sig, 'type': 'wire', 'width': 1, 'wave_info': list(wave_info), 'wave_state': []
		}
		vcd_m.sym2sig[sym] = sig
		vcd_m.vcd_info.append(error_dict)
	fr.close()
	return vcd_m


if __name__ == "__main__":
	'''vcd test'''
	# # compare_ptn('counter/counter.ptn', 'counter/counter.ptn.bak1207')
	# vcd = VcdFile('pin_test/pin_test.vcd', period='1ps')
	# # vcd = VcdFile('counter/counter.vcd', period='1ps')
	# # vcd = VcdFile('mul5/mul5.vcd', period='1us')
	# vcd.get_vcd_info()
	# # vcd.gen_vcd('pin_test/p3.vcd')
	# # vcd.gen_vcd('mul5/m9.vcd')
	#
	# # test vcd_merge
	# vcd1 = VcdFile('pin_test/p2.vcd', period='1ps')
	# print('vcd1 = ', vcd1.vcd_info)
	# vcd1.get_vcd_info()
	# vcd2 = vcd_merge(vcd, vcd1, 'pin_test/p2_merge.vcd')
	# print(vcd2.sym2sig)
	# # vcd2.gen_vcd('pin_test/p1_merge.vcd')
	# vcd2.gen_vcd(vcd2.path)

	'''json test'''
	test_json('temp.json')
