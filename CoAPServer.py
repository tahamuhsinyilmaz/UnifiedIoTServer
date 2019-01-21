from coapthon.server.coap import CoAP
from coapthon import defines
from Resources import BasicResource
from coapthon.serializer import Serializer
from coapthon.messages.message import Message
from coapthon.messages.request import Request
from coapthon.messages.response import Response
import threading
import datetime
from database import database

class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        self.add_resource('basic/', BasicResource())
        # self.add_resource('json/', JSONResource())
        # self.add_resource('storage/', Storage())
        # self.add_resource('separate/', Separate())
        # self.add_resource('long/', Long())
        # self.add_resource('big/', Big())
        # self.add_resource('void/', voidResource())
        # self.add_resource('xml/', XMLResource())
        # self.add_resource('encoding/', MultipleEncodingResource())
        # self.add_resource('etag/', ETAGResource())
        # self.add_resource('child/', Child())
        # self.add_resource('advanced/', AdvancedResource())
        # self.add_resource('advancedSeparate/', AdvancedResourceSeparate())

        print(("CoAP Server start on " + host + ":" + str(port)))
        print((self.root.dump()))


def main():  # pragma: no cover
    ip = "192.168.1.21"
    port = defines.COAP_DEFAULT_PORT
    multicast = False
    server = CoAPServer(ip, port, multicast)
    server.notify('/basic')
    try:
        # server.listen()
        while not server.stopped.isSet():
            data, client_address = server._socket.recvfrom(4096)
            try:
                serializer = Serializer()
                message = serializer.deserialize(data, client_address)
                if isinstance(message, int):
                    print("receive_datagram - BAD REQUEST")

                    rst = Message()
                    rst.destination = client_address
                    rst.type = defines.Types["RST"]
                    rst.code = message
                    rst.mid = server._messageLayer.fetch_mid()
                    server.send_datagram(rst)
                    continue

                # print("receive_datagram " + str(message.payload))
                database().insert_value('CoAP', datetime.datetime.now(), str(message.payload))

                if isinstance(message, Request):
                    transaction = server._messageLayer.receive_request(message)
                    if transaction.request.duplicated and transaction.completed:
                        print("message duplicated, transaction completed")
                        if transaction.response is not None:
                            server.send_datagram(transaction.response)
                        continue
                    elif transaction.request.duplicated and not transaction.completed:
                        print("message duplicated, transaction NOT completed")
                        server._send_ack(transaction)
                        continue
                    args = (transaction, )
                    t = threading.Thread(target=server.receive_request, args=args)
                    t.start()
                # self.receive_datagram(data, client_address)
                elif isinstance(message, Response):
                    print("Received response from %s", message.source)

                else:  # is Message
                    transaction = server._messageLayer.receive_empty(message)
                    if transaction is not None:
                        with transaction:
                            server._blockLayer.receive_empty(message, transaction)
                            server._observeLayer.receive_empty(message, transaction)

            except RuntimeError:
                print("Exception with Executor")
        server._socket.close()
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")
