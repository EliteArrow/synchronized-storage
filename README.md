# Synchronized Storage
The file transfer between the client and the server can be made transparent to users and automatically handled by a helper thread. This creates a cloud synchronized storage service. Whenever changes are made to the synchronized folder at the client, e.g., creating a new file, updating a file, or deleting a file, the helper thread will establish a connection with the server and automatically send the corresponding operation to the server to update the folder at the server side.

## Redme
#### Step 1:<br/>
Start the server on one command prompt use:<br/>
python serverA.py<br/>

#### Step 2:<br/>
Start the server on one command prompt use:<br/>
python serverB.py<br/>

#### Step 3:<br/>
Start another command prompt and use the following command and check the file operations.<br/>
python client.py<br/>

#### Step 4: <br/>
Perform upload file, download file, modify file and delete file in one directory and running server automatically reflect changes to another directory
