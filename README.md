# Synchronized Storage

## Project Description:

The file transfer between the client and server can be made transparent to users and automatically handled by helper thread. This creates a Dropbox-like synchronized storage service. Whenever changes are made to the synchronized folder at the client side, e.g., creating a new file, updating a file, or deleting a file, the helper thread will establish a connection with the server and automatically send the corresponding operation to the server to update the folder at the server side. You can configure the helper thread to periodically check if there are changes made to the synchronized folder. If the last update time to a file is later than the last check, the file should be synchronized. To simplify the design, we do not need to consider incremental updates. Thus, if the content of a file is updated, the entire file should be sent to the server to overwrite the original copy at the server

## How to use:

**Step 1:** Go to project directory and start the serverOne on one command prompt use

```
python serverA.py
```

**Step 2:** Start the serverTwo on second command prompt use

```
python serverB.py
```

**Step3:** Start another command prompt and start client

```
python client.py
```

Step 4: perform basic operation on files in any directory

- Create file
- Update file
- Delete file

![Untitled](https://raw.githubusercontent.com/EliteArrow/synchronized-storage/main/Screenshot.jpeg)

### Key Features:

1. **Real-time Synchronization**: The system constantly monitors a specified folder on the client-side for any changes such as file creation, update, or deletion. Any changes are automatically sent to the server to keep both folders synchronized.
2. **Automatic File Transfer**: A helper thread is used to automatically handle file transfer between the client and server, making the process transparent to the user.
3. **File Locking**: The system supports file locking, which means a file can be "locked" to prevent other processes from changing it while it's being modified.
4. **Two-Way Synchronization**: The system can synchronize files not only from the client to the server but also from the server to the client, ensuring that both folders are identical at all times.
5. **File Comparison**: The system can compare files in two directories, and make updates based on the last modified time of the files.

### Technologies and Libraries Used:

1. **Python**: The primary language used to build the project.
2. **Socket Programming**: Used for setting up the connections between the client and the server, allowing them to communicate and exchange data.
3. **Pickle Module**: Used for serializing and deserializing Python object structures, allowing them to be sent over network connections.
4. **Watchdog Library**: Used to monitor the client-side folder for any changes.
5. **Dirsync Module**: Used to synchronize directories.
6. **Pandas Library**: Used for data manipulation and analysis, primarily through its DataFrame object.
7. **Filecmp Module**: Used for file and directory comparisons.
8. **os and sys Modules**: Used for interacting with the operating system, providing functions to navigate, create, delete, and modify files and directories.
9. **Filelock Module**: Used to handle file locking mechanism.
10. **Time Module**: Used for handling time-related tasks.
