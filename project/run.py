from chathouse import create_app,socket

if __name__=='__main__':
	socket.run(create_app())