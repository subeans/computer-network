import sys, socket, os, time, pickle, random

#------------------------------------------------------------------------
# python3 sr_receiver_20181614_박수빈.py 실행 후 

# python3 sr_sendor_20181614_박수빈.py 
#------------------------------------------------------------------------


#------------------------------------------------------------------------
#create internet UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(0)

host = "localhost"
port = 8080
#------------------------------------------------------------------------


# 교재 pdf 와 같은 setting
seqNumBits=3
windowSize = pow(2,seqNumBits-1)
numPackets = 11 
timeout=10000
segmentSize=50

# numPackets  = int(input("number of packets : "))
# seqNumBits  = int(input("send server the number of bits to use for sequence numbers : "))
# windowSize  = int(input("enter sender's window size : "))
# timeout = int(input("enter propogation time : "))
# segmentSize = int(input("enter segmentsize : "))


print("------------------SETTINGS--------------------")
print("Bits for sequence number: "+str(seqNumBits))
print("Number of packets: "+str(numPackets))
print("Sender Window Size: "+str(windowSize))
print("Timeout: "+str(timeout)+" microseconds")
print("Segment size is "+str(segmentSize)+" bytes")
print("-----------------------------------------------")

#언제든지 window 의 시작 위치를 표시하는 base
base = 0
# sequence 번호는 1번부터 시작하도록 설정
seqNum = 0
# 속한 패킷 번호 
pktNum = 0
window=[]

# print("<<<Starting Progam Timer>>>")
programtimer = time.time()

timer = time.time()
lostACK = False

def sendWindow(window):
    #segmentSize 크기의 임의의 문자열로 패킷 데이터 생성 
    data = os.urandom(segmentSize)

    for fullPacket in window:
        packet = pickle.loads(fullPacket)

        response = random.random()

        if(response > .8):
            response = "LOST_PACKET"

            packet=[packet[0]]
            packet.append(data)
            packet.append(response)

            s.sendto(pickle.dumps(packet), (host, port))
            print("Re-sending packet with sequence number: "+str(packet[0]))

        else:
            response = "CORRECT_PACKET"

            packet=[packet[0]]
            packet.append(data)
            packet.append(response)

            s.sendto(pickle.dumps(packet), (host, port))
            print("Re-sending packet with sequence number: "+str(packet[0]))

def randomResponse():
    response = random.random()
    if(response >= .8):
        response = "LOST_PACKET"
        return response
    else:
        response = "CORRECT_PACKET"
        return response

def sendUNACKED(window):
    for fullPacket in window:
        packet = pickle.loads(fullPacket)
        # print(packet[0])
        # print(packet[1])

        if(int(packet[1]) == 0) :
            packet[4] = randomResponse()
            newPacket = pickle.dumps(packet)
            s.sendto(newPacket,(host,port))
            print("Re-sending packet with sequence number: "+str(packet[0]))


def checkTimer(timenow, timebefore):
    if(timenow - timebefore > timeout/1000000):
        return True
    else:
        return False

print("SR")
if(windowSize > (2**(seqNumBits-1))):
    print("SR will not work. SR max sender window size is 2^(seqNumBits - 1).")
    sys.exit()

print("Starting timer")
while not ((pktNum > numPackets) and window):

    if(checkTimer(time.time(), timer)):
        print("Timer expired, resending UNACK'd packets!")
        sendUNACKED(window)
        #resetting timer
        timer = time.time()

        if(len(window) != 0):
            packet = pickle.loads(window[0])
            if(packet[1] == 1):
                del window[0]



    if(len(window) < windowSize):

        response = random.random()

        #create packet data as a random string (data) of size segmentSize
        data = os.urandom(segmentSize)

        seqNum += 1
        packet=[seqNum]
        packet.append(0)
        packet.append(data)
        packet.append(False)

        if(response > .8):
            response = "LOST_PACKET"

            packet.append(response)

            s.sendto(pickle.dumps(packet), (host, port))
            print("Sent packet with sequence number: "+str(seqNum))

            window.append(pickle.dumps(packet))

            continue

        else:
            response = "CORRECT_PACKET"

            packet.append(response)

            s.sendto(pickle.dumps(packet), (host, port))
            print("Sent packet with sequence number: "+str(seqNum))

            window.append(pickle.dumps(packet))

            continue


    try:
        ACK = s.recv(65536)

        receivedACK = []
        receivedACK = pickle.loads(ACK)
        recvACK = receivedACK[0]
        response = receivedACK[-1]

        wasACKLost = receivedACK[-2]

        if((receivedACK[0]) == 0):
            newReceivedACK = 2**(seqNumBits)
        else:
            newReceivedACK = receivedACK[0] - 1


        if(wasACKLost == "no"):
            pktNum += 1
            if(response == "CORRECT_PACKET"):
                print("ACK received: "+str(receivedACK[0])+" for packet "+str(recvACK))


                counter = 0
                for fullPacket in window:
                    counter += 1
                    packet = pickle.loads(fullPacket)
                    if(packet[0] == newReceivedACK):
                        packet[1] = 1
                        newPacket = pickle.dumps(packet)
                        # window[counter-1] = newPacket
                        window[counter]=newPacket
                        break
                    # counter+=1

                packet = pickle.loads(window[0])
                if(packet[0] == recvACK):
                    #slide window by 1:
                    print("sliding window")
                    #resetting timer
                    timer = time.time()

                    del window[0]
                    base += 1

                if(pktNum == numPackets):
                    break

            elif(response == "selectiveACK"):
                #set packets in window for received ACKS to be ACK'd
                counter = 0
                for fullPacket in window:
                    counter += 1
                    packet = pickle.loads(fullPacket)
                    if(packet[0] == newReceivedACK):
                        print("ACK received: "+str(receivedACK[0])+" for packet "+str(receivedACK[0]))

                        packet[1] = 1
                        newPacket = pickle.dumps(packet)
                        # window[counter-1] = newPacket
                        window[counter] = newPacket
                        #print(pickle.loads(newPacket))
                        break
                    # counter+=1

                packet = pickle.loads(window[0])

                if(packet[0] == recvACK):
                    print("ACK received: "+str(receivedACK[0])+" for packet "+str(receivedACK[0]))
                    print("sliding window")
                    del window[0]
                    numDelete = 0


                    for fullPacket in window:
                        packet = pickle.loads(fullPacket)
                        if(packet[1] == 1):
                            numDelete += 1
                        else:
                            break

                    while(numDelete > 0):
                        # print("sliding window index")
                        del window[0]
                        numDelete -= 1


            else:
                print("timeout ended")
        else:
            print("Lost ACK: "+str(receivedACK[0])+" for packet "+str(receivedACK[0]))

            counter = 0
            for fullPacket in window:
                counter += 1
                packet = pickle.loads(fullPacket)
                if(packet[0] == recvACK):
                    packet[3] = True

                newPacket = pickle.dumps(packet)
                window[counter-1] = newPacket


    except Exception:
        continue

finishTime = time.time() - programtimer
print(str(numPackets)+" total packets have been ACKed.")
print("Done sending packets, goodbye!")
print(" Time taken: "+str(finishTime))
sys.exit()

s.close()