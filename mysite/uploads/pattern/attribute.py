filelist = {'ATF': 'pin_test.atf', 'BIN': u'pin_test_0517.bin',
             'ITM': u'pin_test.itm', 'VCD': u'pin_test.vcd',
             'RPT': u'pin_test.rpt', 'PIO': u'pin_test.pio',
             'SUCF': u'LX200.sucf', 'SBC': u'LX200.sbc',
             'UCF': u'pin_test.ucf', 'LBF': u'LB0101.lbf',
             'TCF': 'F93K.tcf', 'WAV': u'pin_test.wav',
             'BIT': u'pin_test', 'SPIO': u'LX200.spio',
             'DWM': u'SelectMAP32'}
cmd2spio = {'RDWR_B': 'input', 'D14': 'input', 'D16': 'input', 'TMS': 'input', 'D10': 'input', 'PROG_B': 'input', 'D12': 'input', 'D13': 'input', 'D15': 'input', 'D19': 'input', 'D30': 'input', 'D31': 'input', 'D7': 'input', 'DONE': 'output', 'M0': 'input', 'M2': 'input', 'D28': 'input', 'D11': 'input', 'DOUT_BUSY': 'output', 'TCK': 'input', 'D20': 'input', 'D29': 'input', 'PWRDWN_B': 'input', 'D17': 'input', 'D18': 'input', 'D23': 'input', 'D22': 'input', 'D25': 'input', 'D24': 'input', 'D27': 'input', 'D26': 'input', 'CCLK': 'input', 'D_IN': 'input', 'TDI': 'input', 'TDO': 'output', 'D21': 'input', 'INIT_B': 'output', 'CS_B': 'input', 'D8': 'input', 'D9': 'input', 'D6': 'input', 'M1': 'input', 'D4': 'input', 'D5': 'input', 'D2': 'input', 'D3': 'input', 'D0': 'input', 'D1': 'input'}
cmd2pos = {'RDWR_B': (2, 0), 'D14': (15, 4), 'D16': (4, 2), 'TMS': (1, 4), 'D10': (14, 2), 'PROG_B': (2, 3), 'D12': (13, 2), 'D13': (13, 3), 'D15': (15, 5), 'D19': (3, 5), 'D30': (7, 0), 'D31': (7, 1), 'D17': (4, 3), 'M1': (2, 5), 'M0': (2, 7), 'M2': (1, 0), 'D28': (3, 0), 'D11': (14, 3), 'DOUT_BUSY': (1, 1), 'TCK': (1, 3), 'D29': (3, 1), 'PWRDWN_B': (2, 6), 'D21': (4, 1), 'D20': (4, 0), 'D23': (7, 7), 'D22': (7, 6), 'D25': (4, 5), 'D24': (4, 4), 'D27': (5, 3), 'D26': (5, 2), 'D7': (12, 3), 'D18': (3, 4), 'CCLK': (2, 1), 'D_IN': (1, 5), 'TDI': (1, 6), 'TDO': (1, 7), 'INIT_B': (2, 2), 'CS_B': (1, 2), 'D8': (14, 6), 'D9': (14, 7), 'D6': (12, 2), 'DONE': (2, 4), 'D4': (14, 4), 'D5': (14, 5), 'D2': (9, 6), 'D3': (9, 7), 'D0': (9, 4), 'D1': (9, 5)}
cmd2flag = {u'RDWR_B': {'default': 1, 'flag': 'T', 'value': [[300, 0]]},
            u'PWRDWN_B': {'default': 1, 'flag': u'const', 'value': 1},
            u'TDI': {'default': 0, 'flag': u'const', 'value': 0},
            u'TMS': {'default': 0, 'flag': u'const', 'value': 0},
            u'PROG_B': {'default': 1, 'flag': 'T', 'value': [[100, 0], [200, 1]]},
            u'M1': {'default': 0, 'flag': u'const', 'value': 0},
            u'M0': {'default': 1, 'flag': u'const', 'value': 1},
            u'M2': {'default': 0, 'flag': u'const', 'value': 0},
            u'CCLK': {'default': 0, 'flag': u'square', 'value': 2000000},
            u'D_IN': {'default': 0, 'flag': u'const', 'value': 0},
            u'TCK': {'default': 0, 'flag': u'const', 'value': 0},
            u'CS_B': {'default': 1, 'flag': 'T', 'value': [[350, 0]]}}
bs_start = 400
pos2data = {0: u'D0', 1: u'D1', 2: u'D2', 3: u'D3', 4: u'D4', 5: u'D5', 6: u'D6', 7: u'D7', 8: u'D8', 9: u'D9', 10: u'D10', 11: u'D11', 12: u'D12', 13: u'D13', 14: u'D14', 15: u'D15', 16: u'D16', 17: u'D17', 18: u'D18', 19: u'D19', 20: u'D20', 21: u'D21', 22: u'D22', 23: u'D23', 24: u'D24', 25: u'D25', 26: u'D26', 27: u'D27', 28: u'D28', 29: u'D29', 30: u'D30', 31: u'D31'}
nop = {'start': u'AFB', 'cycle': u'40T'}
sig2pio = {'pin_in': 'input', 'tri_inout': 'inout', 'in_tri_out': 'input', 'en_output': 'input', 'pin_out': 'output', 'data_in': 'input', 'data_out': 'output'}
entri_dict = {'en_output': 'tri_inout'}
sig2pos = {'pin_in': (15, 0), 'tri_inout': (16, 5), 'en_output': (15, 2), 'pin_out': (16, 7), 'data_in': (15, 3), 'data_out': (15, 1)}
