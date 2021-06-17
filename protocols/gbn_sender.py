import sys, socket, os, time, pickle, random,math
from threading import *

#------------------------------------------------------------------------
# python3 gbn_receiver.py 실행 후
# python3 gbn_sender.py 실행 
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
windowSize = pow(2,seqNumBits)-1
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

print("<<<Starting Progam Timer>>>")
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

        if(int(packet[1]) == 0):
            packet[4] = randomResponse()
            newPacket = pickle.dumps(packet)
            s.send(newPacket)
            print("Re-sending packet with sequence number: "+str(packet[0]))


def checkTimer(timenow, timebefore):
    if(timenow - timebefore > timeout/1000000):
        return True
    else:
        return False


print("Initializing GBN")
if(windowSize > ((2**seqNumBits)-1)):
    print("GBN will not work. GBN max sender window size is 2^seqNumBits - 1.")
    sys.exit()

# print("Starting timer")
while not ((pktNum >= numPackets) and window):

    if(checkTimer(time.time(), timer)):
        print("Timer expired, resending window!")
        sendWindow(window)
        #resetting timer
        timer = time.time()

    # window 내의 packet 만 전송 
    if(len(window) < (windowSize)):

        response = random.random()

        #데이터 생성 
        data = os.urandom(segmentSize)

        seqNum += 1
        # if(seqNum > 2**seqNumBits):
        #     seqNum = 1

        packet=[seqNum]
        packet.append(data)

        if(response > .8):
            response = "LOST_PACKET"

            packet.append(response)

            s.sendto(pickle.dumps(packet),(host,port))
            print("Sent packet with sequence number: "+str(seqNum))

            window.append(pickle.dumps(packet))

            continue

        else:
            response = "CORRECT_PACKET"

            packet.append(response)
            pck = pickle.dumps(packet)
            s.sendto(pck,(host,port))
            print("Sent packet with sequence number: "+str(seqNum))

            window.append(pck)

            continue

    try:
        ACK = s.recv(65536)

        receivedACK = []
        receivedACK = pickle.loads(ACK)
        recvACK = receivedACK[0]
        response = receivedACK[-1]

        wasACKLost = receivedACK[-2]

        if(wasACKLost == "NotLost"):
            if(response == "CORRECT_PACKET"):
                # print("received check")
                while(int(receivedACK[1]) > (base) and window):
                    print("Received ACK for next: "+str(receivedACK[0]))
                    #resetting timer
                    timer = time.time()
                    
                    # 철커덩 
                    del window[0]
                    base += 1

                    #packet number sent increases by 1
                    pktNum += 1
                    # print("Received ACK for send packet "+str(pktNum) )
                    print("sliding_window")


            elif(response == "dupACK"):
                packet = pickle.loads(window[0])
                print("Duplicate ACK received: "+str(packet[0])+", discarding ACK")

            else:
                print("timeout ended")
        else:
            print("Lost ACK for: "+str(receivedACK[0]))

    except Exception:
        continue

finishTime = time.time() - programtimer
print(str(numPackets)+" packets have been ACKed.")
print("Done sending packets, goodbye!" )
print("Time taken: "+str(finishTime))
sys.exit()

s.close()