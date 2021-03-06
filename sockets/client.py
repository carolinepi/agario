import socket
import _pickle as pickle

from conts import PORT, HOST


class ClientSocket:
    __slots__ = ('client', 'address')

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (HOST, PORT)

    def connect(self, name: str) -> int:
        self.client.connect(self.address)
        self.client.send(str.encode(name))
        val = self.client.recv(8)
        return int(val.decode())

    def disconnect(self):
        self.client.close()

    def send(self, data: str, pick: bool = False) -> str:
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
            reply = self.client.recv(2048 * 4)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)

            return reply
        except socket.error as e:
            print(e)
