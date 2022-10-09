import CONFIG

import socket


def commands(socket_server):
    while True:
        socket_server.send(input('Your command: ').encode('utf-8'))
        msg = socket_server.recv(1024).decode('utf-8')
        print(msg)

def authorization(socket_server):
    login = input('Your login: ')
    socket_server.send(login.encode('utf-8'))

    password = input('Your password: ')
    socket_server.send(password.encode('utf-8'))

    server_check = socket_server.recv(1024).decode('utf-8')
    print(server_check + '\n')
    if server_check == 'Login or password was entered incorrectly!':
        exit()
    commands(socket_server)

def connected(socket_server):
    server_hello = socket_server.recv(1024).decode('utf-8')
    print(server_hello)
    authorization(socket_server)

def main():
    socket_server = socket.socket()
    try:
        socket_server.connect(
            (CONFIG.ip, CONFIG.port)
        )
        connected(socket_server)
    except ConnectionRefusedError:
        print('Server is not available!')
        exit()


if __name__ == '__main__':
    main()
