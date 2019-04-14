__author__ = 'biziuraa'

import asyncio
import socket
from config import Config
from structpu import *
from datagram2 import Datagram2

# from exception_decor import exception
#
# from exception_logger import logger


setting = Config.inst()
__all__ = ['main','Endpoint']

class DatagramEndpointProtocol(asyncio.DatagramProtocol):

    def __init__(self, endpoint, loop):
        self._endpoint = endpoint
        self.loop = loop

    def connection_made(self, transport):
        self._endpoint._transport = transport

    def datagram_received(self, data, addr):
        self._endpoint.add_datagram(data, addr)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        self.loop.stop()

    def error_received(self, exc):
        print('Error received:', exc)

class Endpoint:
    def __init__(self, queue_size=None):

        self.MCAST_GRP, self.MCAST_PORT, self.MCAST_HOST, _ = setting.version
        self.ADDRESS = (self.MCAST_HOST, self.MCAST_PORT)

        ttl = struct.pack('@i', 1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        self.sock.bind(self.ADDRESS)
        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        if queue_size is None:
            queue_size = 0
        self._queue = asyncio.Queue(queue_size)

        self._transport = None


    def add_datagram(self, data, addr):
        try:
            self._queue.put_nowait((data, addr))
        except asyncio.QueueFull:
            print('asyncio.QueueFull')

    def send(self, data):
        self._transport.sendto(data, (self.MCAST_GRP, self.MCAST_PORT))
        return data

    async def receive(self):

        data, addr = await self._queue.get()
        self._queue.task_done()
        return data, addr


Dgram2=Datagram2()

# @exception(logger)
async def recv(local,loop):
    task_channel_name = []
    while True:
        data, address = await local.receive()
        print('recived   {}'.format(data))

        channel_name=Dgram2.parsing_data(data)

        if channel_name:
            local.send(Dgram2.packed_TDatagram2[channel_name])
            if not channel_name in task_channel_name:
                task_channel_name.append(channel_name)
                loop.create_task(send(local,channel_name))

        # await asyncio.sleep(0.01)
# @exception(logger)
async def send(local,channel_name):
    while True:
        local.send(Dgram2.packed_TDatagram2[channel_name])
        await asyncio.sleep(1)

def main():
    endpoint = Endpoint()
    loop = asyncio.get_event_loop()
    connect = loop.create_datagram_endpoint(lambda: DatagramEndpointProtocol(endpoint,loop), sock=endpoint.sock)
    transport, protocol = loop.run_until_complete(connect)
    task = []
    loop.create_task(recv(endpoint, loop))
    loop.run_forever()
    transport.close()
    loop.close()



    # local = await open_datagram_endpoint()
    # print(local.address)
    # remote = await open_remote_endpoint(*local.address)

    # t.append(loop.create_task(send(remote,[b'asdasd\x00\x00\x00\x00\x00\x00'])))
    # name_channel.append(b'asdasd\x00\x00\x00\x00\x00\x00')
    # await asyncio.gather(*task)







