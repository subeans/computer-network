from multiprocessing import Process, Queue
import time , random
from ApplicationLayer import ApplicationLayer 
from TransportLayer import TransportLayer
from NetworkLayer import NetworkLayer
from DatalinkLayer import DatalinkLayer
from PhysicalLayer   import PhysicalLayer
import sys, socket, os, time
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    mq = Queue()

    physical = PhysicalLayer(mq,'localhost',8000,2)
    physical_layer_receiver = Process(target=physical.receiver,args=(mq,))
    physical_layer_receiver.start()
    physical_layer_receiver.join()

    datalink = DatalinkLayer(mq)
    datalink_layer_receiver = Process(target=datalink.receiver,args=(mq,))
    datalink_layer_receiver.start()
    datalink_layer_receiver.join()

    network =NetworkLayer(mq)
    network_layer_receiver = Process(target=network.receiver, args=(mq,))
    network_layer_receiver.start()
    network_layer_receiver.join()

    trans=TransportLayer(mq)
    transport_layer_receiver = Process(target=trans.receiver, args=(mq,))
    transport_layer_receiver.start()
    transport_layer_receiver.join()

    application = ApplicationLayer()
    application_layer = Process (target= application.receiver, args=(mq,))
    application_layer.start()
    application_layer.join()

    #--------------------------------------- senario 2
    print("------------------------------second senario-----------------------------------")
    trans=TransportLayer(mq)
    transport_layer_receiver = Process(target=trans.sender, args=(mq,))
    transport_layer_receiver.start()
    transport_layer_receiver.join()

    network =NetworkLayer(mq)
    network_layer_receiver = Process(target=network.sender, args=(mq,))
    network_layer_receiver.start()
    network_layer_receiver.join()

    datalink = DatalinkLayer(mq)
    datalink_layer_receiver = Process(target=datalink.sender,args=(mq,))
    datalink_layer_receiver.start()
    datalink_layer_receiver.join()
  
    physical = PhysicalLayer(mq,'localhost',8080,1)
    physical_layer_receiver = Process(target=physical.sender,args=(mq,))
    physical_layer_receiver.start()
    physical_layer_receiver.join()

    

    
    
   

   

    
