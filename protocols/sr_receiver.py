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
windowSize = pow(2,seqNumBits-1)

print("Initializing SR")
print("------------------SETTINGS--------------------")
print("Sender Window Size: "+str(windowSize))
print("-----------------------------------------------")

while True:
    data, addr = s.recvfrom(65536)
    receivedPacket = pickle.loads(data)

    response = receivedPacket[-1]

    willACKLose = random.random()

    if(willACKLose <= .05):
        willACKLose = "lostACK"
    else:
        willACKLose = "no"


    ackNumber = int(receivedPacket[0])


    if(len(window) < windowSize):
 

        totalPackets += 1
        if(receivedPacket[0] == expectedSeqNum):
            if(response == "CORRECT_PACKET"):
                expectedSeqNum += 1
                # if(expectedSeqNum > maxSeqNum):
                #     expectedSeqNum = 1

                ackPacket = [ackNumber]
                ackPacket.append(totalPackets)
                ackPacket.append(1)
                ackPacket.append(willACKLose)
                ackPacket.append(response)

                window.append(pickle.dumps(ackPacket))
                try:
                    print("Received packet: "+str(receivedPacket[0]))
                    s.sendto(pickle.dumps(ackPacket), (addr[0], addr[1]))
                    print("Sending ACK: "+str(expectedSeqNum-1))
                except:
                    print("didnt send ack to client")

                print("sliding window")

                #slide window by deleting first entry in window
                del window[0]


           
            elif(response == "LOST_PACKET"):

                print("Packet "+str(receivedPacket[0])+" was lost on way to server")

                ackPacket = [ackNumber]
                ackPacket.append(totalPackets)
                ackPacket.append(0)
                ackPacket.append(willACKLose)
                ackPacket.append("dupACK")

                window.append(pickle.dumps(ackPacket))
            else:
                print("actual udp error occurred")

        else:

            if(receivedPacket[-2] == True):
                print("Received DUPLICATE packet: "+str(receivedPacket[0])+" meaning ACK was LOST")
                print("Re-sending ACK: "+str(ackNumber))

                ackPacket = [ackNumber]
                ackPacket.append(totalPackets)
                ackPacket.append(1)
                ackPacket.append(willACKLose)
                ackPacket.append("selectiveACK")

                s.sendto(pickle.dumps(ackPacket), (addr[0], addr[1]))
                continue

            else:

                alreadyInWindow = False
                for fullPacket in window:
                    packet = pickle.loads(fullPacket)
                    if(packet[0] == ackNumber):
                        alreadyInWindow = True


                if(response == "CORRECT_PACKET"):

                    print("Received packet: "+str(receivedPacket[0]))

                    print("Sending ACK: "+str(ackNumber))


                    ackPacket = [ackNumber]
                    ackPacket.append(totalPackets)
                    ackPacket.append(1)
                    ackPacket.append(willACKLose)
                    ackPacket.append("selectiveACK")


                    if(alreadyInWindow == False):
                        window.append(pickle.dumps(ackPacket))



                    s.sendto(pickle.dumps(ackPacket), (addr[0], addr[1]))
                
                elif(response == "LOST_PACKET"):

                    print("Packet "+str(receivedPacket[0])+" was lost on way to server")

                    ackPacket = [ackNumber]
                    ackPacket.append(totalPackets)
                    ackPacket.append(0)
                    ackPacket.append(willACKLose)
                    ackPacket.append("dupACK")

                    if(alreadyInWindow == False):
                        window.append(pickle.dumps(ackPacket))
                else:
                    print("actual udp error occurred")

    else:
        print("buffer is full, waiting on NACK'd packets in buffer")

        if(response == "CORRECT_PACKET"):
            numDelete = 0
            for fullPacket in window:
                packet = pickle.loads(fullPacket)

                if(packet[0] == ackNumber):

                    ackPacket = [ackNumber]
                    ackPacket.append(totalPackets)
                    ackPacket.append(1)
                    ackPacket.append(willACKLose)
                    ackPacket.append("selectiveACK")

                    print("Received packet: "+str(receivedPacket[0]))
                    print("Sending ACK: "+str(ackNumber))
                    s.sendto(pickle.dumps(ackPacket), (addr[0], addr[1]))

                if((packet[0] == ackNumber) or (packet[2] == 1)):
                    print("sliding window")
                    numDelete += 1

            while(numDelete > 0):
                del window[0]
                expectedSeqNum += 1
                # if(expectedSeqNum > maxSeqNum):
                #     expectedSeqNum = 1
                numDelete -= 1



        elif(response == "LOST_PACKET"):
            print("Packet "+str(receivedPacket[0])+" was lost on way to server")

        else:
            print("actual udp error occurred")

