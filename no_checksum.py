#!/usr/bin/env python3
'''
チェックサムがない単純なダンプリスト
'''

import sys
import re

YOKO = 8
processing_addr = -1

def process_line(tokens, line_num):
    # 通常のデータ行
    global processing_addr
    addr = int(tokens[0], 16)
    if processing_addr != -1 and addr != processing_addr + YOKO:
        print ('Address not in order in line ' + str(line_num))
        processing_addr += YOKO
    processing_addr = addr

    for i in range(1, YOKO+1):
        try:
            val = int(tokens[i], 16)
            if val < 0 or val > 255:
                raise ValueError
        except ValueError:
            print ('Value parse error in line ' + str(line_num))
            return




def process_file(fileName):
    line_num = 1  # 行番号
    with open(fileName) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.replace('\n', '')
            tokens = re.split('[: ]+', line)
            # print(tokens)
            try:
                # 通常のデータ行
                addr = int(tokens[0], 16)
            except ValueError:
                print ('Address parse error in line ' + str(line_num))
            if addr >= 0 and addr <= 0xFFFF and len(tokens) == YOKO+1:
                process_line(tokens, line_num)
            else:
                # チェックサム、データ行どちらにも該当しない場合はエラー
                print ('Parse error in line ' + str(line_num))
            line_num += 1


if __name__ == '__main__':
    argv = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argv)  # 引数の個数
    if argc == 1:
        print("usage: " + argv[0] + " filename")
        sys.exit()

    vert_sums = [0 for i in range(YOKO)]
    processing_addr = -1
    some_error_in_block = False

    process_file(argv[1])
