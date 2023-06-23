import socket
import subprocess


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


def run_ipconfig():
    return subprocess.check_output(['ipconfig', 'getiflist']).split()


if __name__ == '__main__':
    print(f'ip address: {get_ip_address()}')
    print(run_ipconfig())
    
