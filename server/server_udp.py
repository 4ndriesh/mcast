# -*- coding: utf-8 -*-
__author__ = 'biziuraa'
import curio
import socket
import struct
import asyncio
import numpy as np
from config import Config
from collections import namedtuple
TDatagram = namedtuple('TDatagram', 'type name cmd data')
setting = Config.inst()



class Server():
    def __init__(self):
        self.MCAST_GRP, self.MCAST_PORT, self.MCAST_HOST=setting.version
        ADDRESS=(self.MCAST_HOST,self.MCAST_PORT)

        ttl=struct.pack('@i',1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        self.sock.bind(ADDRESS)
        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.struct_fmt = ('H 12s H H')
        self.struct_len = struct.calcsize(self.struct_fmt)

        self.struct_unpack = struct.Struct(self.struct_fmt).unpack_from

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.udp_server(loop, self.sock))
        finally:
            loop.close()


    def print_text(self,dt):
        print(dt.type)

    def sendTDatagram(self, loop, sock, data, addr, fut=None, registed=False):
        fd = sock.fileno()
        if fut is None:
            fut = loop.create_future()
        if registed:
            loop.remove_writer(fd)
        if not data:
            return

        try:
            print('SendTo {0}{1}'.format(data, addr))
            n=0
            # n = sock.sendto(data, addr)
        except (BlockingIOError, InterruptedError):
            loop.add_writer(fd, self.sendTDatagram, loop, sock, data, addr, fut, True)
        else:
            fut.set_result(n)
        return fut


    def recvTDatagram(self, loop, sock, n_bytes, fut=None, registed=False):
        fd = sock.fileno()
        if fut is None:
            fut = loop.create_future()
        if registed:
            loop.remove_reader(fd)

        try:
            data, addr = sock.recvfrom(n_bytes)
        except (BlockingIOError, InterruptedError):
            loop.add_reader(fd, self.recvTDatagram, loop, sock, n_bytes, fut, True)
        else:
            fut.set_result((data, addr))
        return fut

        # while True:
        #     data,addr=self.sock.recvfrom(1024)
        #     TDatagram2 = TDatagram._make(self.struct_unpack(data))
        #     print(TDatagram2.type)
        #     print(TDatagram2.name)
            # self.print_text(np.packbits(TDatagram2.data, axis=-1))

    async def udp_server(self, loop, sock):
        while True:
            data, addr = await self.recvTDatagram(loop, sock, 1024)
            n_bytes = await self.sendTDatagram(loop, sock, data, addr)
