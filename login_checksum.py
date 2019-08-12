#!/usr/bin/env python3
'''
LOGiN関連のダンプリスト用チェックサム
8バイトごとにチェックサム、32行ごとにブロックチェックサム(縦サムはなし)
チェックサムは単純サムに加え、アドレスの上位バイトと下位バイトを加算する
'''

import sys
import re

vert_sums = [0 for i in range(8)]
processing_addr = -1
some_error_in_block = False
sum_block = 0


def process_line(tokens, line_num):
    # 通常のデータ行
    global vert_sums, processing_addr, some_error_in_block, sum_block
    addr = int(tokens[0], 16)
    if processing_addr != -1 and addr != processing_addr + 8:
        print ('Address not in order in line ' + str(line_num))
        processing_addr += 8
        some_error_in_block = True
    processing_addr = addr

    try:
        sum = int(tokens[9], 16)
    except ValueError:
        print ('Sum parse error in line ' + str(line_num))
        some_error_in_block = True
        return

    sum_work = 0
    for i in range(1, 9):
        try:
            val = int(tokens[i], 16)
        except ValueError:
            print ('Value parse error in line ' + str(line_num))
            some_error_in_block = True
            return
        # チェックサムに加算
        sum_work += val
        sum_block += val
        vert_sums[i-1] += val

    # アドレスの上位バイト、下位バイトを加算
    sum_work += addr // 256
    sum_work += addr % 256

    if sum != sum_work % 256:
        print ('Checksum error in line ' + str(line_num))
        some_error_in_block = True
        return


def process_sum_line(tokens, line_num):
    # チェックサム行
    global vert_sums, some_error_in_block
    try:
        try:
            sum = int(tokens[10], 16)
        except ValueError:
            print ('Sum parse error in line ' + str(line_num))
            raise Exception

        # データ本体は通常行と同様に処理
        process_line(tokens, line_num)

        if sum != sum_block % 256:
            print ('Block checksum error in line ' + str(line_num))
            raise Exception
    except:
        pass

    some_error_in_block = False
    vert_sums = [0 for i in range(8)]
    sum_block = 0


def process_file(fileName):
    line_num = 1  # 行番号
    with open(fileName) as f:
        while True:
            line = f.readline()
            if not line:
                break
            tokens = re.split('[: \n]', line)
            if len(tokens) == 12:
                # チェックサム行
                process_sum_line(tokens, line_num)
            else:
                try:
                    # 通常のデータ行
                    addr = int(tokens[0], 16)
                except ValueError:
                    print ('Address parse error in line ' + str(line_num))
                if addr >= 0 and addr <= 0xFFFF and len(tokens) == 11:
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

    vert_sums = [0 for i in range(8)]
    processing_addr = -1
    some_error_in_block = False

    process_file(argv[1])
