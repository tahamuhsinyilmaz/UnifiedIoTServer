import threading
import AMQPServer
import XMPPServer
import MQTTServer
import CoAPServer
import queue

def CoAPRun():
    print("CoAP")
    CoAPServer.main()
def AMQPRun():
    print("AMQP")
    AMQPServer.main()
def MQTTRun():
    print("MQTT")
    MQTTServer.main()
def XMPPRun():
    print("XMPP")
    XMPPServer.main()

coap = threading.Thread(target=CoAPRun,name="CoAP Thread",args=())
xmpp = threading.Thread(target=XMPPRun,name="XMPP Thread",args=())
mqtt = threading.Thread(target=MQTTRun,name="MQTT Thread",args=())
amqp = threading.Thread(target=AMQPRun,name="AMQP Thread",args=())

try:
    xmpp.start()
    mqtt.start()
    amqp.start()
    coap.start()
except KeyboardInterrupt:
    xmpp.exit()
    mqtt.exit()
    amqp.exit()
    coap.exit()
