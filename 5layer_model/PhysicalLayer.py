import socket,os
import warnings
warnings.filterwarnings("ignore")

class PhysicalLayer():
    def __init__(self,mq,host,port,case):
        self.case = case
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        if case==1:
            self.serversocket.bind((host, port))
            connected = False
            while not connected:
                self.serversocket.listen(1)
                self.clientsocket , address = self.serversocket.accept()
                print("[ Physical layer ] Receiver "+str(address)+" connected")    
                connected = True
        else:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.connect((host,port))

        
    def sender(self,mq):
        data = mq.get()

        if data[1]==4:
            print("[ Physical layer : sender ] received bit-stuffing from datalink layer ")
            mlt_bit = self.mlt(data[0]) 
            print("[ Physical layer ] Multi-transition MLT-3 scheme : ",mlt_bit)
            print("[ Physical layer ] send bit through socket")
            self.clientsocket.send(mlt_bit.encode())

    def receiver(self,mq):
        data = self.serversocket.recv(256).decode()
        print("[ Physical layer ] received bit-stuffing from sender  ",data)
        rev_mlt_bit = self.reverse_mlt(data)
        print("[ Physical layer ] reverse mlt-3 ",rev_mlt_bit)
        mq.put((rev_mlt_bit,5))

    def mlt(self,input_signal):
        output_signal = ''
        last_zero =''
        prev = str(input_signal[0])
        if prev == '0':
            output_signal +='0'
            prev = '0'
        else : 
            output_signal +='+'
            prev='+'
        for i in range(1,len(input_signal)):
            if input_signal[i]=='0':
        #         print('not_changed')
                output_signal +=prev 
            elif input_signal[i] =='1' and prev!='0':
        #         print('changed to zero')
                output_signal +='0'
                last_zero = prev
                prev = '0'
            elif input_signal[i]=='1' and prev =='0' :
        #         print('changed to pos or neg')
                if last_zero == '':
                    output_signal +='+'
                    prev='+'
                elif last_zero == '+':
                    output_signal += '-'
                    prev='-'
                elif last_zero=='-':
                    output_signal+='+'
                    prev='+'
        return output_signal

    def reverse_mlt(self,signal):
        prev = signal[0]
        if prev=='+':
            bit_stream = '1'
        else:
            bit_stream='0'
        for i in range(1,len(signal)):
            if prev != signal[i]:
                bit_stream+='1'
            else:
                bit_stream+='0'
            prev = signal[i]
        return bit_stream