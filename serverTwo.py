
import os
import pickle
import socket
import time
import pandas as pd

port = 60024  
s = socket.socket()  
host = socket.gethostname()  # local machine name
s.bind((host, port)) 
s.listen(5) 


dataframe = pd.DataFrame() 

print('Status Server Two now Running') 

while True:
  conn, addr = s.accept()  
  print('Got connection from', addr)

  currDir = os.getcwd() 
  servBdir = "folderTwo"

  listOfFiles = os.listdir(os.path.join(currDir, servBdir))  
  # folderTwo

  for file in listOfFiles: 
    status = os.stat(os.path.join(currDir, servBdir, file))  
    dataframe = dataframe.append({"File name": file, "size(kb)": float(status.st_size) / 1000,
                                  "Modified date": time.ctime(status.st_mtime)},
                                 ignore_index=True)  

  data = pickle.dumps(dataframe)  
  print(pickle.loads(data))  
  conn.sendall(data) 
  dataframe.drop(dataframe.index, inplace=True)
  del data
  print('Done sending files information from server B to server A')
