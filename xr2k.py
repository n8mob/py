import socket

HOST = 'clearsky.dev'
PORT = 29438

def connect_send_receive(packets, host=HOST, port=PORT):
  if isinstance(packets, bytes):
    print('wrapping string in list')
    packets = [packets]
  with socket.create_connection((host, port)) as s:
    for packet in packets:
      while True:
          data = s.recv(4096)
          if not data:
            print('end of data')
            break
          print(data.decode(errors='ignore'), end="")
          s.sendall(packet + b'\n')
          
          
if __name__ == '__main__':
  connect_send_receive(b'\x00XR2K')
