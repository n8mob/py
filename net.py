import socket
import psutil


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


if __name__ == '__main__':
    print(f'ip address: {get_ip_address()}')
    
