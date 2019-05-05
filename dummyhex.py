#!/usr/bin/env python

addr = 0xce00

while True:
    print('{:04X}:00 00 00 00 00 00 00 00:00').format(addr)
    addr+=8
    if (addr % (8*16))==0:
        print('Sum :00 00 00 00 00 00 00 00:00')
    if addr > 0xcfff:
        break
