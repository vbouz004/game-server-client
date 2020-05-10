import socket
import pickle


package_size = 2048


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.254.11"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            #pickle.loads(self.client.recv(package_size))
            return self.client.recv(package_size).decode()
        except:
            pass

    def send(self, data):
        try:
            #self.client.send(pickle.dumps(data))
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(package_size))
        except socket.error as e:
            print(e)
