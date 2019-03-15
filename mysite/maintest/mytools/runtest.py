import sys

if len(sys.argv) < 3:
	print("help message")
	sys.exit()
i_file, o_file = sys.argv[1:3]
if len(sys.argv) < 4:
	command = '-c'
else:
	command = sys.argv[3]
try:
	with open(o_file, 'w') as fw:
		fw.write('test result')
	print('test succeed!')
except Exception as err:
	print(err)

