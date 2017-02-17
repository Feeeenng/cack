# -*- coding: utf8 -*-
from __future__ import unicode_literals
import struct


def type_list():
    return {
        'FFD8FF': '.jpg',
        '47494638': '.gif',
        '89504E47': '.png',
        '255044': '.ai',
        '384250': '.psd',
        'C5D0D3': '.eps',
        '504B03': '.xlsx'
    }


# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u''
    for i in range(num):
        t = u'%x' % bytes[i]
        if len(t) % 2:
            hexstr += u'0'
        hexstr += t
    return hexstr.upper()


# 获取文件类型
def file_type(f):
    tl = type_list()
    ftype = 'unknown'
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2  # 需要读多少字节
        f.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from('B' * numOfBytes, f.read(numOfBytes))  # 一个 'B'表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    return ftype

