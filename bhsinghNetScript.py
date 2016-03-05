import sys
import socket
import getopt
import threading
import subprocess

#define some global variables here.
listen = False
command = False
upload = False
execute = ""
Target = ""
upload_destination = ""
port = 0

# this is my main function. Going to be used for handling command line arguments
#	for the rest of the functions
def usage():
	print "Bryan's Networking Tool :)"
	print
	print "Usage: bhsinghNetScript.py -t target_host -p port"
	print "-l --listen              - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute the given file upon receiving a connection"
    print "-c --command             - initialize a command shell"
	print "-u --upload=destination  - upon receiving connection upload a file and write to [destination]"
	print
	print
	print "Examples: "
	print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
	print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
	print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
	print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
	sys.exit(0)

def main():
	global listen
	global port
	global port
	global execute
	global command
	global upload_destination
	global target

	if not len(sys.argv[1:]:
		usage()
	# read the command line options
	try:

		opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help", "listen", "execute","target","port", "command", "upload"])
	except getopt.GetoptError as err:
		print str(err)
		usage()

	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-l", "--listen"):
			listen = True
		elif o in ("-e", "--execute"):
			execute = a
		elif o in ("c", "--Comandshell"):
			command = True
		elif o in ("u","--upload"):
			upload_destination = a
		elif o in ("t", "--target"):
			target = a
		elif o in ("p","--port"):
			port = int(a)
		else:
			assert False,"Unhandled Option"

	# are we going to listen or just send data from stdin
	if not listen and len(target) and port > 0:
		# read the buffer from the command line
		# this will  bblock, so send CTRL-D if no sending input
		# to stdin
		buffer  = sys.stdin.read()

		client_sender(buffer)

		#we are going to listen and potientially  upload things, exe commands, and drop a shell back depending  on our command line optins above
		if listen:
			server_loop()
main()
def client_sender(buffer):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		#connect to our target host
		client.connect((target,port))

		if len(buffer):
			client.send(buffer)

		while True:
			# now wait for data back
			recv_len = 1
			response = ""

			while recv_len:
				data = client.recv_len(4096)
				recv_len = len(data)
				response+=data

				if recv_len < 4096:
					break
			print response,

			# wait for some more imput
			buffer = raw_input("")
			buffer += "\n"

			#send it off
			client.send(buffer)

	except:

		print "[*] Exception! Exiing."

		# tear down the connection
		client.close()

def server_loop():

	global target

	#if no target is defined, we listen on all interfaces
	if not len(target):
		target = "0.0.0.0"

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target,port))

	server.listen(5)

	while True:
		client_socket, addr = server.accept()

		#spin off a thread to handle our new client

		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		client_thread.start()


def run_command(command):
	
	#trim the new line
	command = command.rstrip()

	#run the command  and get the output back
	try:
		output = subprocess.check_output(command,stderr=subprocess. STDOUT, shell=True)
	except:
		output = "Failed to execute command. \r\n"
	#send the output back to the client
	return output

def client_handler(client_socket):
	global upload
	global execute
	global command

	if len(upload_destination):
		
		#read in all of the bytes and write to our destination
		file_buffer = ""

		# keep reading data until nothing is aviable

		while True:
			data = client_socket.recv(1024)

			if not data:
				break
			else:
				file_buffer += data
		# take the bytes and write them out
		try:
			file_descriptor = open(upload_destination,"wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()

			#acknowledge that we wrote th e file out
			client_socket.send("Successfully saved to file to %s\r\n" % upload_destination)
		except:
			client_socket.send("Failed to save file to %s\r\n" % upload_destination)
	#check command execution
	if len(execute):
		
		#run the command
		output = run_command(execute)

		client_socket.send(output)
	if command:
		
		while True:
			#show a prompt
			client_socket.send("<BHP:#> ")

				(enter key)
				emd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)

			#send back to the command output
			response = run_command(cmd_buffer)

			#send back the resposne
			client_socket.send(resposne)