# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
# from server_udp import main
from server_udp import *
import sys

from datagram2 import Datagram2

if __name__ == "__main__":

    Dgram2 = Datagram2()
    path=''
    if len(sys.argv)>1 and sys.argv[1]:
        path = sys.argv[1]


    main(Dgram2,path)







