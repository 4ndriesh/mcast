from structpu import StructPU
import numpy as np


class Datagram2():
    def __init__(self):
        self.TDatagram2_SZ = 1024
        self.TDatagram2_HEADER_LN = 16

        self.Ttssrvcmd_Data_HEADER_LN = 16

        self.switch = {0: self.clear_Data_TDatagram2,
                      1: self.set_TS,
                      2: self.data_OFFSET}

        self.structpu=StructPU()
        self.ts_array=np.array([])
        self.packed_TDatagram2=''

    def clear_Data_TDatagram2(self, **kwargs):
        self.ts_array=np.zeros(kwargs['size_datagram2_data'],dtype=np.uint8)
        print(self.ts_array)
        return

    def set_TS(self, **kwargs):

        bitarray = np.unpackbits(self.ts_array, axis=None)
        bitarray[kwargs['ts_number']] = kwargs['ts_val']
        self.ts_array = np.packbits(bitarray, axis=None)
        print(self.ts_array)
        return

    def data_OFFSET(self, **kwargs):
        Head_Ttssrvcmd_Data2 = self.structpu.unpack_Ttssrvcmd_Data2(kwargs['TDatagram2'])
        print(Head_Ttssrvcmd_Data2)
        return

    def parsing_data(self, TDatagram2):
        Head_TDatagram2=self.structpu.unpack_TDatagram2(TDatagram2)
        # print(Head_TDatagram2.name[])
        if Head_TDatagram2.type==54 and Head_TDatagram2.name[:5]==b'tssrv':
            Head_Ttssrvcmd_Data = self.structpu.unpack_Ttssrvcmd_Data(TDatagram2)
            Head_Ttssrvcmd_Data1 = self.structpu.unpack_Ttssrvcmd_Data1(TDatagram2)
            if not self.ts_array.size:
                self.switch[0](size_datagram2_data=Head_Ttssrvcmd_Data.size_datagram2_data)

            self.switch[Head_Ttssrvcmd_Data.cmd](TDatagram2=TDatagram2,
                                                 ts_number=Head_Ttssrvcmd_Data1.ts_number,
                                                 ts_val=Head_Ttssrvcmd_Data1.ts_val,
                                                 size_datagram2_data=Head_Ttssrvcmd_Data.size_datagram2_data)

            self.packed_TDatagram2= self.structpu.pack_TDatagram2(ts_array=self.ts_array,
                                                 size_datagram2_data=Head_Ttssrvcmd_Data.size_datagram2_data,
                                                 channel_name=Head_Ttssrvcmd_Data.channel_name)

            return Head_Ttssrvcmd_Data.channel_name
        else:
            return None