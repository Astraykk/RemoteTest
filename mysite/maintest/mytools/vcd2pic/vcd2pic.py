import re
import enum
import os
import sys
import json
#constants for state shift
class State(enum.Enum):
	I_X_X = 0
	I_Z_X = 1
	I_0_X = 2
	I_1_X = 3
	I_X_Z = 4
	I_Z_Z = 5
	I_0_Z = 6
	I_1_Z = 7
	I_X_0 = 8
	I_Z_0 = 9
	I_0_0 = 10
	I_1_0 = 11
	I_X_1 = 12
	I_Z_1 = 13
	I_0_1 = 14
	I_1_1 = 15
	I_BUS_TRAN = 16
	I_BUS_INIT = 17

def read_dataline(line):
	wave_data=''
	wave_sign=''
	#bus pattern: (b|o|d|h)(wave data)(white space)(sign)
	if re.search(r'^(b|o|d|h)',line):
		stoppos=len(line[:-2].strip())
		wave_data = line[1:stoppos]
		wave_sign=line[-2]
	#non-bus pattern: (wave data)(sign)
	else:
		wave_data = line[0]
		wave_sign=line[1:].strip()
	return wave_data, wave_sign

def parsevcd(vcd_location):
	with open(vcd_location) as vcd:
		inputs = []
		outputs = []
		for each_line in vcd:
			word = each_line.strip().split()
			if not word:
				continue
			if word[0] == '$date':
				vcd.readline()
			if word[0] == '$version':
				vcd.readline()
			if word[0] == '$timescale':
				timescale = vcd.readline()
				timescale_value = re.search(r'\d',timescale).group()
				timescale_scale = re.search(r'[a-z]{1,2}',timescale).group()
			if word[0] == '$scope':
				pass
			if word[0] == '$var':
			#sometimes buses may have bit index seperated from their names, fix this
				signame = word[4]
				if word[5] != '$end':
					signame += word[5]
				sigdat = {'name':signame,'sign':word[3],'width':word[2],'wave':[],'state':[],'time':[]}
				if word[1] == "reg":
					inputs.append(sigdat)
				elif word[1] == "wire":
					outputs.append(sigdat)
				elif word[1] == "parameter":
					outputs.append(sigdat)
			line = each_line
			while re.search(r'^#',line):
				time = re.search(r'\d+',line).group()
				line = vcd.readline()
				if line == '$dumpvars\n':
					waveout = inputs + outputs
					line = vcd.readline()
				while (len(line)>1 and line[0] != '#'):
					if line[0] == '$':
						line = vcd.readline()
						continue
					data, sign = read_dataline(line)
					for i in range(len(waveout)):
						if sign == waveout[i]['sign']:
							waveout[i]['wave'].append(data)
							waveout[i]['time'].append(int(time))
							break
					line = vcd.readline()
				if line == '$end\n':
					line = vcd.readline()
					continue
	for i in range(len(waveout)):
		if(waveout[i]['width'] == '1'):
			for j in range(len(waveout[i]['wave'])):
				if j == 0:
					now_wave = waveout[i]['wave'][j]
					if now_wave == 'x':
						waveout[i]['state'].append(State.I_X_X.value)
					elif now_wave == 'z':
						waveout[i]['state'].append(State.I_Z_Z.value)
					elif now_wave == '0':
						waveout[i]['state'].append(State.I_0_0.value)
					elif now_wave == '1':
						waveout[i]['state'].append(State.I_1_1.value)
				else:
					b_wave = waveout[i]['wave'][j - 1]
					now_wave = waveout[i]['wave'][j]
					if b_wave == 'x' and now_wave == 'x':
						waveout[i]['state'].append(State.I_X_X.value)
					elif b_wave == 'z' and now_wave == 'x':
						waveout[i]['state'].append(State.I_Z_X.value)
					elif b_wave == '0' and now_wave == 'x':
						waveout[i]['state'].append(State.I_0_X.value)
					elif b_wave == '1' and now_wave == 'x':
						waveout[i]['state'].append(State.I_1_X.value)
					elif b_wave == 'x' and now_wave == 'z':
						waveout[i]['state'].append(State.I_X_Z.value)
					elif b_wave == 'z' and now_wave == 'z':
						waveout[i]['state'].append(State.I_Z_Z.value)
					elif b_wave == '0' and now_wave == 'z':
						waveout[i]['state'].append(State.I_0_Z.value)
					elif b_wave == '1' and now_wave == 'z':
						waveout[i]['state'].append(State.I_1_Z.value)
					elif b_wave == 'x' and now_wave == '0':
						waveout[i]['state'].append(State.I_X_0.value)
					elif b_wave == 'z' and now_wave == '0':
						waveout[i]['state'].append(State.I_Z_0.value)
					elif b_wave == '0' and now_wave == '0':
						waveout[i]['state'].append(State.I_0_0.value)
					elif b_wave == '1' and now_wave == '0':
						waveout[i]['state'].append(State.I_1_0.value)
					elif b_wave == 'x' and now_wave == '1':
						waveout[i]['state'].append(State.I_X_1.value)
					elif b_wave == 'z' and now_wave == '1':
						waveout[i]['state'].append(State.I_Z_1.value)
					elif b_wave == '0' and now_wave == '1':
						waveout[i]['state'].append(State.I_0_1.value)
					elif b_wave == '1' and now_wave == '1':
						waveout[i]['state'].append(State.I_1_1.value)
		else:
			for j in range(len(waveout[i]['wave'])):
				if j == 0:
					waveout[i]['state'].append(State.I_BUS_INIT.value)
				else:
					waveout[i]['state'].append(State.I_BUS_TRAN.value)
	return waveout, (time,timescale_scale)
def wave2json(waveout, *extra):
	'''
	note: change waveout because waveout['sign'] may use ' and " which may interfere with
	json parser. hence removed.'''
	for i in range(len(waveout)):
		del waveout[i]['sign']
	jsdat=json.dumps(dict(dat=waveout,time=extra[0]))
	return jsdat
		
def vcd2pic(vcd_location):
	waveout, time=parsevcd(vcd_location)
	jsdat=wave2json(waveout,time)
	return jsdat
