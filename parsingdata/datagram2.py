from structpu import StructPU
import numpy as np
from json_pars import Json_Pars


class Datagram2():
    def __init__(self):
        self.TDatagram2_SZ = 1024
        self.TDatagram2_HEADER_LN = 16

        self.Ttssrvcmd_Data_HEADER_LN = 16

        self.switch = {0: self.clear_Data_TDatagram2,
                       1: self.set_TS,
                       2: self.data_OFFSET,
                       'tssrv_setbits': self.set_TS, }

        self.structpu = StructPU()
        self.ts_array = {}
        self.packed_TDatagram2 = {}

    def clear_Data_TDatagram2(self, **kwargs):

        self.ts_array[kwargs['channel_name']] = np.zeros(kwargs['size_datagram2_data'], dtype=np.uint8)
        print(self.ts_array)
        return

    def set_bit(self, value, bit):
        return value | (1 << bit)

    def clear_bit(self, value, bit):
        return value & ~(1 << bit)

    def set_TS(self, **kwargs):
        ts_1000, nbit_1000 = divmod((kwargs['ts_number']), 1000)
        ts, nbit = divmod((nbit_1000 + 1), 8)
        ts = ts + 1
        ts_number = self.ts_array[kwargs['channel_name']][ts]
        if kwargs['ts_val']:
            self.ts_array[kwargs['channel_name']][ts] = self.set_bit(ts_number, nbit)
        else:
            self.ts_array[kwargs['channel_name']][ts] = self.clear_bit(ts_number, nbit)

        # bitarray = np.unpackbits(self.ts_array, axis=None)
        # bitarray[((x+1)*8)+(7-y)] = kwargs['ts_val']
        # self.ts_array = np.packbits(bitarray, axis=None)
        # print(self.ts_array)
        return

    def data_OFFSET(self, **kwargs):
        Head_Ttssrvcmd_Data2 = self.structpu.unpack_Ttssrvcmd_Data2(kwargs['TDatagram2'])
        print(Head_Ttssrvcmd_Data2)
        return

    def parsing_js(self, TDatagram2, js):
        json_pars = Json_Pars()
        commands = json_pars.main(TDatagram2)
        for com_generator in commands:
            print(com_generator.cmd)
            if not com_generator.channel_name in self.ts_array.keys():
                self.switch[0](size_datagram2_data=120,
                               channel_name=com_generator.channel_name)

            self.switch[com_generator.cmd](
                ts_number=int(com_generator.ts_number),
                ts_val=int(com_generator.ts_val),
                size_datagram2_data=120,
                channel_name=com_generator.channel_name)
            self.packed_TDatagram2[com_generator.channel_name] = self.structpu.pack_TDatagram2(
                ts_array=self.ts_array[com_generator.channel_name],
                size_datagram2_data=120,
                channel_name=com_generator.channel_name.encode('utf-8'))
            yield com_generator.channel_name

    def to_str(self, bytes_or_str):
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode('utf-8')
        else:
            value = bytes_or_str
        return value.rstrip('\x00')

    def parsing_data(self, TDatagram2, js):
        Head_TDatagram2 = self.structpu.unpack_TDatagram2(TDatagram2)
        if Head_TDatagram2.type == 54 and Head_TDatagram2.name[:5] == b'tssrv':
            Head_Ttssrvcmd_Data = self.structpu.unpack_Ttssrvcmd_Data(TDatagram2)
            Head_Ttssrvcmd_Data1 = self.structpu.unpack_Ttssrvcmd_Data1(TDatagram2)
            channel_name = self.to_str(Head_Ttssrvcmd_Data.channel_name)
            print(channel_name)
            if not channel_name in self.ts_array.keys():
                self.switch[0](size_datagram2_data=Head_Ttssrvcmd_Data.size_datagram2_data,
                               channel_name=channel_name)

            self.switch[Head_Ttssrvcmd_Data.cmd](TDatagram2=TDatagram2,
                                                 ts_number=Head_Ttssrvcmd_Data1.ts_number,
                                                 ts_val=Head_Ttssrvcmd_Data1.ts_val,
                                                 size_datagram2_data=Head_Ttssrvcmd_Data.size_datagram2_data,
                                                 channel_name=channel_name)

            self.packed_TDatagram2[channel_name] = self.structpu.pack_TDatagram2(ts_array=self.ts_array[channel_name],
                                                                                 size_datagram2_data=Head_Ttssrvcmd_Data.size_datagram2_data,
                                                                                 channel_name=Head_Ttssrvcmd_Data.channel_name)

            return channel_name
            # return Head_Ttssrvcmd_Data.channel_name.decode('utf-8').splite('\x00')[0]
        else:
            return None
