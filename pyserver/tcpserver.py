import socket, threading

BACKLOG_LISTEN = 5
PAYLOAD_LEN = 2048
SERVER_LISTEN_PORT = 9999
SERVER_HOST = "localhost"

import PDSDlogging, logging
log = PDSDlogging.PDSDlogging('MAIN_Logger', 'logs/PDSD_TCPServer.log', logging.DEBUG)
log = log.logger

client_id = 0
clients_list = []
cli_sock_list = []

class ClientThread(threading.Thread):

    def __init__(self,ip,port,socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        log.info("[+][NEW THREAD] for "+ip+":"+str(port))


    def run(self):
        global cli_sock_list
        global clients_list
        global client_id


        log.info("Accepted connection from : " + ip + " : " + str(port))
        client_id = client_id + 1
        clients_list.append(client_id)
        clientsock = self.socket
        clientsock.send("\nWelcome to PDSD TCP Server\n\n")

        data = "NONE"

        while len(data):
            data = clientsock.recv(PAYLOAD_LEN)
            log.info("[CLIENT %d] Payload msg %s : " % (client_id,  str(data)))
            clientsock.send("You sent me : " + data)

        log.info("[CLIENT] ID=%d disconnected" % client_id)
        clients_list.remove(client_id)
        cli_sock_list.remove(clientsock)

if __name__ == "__main__":
    #global cli_sock_list
    #global clients_list
    #global client_id

    host = SERVER_HOST
    port = SERVER_LISTEN_PORT

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcpsock.bind((host,port))
    threads = []
    client_id = 0

    print 'PDSD TCP Server started'

    while True:
        try:
            tcpsock.listen(BACKLOG_LISTEN)
            #print "\nListening for incoming connections..."
            (clientsock, (ip, port)) = tcpsock.accept()
            newthread = ClientThread(ip, port, clientsock)
            cli_sock_list.append(clientsock)
            newthread.daemon = True
            log.debug("Client ID list: %s " % str(clients_list))
            log.debug("Client Sockets list: %s " % str(cli_sock_list))
            newthread.start()
            threads.append(newthread)
        except (KeyboardInterrupt, SystemExit):
            print '\n! Received keyboard interrupt, attempt to join threads, now quitting.\n'
            for sock in cli_sock_list:
                sock.close()

            for t in threads:
                t.join()
            exit(0)

    for t in threads:
        t.join()
