#!/usr/bin/env python3

import os
import sys
import re


def process_file(fileName):
    binarray = []
    with open(fileName) as f:
        while True:
            line = f.readline()
            if not line:
                break
            tokens = re.split('[ \n]', line)
            for b in tokens:
                if not b:
                    continue
                binarray.append(int(b, 16))
    with open(fileName.replace('.txt', '.bin'), 'bw') as wf:
        wf.write(bytearray(binarray))


if __name__ == '__main__':
    argv = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argv)  # 引数の個数
    if argc == 1:
        print("usage: " + argv[0] + " filename")
        sys.exit()

    process_file(argv[1])
