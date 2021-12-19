from sockets.server import Server

server = Server()   # TODO: do singleton
server.setup_sockets()
server.main()
