class TransportLayer():
    def __init__(self,mq):
        self.str_message = self.get_from_application(mq)
    def get_from_application(self,mq):
        message = mq.get()
        return message

    def receiver(self,mq):  
        print("[ Transport layer ] stop and wait")
        mq.put((self.str_message,2))

    def sender(self,mq):
        print("[ Transport layer ] stop and wait")
        if self.str_message[0] =='OK':
            self.str_message = "ACK"
            print("[ Transport layer ]",self.str_message," to aschii")
            self.str_message = ''.join(format(ord(i), '08b') for i in 'ACK')
            print("[ Transport layer ] ACK to ",self.str_message)
            mq.put((self.str_message,2))
        else:
            print("[ Transport Layer ] stop and wait ")
            mq.put((self.str_message[0],2))
