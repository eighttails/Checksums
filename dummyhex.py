#!/usr/bin/env python3

start_addr = 0xce00
end_addr = 0xcfff
addr = start_addr
while True:
    print('{:04X}:00 00 00 00 00 00 00 00:00').format(addr)
    addr+=8
    if (addr % (8*16))==0:
        print('Sum :00 00 00 00 00 00 00 00:00')
    if addr > end_addr:
        break
