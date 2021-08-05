
import socket
import ssl
from bs4 import BeautifulSoup
import csv
import threading
import os





def downloadImage(url, picName):

	hostname = 'www.rit.edu'
	context = ssl.create_default_context()

	with socket.create_connection((hostname, 443)) as sock:
		with context.wrap_socket(sock, server_hostname=hostname) as ssock:
		    request = "GET "+url+" HTTP/1.1\r\nHost: www.rit.edu\r\nAccept: */*\r\n\r\n"
		    ssock.send(request.encode())


		    data=b''
		    while True:
	        	temp=ssock.recv(1)
	        	if temp is None or len(temp)==0:
	        		break
	        	data+=temp

	ssock.close()


	#Get rid of header
	headers = data.split(b'\r\n\r\n')[0].decode()

	if "image/png" not in headers and "image/jpeg" not in headers: 
		return


	#Getting image and 
	image = data[len(headers)+4:]

	with open("images/"+picName+".png", mode='wb') as file:
	# file = open("images/"+picName+".png", "wb")
		file.write(image)
		file.close()

	return







def main():

	threads = [] 
	hostname = 'www.rit.edu'
	context = ssl.create_default_context()


	#create the image folder
	path = "images"
	os.mkdir(path)


	#creating sockets and getting html
	with socket.create_connection((hostname, 443)) as sock:
	    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
	        request = "GET /gccis/computingsecurity/people HTTP/1.1\r\nHost: www.rit.edu\r\nAccept: text/html, */*\r\n\r\n"
	        ssock.send(request.encode())

	        data=b''
	        while True:
	        	temp=ssock.recv(1)
	        	if temp is None or len(temp)==0:
	        		break
	        	data+=temp

	        ssock.close()


	#parse html for image url
	soup = BeautifulSoup(data, 'html.parser')

	img_tags = soup.find_all('img')

	urls = [img['src'] for img in img_tags]



	#getting image
	#name counter
	picName = 0
	for url in urls:
		#Open a thread 
		thr = threading.Thread(target=downloadImage, args=(url,str(picName),))
		threads.append(thr)
		thr.start()
		picName += 1
	#closing threads
	for thr in threads:
		thr.join()


	return








	


main()