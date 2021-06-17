#!/usr/bin/env python3

#------------------------------------------------------------------------
# python3 simple_receiver.py
#------------------------------------------------------------------------

#공유메모리를 사용하기 위함
import sysv_ipc
import numpy as np
import os 
import struct

BUFF_SIZE = 16

TYPE_STRING = 1
TYPE_TWODOUBLES = 2
TYPE_NUMPY = 3

message_queue = sysv_ipc.MessageQueue(1234, sysv_ipc.IPC_CREAT)
running = True

while running:
    message, mtype = message_queue.receive()
    if message :
        running = True
    else:
        running = False
    # print(f"Raw message: {message}")
    if mtype == TYPE_STRING:
        str_message = message.decode()
        if str_message == "end":
            break
        print("*** New message received ***")
        print(f"string: {str_message}")
    elif mtype == TYPE_TWODOUBLES:
        two_doubles = struct.unpack("dd", message)
        print("*** New message received ***")
        print(f"two doubles: {two_doubles}")
    elif mtype == TYPE_NUMPY:
        print("*** New message received ***")
        numpy_message = np.frombuffer(message, dtype=np.int8)
        print(f"numpy: {numpy_message}")

    print()