#!/usr/bin/env python
import ctypes

class S7Comm:
    def __init__(self, address):
        self._address = address
        self._s7obj = ctypes.CDLL("libs7comm.so.0.1")

        c_address = ctypes.create_string_buffer(address)
        self._s7conn = self._s7obj.s7comm_connect(c_address)
        if not self._s7conn:
            raise "Unable to connect"

    def __del__(self):
        self._s7obj.s7comm_disconnect(self._s7conn)
        self._s7conn = None
        self._address = None

    def _readWord(self, db, num, value):
        ret = self._s7obj.s7comm_read_word(self._s7conn, db, num, ctypes.byref(value))

        if ret != 0:
            raise "Aiii"

    def readInt16(self, db, num):
        value = ctypes.c_int16()
        self._readWord(db, num, value)
        return value.value

    def readUInt16(self, db, num):
        value = ctypes.c_uint16()
        self._readWord(db, num, value)
        return value.value

    def _writeWord(self, db, num, value):
        ret = self._s7obj.s7comm_write_word(self._s7conn, db, num, value)

        if ret != 0:
            raise "Aiii"

    def writeUIn16(self, db, num, value):
        self._writeWord(db, num, value)

    def writeInt16(self, db, num, value):
        self._writeWord(db, num, value)

    def _readByte(self, db, num, value):
        ret = self._s7obj.s7comm_read_byte(self._s7conn, db, num, ctypes.byref(value))

        if ret != 0:
            raise "Aiii"

    def readInt8(self, db, num):
        value = ctypes.c_int8()
        self._readByte(db, num, value)
        return value.value

    def readUInt8(self, db, num):
        value = ctypes.c_uint8()
        self._readByte(db, num, value)
        return value.value

    def _writeByte(self, db, num, value):
        ret = self._s7obj.s7comm_write_byte(self._s7conn, db, num, value)

        if ret != 0:
            raise "Aiii"

    def writeInt8(self, db, num, value):
        self._writeByte(db, num, ctypes.c_int8(value))

    def writeUInt8(self, db, num, value):
        self._writeByte(db, num, ctypes.c_uint8(value))

    def readBit(self, db, num):
        value = ctypes.c_uint8()
        ret = self._s7obj.s7comm_read_bit(self._s7conn, db, num, ctypes.byref(value))

        if ret != 0:
            raise "Aiii"

        if value.value != 0:
            return 1
        else:
            return 0

    def writeBit(self, db, num, value):
        val = ctypes.c_uint8()
        if value:
            val.value = 1
        else:
            val.value = 0
        ret = self._s7obj.s7comm_write_bit(self._s7conn, db, num, val)

        if ret != 0:
            raise "Aiii"
