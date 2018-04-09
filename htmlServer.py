import sys
import socket
import select

if __name__ == '__main__':

    # check command line args
    if len(sys.argv) != 2:
        print('invalid arguments')
        sys.exit(0)

    # set addr
    port = int(sys.argv[1])
    addr = ('localhost', port)

    # create server socket and bind it to port
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(addr)
    serverSock.listen(5)
    print('Server started on port %s' % port)

    clientList = []

    while True:

        checkToRead = clientList[:]
        checkToRead.append(serverSock)
        # select
        socksToRead, _, _ = select.select(checkToRead, [], [])

        for sock in socksToRead:

            # check if new connection
            if sock == serverSock:

                # create socket for client and add to client list
                clientSock, clientAddr = serverSock.accept()
                clientList.append(clientSock)
                print('Client connected')

                # parse http request
                httpRequest = clientSock.recv(256).decode('utf-8')
                httpLines = httpRequest.splitlines()
                uri = httpLines[0].split(' ')[1]

                # load html file
                file = open(uri[1:], 'r')

                # create http response
                responseHeader = 'HTTP/1.1 200 OK\n' \
                                 'Content-Type: text/html\n' \
                                 'Connection: close\n\n'
                responseBody = file.read()

                # send http response
                clientSock.send(bytes(responseHeader, 'utf-8'))
                clientSock.send(bytes(responseBody, 'utf-8'))








