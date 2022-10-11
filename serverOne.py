import filecmp
import os
import pickle
import socket
import time
import dirsync
import filelock
import pandas as pd

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

port = 60001  
server_a = socket.socket()  
host = socket.gethostname()  
server_a.bind((host, port))  
server_a.listen(5) 
send_files_to_client = False
print('Status Server Two now Running')  
file_list_with_operations = []  


def dirSync():
  path = os.getcwd() + '/folderOne/'
  copyto = os.getcwd() + '/folderTwo/'

  if len(file_name_list) > 0:
    dirsync.sync(copyto, path, 'sync', ignore=file_name_list)  
  else:
    dirsync.sync(copyto, path, 'sync')
    dirsync.sync(path, copyto, 'sync')


def on_created(event):
  dirSync()
  if compare_directories.common_files:  
    for common_file in compare_directories.common_files:
      path_directory_a = os.path.join(current_directory, server_a_directory, common_file)
      path_directory_b = os.path.join(current_directory, server_b_directory, common_file)
      if os.path.isfile(path_directory_a) and os.path.isfile(path_directory_b):
        directory_a_time = time.ctime(
          os.stat(os.path.join(current_directory, server_a_directory, common_file)).st_mtime)
        directory_b_time = time.ctime(
          os.stat(
            os.path.join(current_directory, server_b_directory, common_file)).st_mtime)
        if directory_a_time < directory_b_time and directory_a_time != directory_b_time:  
          print(common_file == file_name)
          path = os.path.join(current_directory, server_a_directory, common_file)
          if os.path.isfile(path and (common_file == file_name and operation != 'lock')):
            os.remove(path) 
          else:
            path = os.path.join(current_directory, server_b_directory, common_file)
            if os.path.isfile(path and (common_file == file_name and operation != 'lock')):
              os.remove(path) 
        elif directory_a_time != directory_b_time:
          path = os.path.join(current_directory, server_b_directory, common_file)
          if os.path.isfile(path and (common_file == file_name and operation != 'lock')):
            os.remove(path) 


def on_deleted(event):
  directory_a_path = os.getcwd() + '/folderOne/'
  directory_b_path = os.getcwd() + '/folderTwo/'

  a_path = os.path.join(directory_a_path, os.path.basename(event.src_path))

  b_path = os.path.join(directory_b_path, os.path.basename(event.src_path))

  file_name_to_be_deleted = os.path.basename(event.src_path)
  
  if file_name_to_be_deleted not in file_name_list:
    if os.path.isfile(a_path):
      os.remove(a_path)
    elif os.path.isfile(b_path):
      os.remove(b_path)


def on_modified(event):
  print(event.src_path + " Modified")


while True:

  dataframe = pd.DataFrame() 
  conn, addr = server_a.accept()  
  print('Got connection from server1', addr)

  data_from_client = conn.recv(4096)
  print(pickle.loads(data_from_client))
  loaded_data_from_client = pickle.loads(data_from_client)

  server_b = socket.socket() 
  port = 60024  
  server_b.connect((host, port)) 

  data = server_b.recv(4096)
  data_from_server_b = pickle.loads(data) 

  current_directory = os.getcwd() 
  server_a_directory = "folderOne"
  server_b_directory = "folderTwo"

  files_list = os.listdir(os.path.join(current_directory, "folderOne")) 

  compare_directories = filecmp.dircmp(os.getcwd() + "/" + server_a_directory, os.getcwd() + "/" + server_b_directory)

  patterns = ["*"]
  ignore_patterns = None
  ignore_directories = False
  case_sensitive = True
  my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
 
  my_event_handler.on_created = on_created  
  my_event_handler.on_deleted = on_deleted  
  my_event_handler.on_modified = on_modified  

  go_recursively = True

  observer_for_directory_a = Observer()  
  observer_for_directory_a.schedule(my_event_handler, current_directory + "/folderOne", recursive=go_recursively)
  observer_for_directory_a.start()  

  observer_for_directory_b = Observer()  
  observer_for_directory_b.schedule(my_event_handler, current_directory + "/folderTwo", recursive=go_recursively)
  observer_for_directory_b.start() 

  dataframe = data_from_server_b  

  print(dataframe)  

  if len(compare_directories.same_files) != len(os.listdir(os.path.join(current_directory, "folderOne"))) or len(
    compare_directories.same_files) != len(os.listdir(os.path.join(current_directory, "folderTwo"))):  # if file
   
    for file in files_list: 
      path = os.path.join(current_directory, server_a_directory, file)
      if os.path.isfile(path) and file not in compare_directories.same_files:
        status = os.stat(os.path.join(current_directory, server_a_directory, file)) 
        dataframe = dataframe.append({"File name": file, "size(kb)": float(status.st_size) / 1000,
                                      "Modified date": time.ctime(status.st_mtime)},
                                     ignore_index=True)  
        print(pickle.loads(pickle.dumps(dataframe)))

  data_for_client = dataframe.sort_values('File name').reset_index().drop(
    columns='index')  

  operation = ""  
  file_name_list = []  
  file_list_with_operations.append(loaded_data_from_client)
  if (len(file_name_list)) == 0:
    data_for_client.insert(len(data_for_client.columns), '', '') 
  if len(loaded_data_from_client) > 2:
    selected_index = int(loaded_data_from_client[1])  
    file_name = data_for_client.iloc[selected_index]['File name'] 
    operation = loaded_data_from_client[2] 
  for file_list_with_operation in file_list_with_operations:  
    if len(file_list_with_operation) > 2:
      selected_index_file = int(file_list_with_operation[1]) 
      file_name_with_operation = data_for_client.iloc[selected_index_file][
        'File name'] 
      operation = file_list_with_operation[2]  
      if operation == 'lock': 
        file_name_list.append(file_name_with_operation)
      elif operation == 'unlock':  
        if file_name_with_operation in file_name_list:
          file_name_list.remove(file_name_with_operation)
          file_list_with_operations.remove(file_list_with_operation)

     
      index = data_for_client.index
      condition = data_for_client["File name"] == file_name_with_operation
      file_name_indices = index[condition]
      file_name_indices_list = file_name_indices.tolist()
      for i in file_name_indices_list:
        if i != selected_index_file:
          data_for_client.drop(i, inplace=True)
          data_for_client.reset_index(inplace=True) 
        else:
          data_for_client.ix[selected_index_file, len(data_for_client.columns) - 1] = operation 
  if 'level 0' in dataframe.columns:
    data_for_client.droplevel('level_0', axis=1) 
  if 'index' in dataframe.columns:
    data_for_client.droplevel('index', axis=1)
  data_for_client = pickle.dumps(data_for_client)  
  print(pickle.loads(pickle.dumps(dataframe)))
  conn.sendall(
    data_for_client) 

  del dataframe 
  del data_for_client
