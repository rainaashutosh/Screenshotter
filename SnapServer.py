import socket
import time

HOST = ''
PORT = 9877
ADDR = (HOST,PORT)
BUFSIZE = 4096

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(ADDR)
serv.listen(5)

print 'listening ...'
counter=0
while True:
	conn, addr = serv.accept()
	print 'client connected ... ', addr
	a=time.ctime(time.time())
	filename = "Exfiltrated"+a[4:7]+a[8:10]+a[11:13]+a[14:16]+a[17:19]+".png"
	myfile = open(filename, 'w')
	while True:
		data = conn.recv(BUFSIZE)
		if not data: 
			print 'eof'
			break
		myfile.write(data)
		print 'writing file ....'
	myfile.close()
	counter=counter+1
	print 'finished writing file'
	conn.close()
	print 'client disconnected'	

