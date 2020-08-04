import socket
class EndDevice:
    def __init__(self, hostname='', ip='', mac='', port=''):
        self.hostname = hostname
        self.ip = ip
        self.mac = mac
        self.port = port

    def get_hostname(self):
        try:
            self.hostname = socket.gethostbyaddr(self.ip)[0]
            print(f'We found the hostname associate with this IP {self.ip}')
        except :
            self.hostname = False
            print(f'We couldnt find the hostname associate with this IP {self.ip}')