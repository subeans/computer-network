#!/usr/bin/env python3

#------------------------------------------------------------------------
# python3 simple_sender.py
#------------------------------------------------------------------------

import sysv_ipc
import numpy as np
import struct

BUFF_SIZE = 16

TYPE_STRING = 1
TYPE_TWODOUBLES = 2
TYPE_NUMPY = 3


if __name__ == '__main__':
    print("---SIMPLE SENDER---")
    msg_string = "computer network simple protocol\0"

    msg_double1 = 1234.56789
    msg_double2 = 9876.12345
    msg_npy = np.arange(BUFF_SIZE, dtype=np.uint8).reshape((2,BUFF_SIZE//2))

    try:
        message_queue = sysv_ipc.MessageQueue(1234, sysv_ipc.IPC_CREAT)

        # string transmission
        message_queue.send(msg_string, True, type=TYPE_STRING)
        print(f"string sent: {msg_string}")

        # Two double transmission
        bytearray1 = struct.pack("d", msg_double1)
        bytearray2 = struct.pack("d", msg_double2)
        message_queue.send(bytearray1 + bytearray2, True, type=TYPE_TWODOUBLES)
        print(f"two doubles sent: {msg_double1}, {msg_double2}")

        # numpy array transmission
        message_queue.send(msg_npy.tobytes(order='C'), True, type=TYPE_NUMPY)
        print(f"numpy array sent: {msg_npy}")

        message_queue.send("end", True, type=TYPE_STRING)

    except sysv_ipc.ExistentialError:
        print("ERROR: message queue creation failed")