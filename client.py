
import pickle
import socket
import sys

client = socket.socket() 
host = socket.gethostname() 
port = 60001 

client.connect((host, port))

while True:
  d=pickle.dumps((sys.argv))
  client.sendall(d)

  payload = client.recv(4096)
  res = pickle.loads(payload)
  print(res)

