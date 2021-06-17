import sys, os, socket, pickle, random, time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host ="localhost"
port =8080
s.bind((host, port))

window=[]

expectedSeqNum = 1
totalPackets = 0
seqNumBits = 3
maxSeqNum = (2**seqNumBits)

print("Initializing GBN receiver")
while True:
    data, addr = s.recvfrom(65536)
    receivedPacket = pickle.loads(data)

    response = receivedPacket[-1]
    # print(response)

    willACKLose = random.random()

    if(willACKLose <= .05):
        willACKLose = "lostACK"
    else:
        willACKLose = "NotLost"

    if(receivedPacket[0] == expectedSeqNum):
        if(response == "CORRECT_PACKET"):
            expectedSeqNum += 1
            totalPackets += 1

            # if(expectedSeqNum > maxSeqNum):
            #     expectedSeqNum = 1

            ackPacket = [expectedSeqNum]
            ackPacket.append(totalPackets)
            ackPacket.append(willACKLose)
            ackPacket.append(response)
            try:
                print("Received packet: "+str(receivedPacket[0]))
                s.sendto(pickle.dumps(ackPacket), (addr[0], addr[1]))
                print("Sending ACK: "+str(expectedSeqNum))
            except Exception:
                print("didnt send ack to client")

        elif(response == "LOST_PACKET"):
            print("Packet "+str(receivedPacket[0])+" was lost on way to server")

        else:
            print("actual udp error occurred")

    else:
        if(response == "CORRECT_PACKET"):
            print("Received packet: "+str(receivedPacket[0])+", OUT OF ORDER, discarding packet: "+str(receivedPacket[0]))
            print("Resending ACK: "+str(expectedSeqNum))

            ackPacket = [expectedSeqNum]
            ackPacket.append(totalPackets)
            ackPacket.append(willACKLose)
            ackPacket.append("dupACK")

            s.sendto(pickle.dumps(ackPacket), (addr[0], addr[1]))
    
        elif(response == "LOST_PACKET"):
            print("Packet "+str(receivedPacket[0])+" was lost on way to server")
        else:
            print("actual udp error occurred")


