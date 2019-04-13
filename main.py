# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
# from server_udp import main
from server_endpoint import *
from client import client1
import curio
import asyncio

if __name__ == "__main__":

    # srv=Serve()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main(loop))






