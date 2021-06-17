class ApplicationLayer(): 
    def __init__(self):
        super().__init__()

    def sender(self,mq):
        self.msg_string = "1111000011110000\0"
        print("[ Application layer : sender ] input bit string" , self.msg_string)
        mq.put((self.msg_string,1))

    def receiver(self,mq):
        data = mq.get()

        if data[0][0] == "010000010100001101001011":
            print("[ Application layer ] ACK Received")
        
        else: 
            print("[ Application layer : receiver ] Receiver received ")
            self.msg_string = "OK"
            mq.put((self.msg_string,1))