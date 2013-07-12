#!/usr/bin/env python
import ctypes

class S7Comm:
    def __init__(self, address):
        self._address = address
        self._s7obj = ctypes.CDLL("libs7comm.so")  

        c_address = ctypes.create_string_buffer("10.0.3.9")
        self._s7conn = self._s7obj.s7comm_connect(c_address)

    def readWord(self, db, num):
        value = ctypes.c_int()
        ret = self._s7obj.s7comm_read_word(self._s7conn, db, num, ctypes.byref(value));

        if ret != 0:
            raise "Aiii"

        return value.value
