# -*- coding: utf-8 -*-
__author__ = 'biziuraa'
import curio
import socket
import struct
import asyncio
import time
import numpy as np
from config import Config
from structpu import StructPU

setting = Config.inst()
structpu= StructPU()


import asyncio



MCAST_GRP, MCAST_PORT,MCAST_HOST, _ = setting.version
ADDRESS = (MCAST_HOST, MCAST_PORT)

ttl = struct.pack('@i', 1)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

sock.bind(ADDRESS)
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

class EchoClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, message, loop):



        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        # self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))

        # print("Close the socket")
        # self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

def main():

    loop = asyncio.get_event_loop()
    message = "Hello World!"
    connect = loop.create_datagram_endpoint(lambda: EchoClientProtocol(message, loop),sock=sock)
    transport, protocol = loop.run_until_complete(connect)
    loop.run_forever()
    transport.close()
    loop.close()



# import asyncio
#
# class Server:
#     def __init__(self):
#
#         self.MCAST_GRP, self.MCAST_PORT, self.MCAST_HOST,_=setting.version
#         ADDRESS=(self.MCAST_HOST,self.MCAST_PORT)
#
#         ttl=struct.pack('@i',1)
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#         self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
#
#         self.sock.bind(ADDRESS)
#         mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
#
#         self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#
#     def connection_made(self, transport):
#         self.transport = transport
#
#     def datagram_received(self, data, addr):
#         message = data.decode()
#         print('Received %r from %s' % (message, addr))
#         print('Send %r to %s' % (message, addr))
#         self.transport.sendto(data, addr)
#
# def main():
#     srv=Server()
#     loop = asyncio.get_event_loop()
#     print("Starting UDP server")
#     # One protocol instance will be created to serve all client requests
#
#     listen = loop.create_datagram_endpoint(Server, sock=srv.sock)
#     transport, protocol = loop.run_until_complete(listen)
#
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#
#     transport.close()
#     loop.close()


#
# class Server():
#     def __init__(self):
#         self.MCAST_GRP, self.MCAST_PORT, self.MCAST_HOST,_=setting.version
#         ADDRESS=(self.MCAST_HOST,self.MCAST_PORT)
#
#         ttl=struct.pack('@i',1)
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#         self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
#
#         self.sock.bind(ADDRESS)
#         mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
#
#         self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#         loop = asyncio.get_event_loop()
#         try:
#             loop.run_until_complete(self.udp_server(loop, self.sock))
#         finally:
#             loop.close()
#
#
#     def sendTDatagram(self, loop, sock, data, addr, fut=None, registed=False):
#         fd = sock.fileno()
#         if fut is None: fut = loop.create_future()
#         if registed: loop.remove_writer(fd)
#         if not data:
#             return
#
#         try:
#             print('SendTo {0}{1}'.format(data, addr))
#             n=None
#             # n = sock.sendall(data)
#         except (BlockingIOError, InterruptedError):
#             loop.add_writer(fd, self.sendTDatagram, loop, sock, data, addr, fut, True)
#         else:
#             fut.set_result(n)
#         return fut
#
#
#     def recvTDatagram(self, loop, sock, n_bytes, fut=None, registed=False):
#         fd = sock.fileno()
#         if fut is None: fut = loop.create_future()
#         if registed: loop.remove_reader(fd)
#
#         try:
#             data, addr = sock.recvfrom(n_bytes)
#         except (BlockingIOError, InterruptedError):
#             loop.add_reader(fd, self.recvTDatagram, loop, sock, n_bytes, fut, True)
#         else:
#             fut.set_result((data, addr))
#         return fut
#
#     async def udp_server(self, loop, sock):
#         while True:
#             data, addr = await self.recvTDatagram(loop, sock, 1024)
#             print(structpu.struct_unpack(data))
#             n_bytes = await self.sendTDatagram(loop, sock, data, addr)
#             # print(n_bytes)
