#!/usr/bin/env python
import ctypes

class S7Exception:
    def __init__(self, msg, err):
        self._err = err
        self._msg = msg

    def __str__(self):
        return "%s (%d)" % (self._msg, self._err)

class S7Comm:
    def __init__(self, address):
        self._address = address
        self._s7obj = ctypes.CDLL("libs7comm.so.0.0")

        self._s7obj.s7comm_connect.restype = ctypes.c_void_p
        self._s7obj.err_to_string.restype = ctypes.c_char_p

        c_address = ctypes.create_string_buffer(address)
        tmp = self._s7obj.s7comm_connect(c_address)
        self._s7conn = ctypes.c_void_p(tmp)
        if not self._s7conn:
            raise S7Exception("Unable to connect", -1)

    def __del__(self):
        if self._s7conn:
            self._s7obj.s7comm_disconnect(self._s7conn)
        self._s7obj = None
        self._s7conn = None
        self._address = None

    def _err_to_string(self, err):
        return self._s7obj.err_to_string(err)

    def _readWord(self, db, num, value):
        ret = self._s7obj.s7comm_read_word(self._s7conn, db, num, ctypes.byref(value))

        if ret != 0:
            raise S7Exception(self._err_to_string(ret), ret)

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
            raise S7Exception(self._err_to_string(ret), ret)

    def writeUInt16(self, db, num, value):
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
            raise S7Exception(self._err_to_string(ret), ret)

    def writeInt8(self, db, num, value):
        self._writeByte(db, num, ctypes.c_int8(value))

    def writeUInt8(self, db, num, value):
        self._writeByte(db, num, ctypes.c_uint8(value))

    def readBit(self, db, byteNum, bitNum):
        value = ctypes.c_uint8()
        ret = self._s7obj.s7comm_read_bit(self._s7conn, db, (byteNum * 8) + bitNum, ctypes.byref(value))

        if ret != 0:
            raise S7Exception(self._err_to_string(ret), ret)

        if value.value != 0:
            return 1
        else:
            return 0

    def writeBit(self, db, byteNum, bitNum, value):
        val = ctypes.c_uint8()
        if value:
            val.value = 1
        else:
            val.value = 0
        ret = self._s7obj.s7comm_write_bit(self._s7conn, db, (byteNum * 8) + bitNum, val)

        if ret != 0:
            raise S7Exception(self._err_to_string(ret), ret)
