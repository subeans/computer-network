import random
import math
import time

class DatalinkLayer():
    def __init__(self,mq):
        self.data = mq.get()
        self.input_data = ''


    def receiver(self,mq):                              
        if self.data[1] == 5 :
            self.input_data = self.data[0]
            unstuffed_data = self.bit_unstuffing(self.input_data)
            print("[ Datalink layer : sender ] unstuffed data ",unstuffed_data)
            mq.put((unstuffed_data,4))


    def sender(self,mq):
        if self.data[1]==3:
            self.input_data = self.data[0]
            # print("stuff before : ",self.input_data)
            stuffed_data = self.bit_stuffing(self.input_data)
            # print("stuff after : ",stuffed_data)
            print("[ Datalink layer : sender ] stuffed data ",stuffed_data)
            mq.put((stuffed_data,4))
        
        self.csma_cd()

    def bit_stuffing(self,input_data):
        stuff_cnt = 0
        stuffed=''
        for i in range(len(str(input_data))):
            if input_data[i]=="1" :
                stuff_cnt+=1
                if stuff_cnt == 5 :
                    stuffed+=str(input_data[i] )
                    stuffed += '0'
                    stuff_cnt = 0
                elif stuff_cnt!=5:
                    stuffed+=str(input_data[i])
            else:
                stuff_cnt = 0 
                stuffed+=str(input_data[i])
        return stuffed

    def bit_unstuffing(self,unstuffing_input):
        unstuff_cnt = 0
        unstuffed=''
        for i in range(len(unstuffing_input)):
            if unstuffing_input[i]=="1" :
                unstuff_cnt+=1
                unstuffed+=unstuffing_input[i]
            else:
                if unstuff_cnt == 5:
                    unstuff_cnt=0
                    continue
                else:
                    unstuff_cnt = 0 
                    unstuffed+=unstuffing_input[i]
        return unstuffed



    def exponential_backoff_time(self,k):
        rand_num = random.random() * (pow(2, k) - 1)
        return rand_num  

    def non_persistent(self,wait_time):
        print("Wait backoff time ",wait_time)
        print()
        time.sleep(wait_time)

    def random_backoff(self,k,k_max):
        Tp = random.randrange(1,10)
        k += 1
        #random back off
        if k > k_max:
            k=0 # abort 
            print("Abort")
            return 0
            # Add the exponential backoff time to waiting time
        backoff_time = Tp * self.exponential_backoff_time(k)
        return backoff_time

    def csma_cd(self):
        k = 0
        k_max = 15
        trial = 1
        cont=True
        while cont :
            is_persistent = random.randrange(0,2)
            print("[ DataLink layer ] CSMA : Apply one of the persistence method")
            if is_persistent :
                print("<<<1-persistent method applied>>>")
                idle = random.randrange(0,2)
                if idle:
                    print("IDLE ")
                    collision = random.randrange(0,2)
                    if collision :
                        print("Collision detected : jamming signal")
                        print()
                        trial +=1
                    else:
                        print("SUCCESS")
                        print("transmission done in {} trial".format(trial))
                        cont=False
            else:
                print("<<<non-persistent method applied>>>")
                idle = random.randrange(0,2)
                if idle:
                    print("IDLE")
                    collision = random.randrange(0,2)
                    if collision :
                        print("Collision detected : jamming signal ")
                        wait_time = self.random_backoff(k,k_max)
                        self.non_persistent(wait_time)
                        print()
                        trial +=1
                    else:
                        print("SUCCESS")
                        print("transmission done in {} trial".format(trial) )
                        cont=False
