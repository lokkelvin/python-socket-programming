# Python socket programming
- HTTP Persistent & Non Persistent connections
- Multiple client server

For EE4210 Network Protocols and Applications

## 1. Prerequisites
Python 2.7: socket, sys, os and time libraries. 
The application is tested on Ubuntu 17.10 and Raspbian 8.

## 2. Running the application
**Server - Single Client mode**

In terminal, run the server.py file in the same directory as a.jpg, b.mp3 and c.txt. The command line arguments are <Mode> and <Port number>. Setting mode to 1 enables single-client mode, and setting mode to 2 enables multi-client mode.

`python server.py 1 12345`

**Server - Multiple Client mode**

Run the same command with mode set to 2.

`python server.py 2 12345`

**Client - Persistent HTTP**

Run the client_persistent.py file with the command line arguments <IP Address> and <Port number>. If the server is on a different computer, use ifconfig to determine its IP Address.

`python client_persistent.py 127.0.0.1 12345`


**Client - Non persistent HTTP**

Similarly, run the client_nonpersistent.py file with the command line arguments <IP Address> and <Port number>

`python client_nonpersistent.py 127.0.0.1 12345`


## 3. Measuring timings
The timings for the 3 file transfers are printed on the terminal in milliseconds.

## 4. Running your own files 
To transfer other files, the files will need to be renamed to either a.jpg, b.mp3 and c.txt. Only three files can be transferred at a time, because this is hardcoded into the client, but the code can be modified to send any number of files. It is possible to create your own GET Requests by using the get_request() helper function. 
