# -*- coding: utf-8 -*-
__author__ = 'biziuraa'

import struct
from collections import namedtuple
import numpy as np
from config import Config
setting = Config.inst()

class StructPU():
    def __init__(self):


        self.TDatagram2 = namedtuple('TDatagram2', 'size, type, name')
        self.Ttssrvcmd_Data = namedtuple('TTSSRVCMD_DATA', 'channel_type, channel_name, size_datagram2_data, cmd')
        self.Ttssrvcmd_Data1 = namedtuple('TTSSRVCMD_DATA1', 'ts_number, ts_val')
        self.Ttssrvcmd_Data2 = namedtuple('TTSSRVCMD_DATA2', 'data_offset, data_sz')

        self.struct_fmt_TDatagram2 = 'H H 12s'
        self.struct_len_TDatagram2 = struct.calcsize(self.struct_fmt_TDatagram2)
        self.struct_unpack_TDatagram2 = struct.Struct(self.struct_fmt_TDatagram2).unpack_from

        self.struct_fmt_Ttssrvcmd_Data = 'B 12s B B'
        self.struct_len_Ttssrvcmd_Data = struct.calcsize(self.struct_fmt_Ttssrvcmd_Data)
        self.struct_unpack_Ttssrvcmd_Data = struct.Struct(self.struct_fmt_Ttssrvcmd_Data).unpack_from

        self.struct_fmt_Ttssrvcmd_Data1 = 'H H'
        self.struct_len_Ttssrvcmd_Data1 = struct.calcsize(self.struct_fmt_Ttssrvcmd_Data1)
        self.struct_unpack_Ttssrvcmd_Data1 = struct.Struct(self.struct_fmt_Ttssrvcmd_Data1).unpack_from

        self.struct_fmt_Ttssrvcmd_Data2 = 'H H'
        self.struct_len_Ttssrvcmd_Data2 = struct.calcsize(self.struct_fmt_Ttssrvcmd_Data2)
        self.struct_unpack_Ttssrvcmd_Data2 = struct.Struct(self.struct_fmt_Ttssrvcmd_Data2).unpack_from



        self.struct_unpack=None


    def unpack_TDatagram2(self, TDatagram2):
        Head_TDatagram2 = self.TDatagram2._make(self.struct_unpack_TDatagram2(TDatagram2[:self.struct_len_TDatagram2]))
        return Head_TDatagram2

    def unpack_Ttssrvcmd_Data(self, TDatagram2):
        Head_TDatagram2 = self.Ttssrvcmd_Data._make(self.struct_unpack_Ttssrvcmd_Data(TDatagram2[self.struct_len_TDatagram2:]))
        return Head_TDatagram2

    def unpack_Ttssrvcmd_Data1(self, TDatagram2):
        size_Data=self.struct_len_TDatagram2+self.struct_len_Ttssrvcmd_Data
        Head_Ttssrvcmd_Data1 = self.Ttssrvcmd_Data1._make(self.struct_unpack_Ttssrvcmd_Data1(TDatagram2[size_Data:]))
        return Head_Ttssrvcmd_Data1

    def unpack_Ttssrvcmd_Data2(self, TDatagram2):
        size_Data = self.struct_len_TDatagram2 + self.struct_len_Ttssrvcmd_Data+self.struct_len_Ttssrvcmd_Data1
        Ttssrvcmd_Data2 = self.Ttssrvcmd_Data2._make(self.struct_unpack_Ttssrvcmd_Data2(TDatagram2[size_Data:]))
        return Ttssrvcmd_Data2

    def pack_TDatagram2(self, **kwargs):
        struct_fmt_Ttssrvcmd_Data2 = 'H H 12s {}B'
        struct_pack_Data_TDatagram2 = struct.Struct(struct_fmt_Ttssrvcmd_Data2.format(kwargs['size_datagram2_data'])).pack
        TDatagram2 = struct_pack_Data_TDatagram2(kwargs['size_datagram2_data'],1, kwargs['channel_name'], *kwargs['ts_array'])
        print(TDatagram2)
        return TDatagram2

    # @property
    # def data(self):
    #     return
    # @data.setter
    # def data(self, value):
    #     pass

