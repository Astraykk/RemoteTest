#!/usr/bin/python3
# -*- coding:utf-8 -*-
from mytools import VcdFile, vcd_merge
import sys


def test():
	vcd_ref = VcdFile('pin_test/pin_test.vcd', period='1ps')
	vcd_ref.get_vcd_info()
	vcd1 = VcdFile('pin_test/p1.vcd', period='1ps')
	vcd1.get_vcd_info()
	vcd2 = vcd_merge(vcd_ref, vcd1)
	vcd2.gen_vcd('pin_test/p1_merge.vcd')


if __name__ == "__main__":
	if len(sys.argv) == 1:
		test()
	elif len(sys.argv) == 6:
		path1, period1, path2, period2, pathm = sys.argv[1:]
		vcd1 = VcdFile(path1, period=period1)
		vcd1.get_vcd_info()
		vcd2 = VcdFile(path2, period=period2)
		vcd2.get_vcd_info()
		vcdm = vcd_merge(vcd1, vcd2)
		vcdm.gen_vcd(pathm)