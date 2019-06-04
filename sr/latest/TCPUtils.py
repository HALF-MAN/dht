# encoding: utf-8

import socket


class TCPConnection:
    def __init__(self, address, timeOut):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeOut)
        self.socket.connect(address)

    def send_msg(self, msg):
        self.socket.send(msg)

    def close(self):
        if self.socket:
            self.socket.close()

    def recv(self):
        return self.socket.recv(4096)


def get_connection(address, timeout=50):
        return TCPConnection(address, timeout)



