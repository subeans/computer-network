class NetworkLayer():
    def __init__(self,mq):
        self.condition = 'bypass'
        
    def receiver(self,mq):                              
        data = mq.get()
        if data[1]==4:
            print("[ Networklayer : sender ] bypass from datalink layer to transport layer")
            mq.put((data[0],3))
    def sender(self,mq):
        data = mq.get()
        if data[1]==2:
            print("[ Networklayer : sender ] bypass from transport layer to datalink layer")
            mq.put((data[0],3))