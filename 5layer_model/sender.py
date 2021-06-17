from multiprocessing import Process, Queue
import time , random
from ApplicationLayer import ApplicationLayer 
from TransportLayer import TransportLayer
from NetworkLayer import NetworkLayer
from DatalinkLayer import DatalinkLayer
from PhysicalLayer   import PhysicalLayer
import socket ,sys
import time
import warnings
warnings.filterwarnings("ignore")


mq = Queue()

if __name__ == '__main__':
    params = sys.argv
    if len(params)>1 :
        print("-------------------------------second senario-------------------")
        physical = PhysicalLayer(mq,'localhost',8080,2)
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

    else:
        application = ApplicationLayer()
        application_layer = Process (target= application.sender, args=(mq,))
        application_layer.start()

        trans_sender=TransportLayer(mq)
        transport_layer_sender = Process(target=trans_sender.sender, args=(mq,))
        transport_layer_sender.start()
        transport_layer_sender.join()

        network_sender=NetworkLayer(mq)
        network_layer_sender = Process(target=network_sender.sender, args=(mq,))
        network_layer_sender.start()
        network_layer_sender.join()

        datalink_sender = DatalinkLayer(mq)
        datalink_layer_sender = Process(target=datalink_sender.sender,args=(mq,))
        datalink_layer_sender.start()
        datalink_layer_sender.join()

        physical_sender = PhysicalLayer(mq,'localhost',8000,1)
        physical_layer_sender = Process(target=physical_sender.sender,args=(mq,))
        physical_layer_sender.start()
        physical_layer_sender.join()

    #-----------------------------------------------------

    
