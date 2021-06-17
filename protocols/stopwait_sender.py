import socket
from threading import *
import time
import random

#------------------------------------------------------------------------
# python3 stopwait_sender.py 실행 후 
# 다른 터미널에서 python3 stopwait_receiver.py 실행 

# sender 쪽 터미널 
# enter bit string : 010101
# enter propagation time : 10 
# enter peobability of message getting lost : 0.5 

# receiver 쪽 터미널 
# enter probability of acknowledgement not being sent : 0.5 

#------------------------------------------------------------------------
# 이미 실행되고 있다면 kill 
# ps -ef | grep python   
# kill third part number
#------------------------------------------------------------------------

#create socket object and bind it.
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000

serversocket.bind((host, port))

#------------------------------------------------------------------------

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()


    def run(self):
        while True:

            #take input from user 
            print("[ Transport Layer ] stop and wait ")
            bitstring  = str(input("enter bit string : "))
            propogationtime = float(input("enter propogation time : "))
            p_nosend = float(input("enter probability of message getting lost : "))
            
            #create a list of 1000 elements. (redundant, can be changed)
            l = []
            for i in range(0,1000):
                l = l +[i]

            #go through all the bits of the bitstring. 
            i = 0
            while i < len(bitstring):
                #for each bit, create a dictionary with the current 
                #window index (i%2 => 0,1,0,1...) and the bit itself
                datadict = {}
                datadict = {i%2 : bitstring[i], }
                
                #convert the dictionary to a string 
                sendstring = str(datadict)

                #find a random number between 0,1000 (both included)
                number= random.randint(0,1000)
                
                #store current time 
                time1 = time.time()
                
                
                #if statement is true with a probability of (1-p_nosend)
                if l[number] > (p_nosend*1000):

                    clientsocket.send(sendstring.encode())
                    time.sleep((propogationtime)/1.1)
                    time2 = time.time()
                    ackflag= False
                
                else: 
                    time.sleep(propogationtime/1.1)
                    time2 = time.time()
                    print ("package lost")
                    ackflag= False               


                while True:
                    #if the time elapsed is less that prop time, 
                    if time2-time1<= propogationtime:
                        #store current time     
                        time2= time.time()

                        #set timeout to listen for an acknowledgement. 
                        clientsocket.settimeout(propogationtime/1.1)

                        #raises exception when the timeout occurs. 
                        try:
                            #attempt to listen for ack. 
                            recieved = clientsocket.recv(1024)
                            print(recieved)
                            
                            if recieved:
                                print ("ACK received")
                                #window 철커덩
                                i = i+1
                                ackflag = True
                                break 

                        #timed out
                        except:
                            if time2 - time1 >propogationtime and ackflag == False:
                                print ("----TIMEOUT----")

                                number= random.randint(0,1000)

                                #package resent
                                if l[number] > (p_nosend*1000):
                                    clientsocket.send(sendstring.encode())
                                    time1 = time.time()
                                    time2 = time.time()
                                    print ("package resent")

                                #package dropped:    
                                else: 
                                    time1 = time.time()
                                    time2 = time.time()
                                    #time.sleep(propogationtime/1.1)
                                    print("package lost")


                        
                    
                     

serversocket.listen(5)
print ('Sender ready and is listening , please start receiver')
while (True):
    serversocket.listen(1)
    #to accept all incoming connections
    clientsocket, address = serversocket.accept()
    print("Receiver "+str(address)+" connected")
    #create a different thread for every 
    #incoming connection 
    client(clientsocket, address)