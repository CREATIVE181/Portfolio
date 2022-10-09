import CONFIG
import sql_requests

import socket
import asyncio

def commands(new_user, check_user):
    while True:
        msg = new_user.recv(1024).decode('utf-8')

        if check_user[3] != 'True' and msg.split()[0].lower() != 'select':
            new_user.send("You do not have enough rights for this command!\n".encode('utf-8'))
            commands(new_user, check_user)

        result = sql_requests.req(msg)
        if result[1] is True:
            new_user.send(str(result[0]).encode('utf-8'))

        elif result[0] is True:
            new_user.send(f'Error: {str(result[1])}\n'.encode('utf-8'))
        else:
            new_user.send("OK\n".encode('utf-8'))


def checker(new_user, login, password):
    check_user = sql_requests.cur.execute('SELECT * FROM users WHERE login = ?', (login,)).fetchone()

    if check_user is not None and password == check_user[1]:
        new_user.send("You are logged in!".encode('utf-8'))
        commands(new_user, check_user)
    else:
        new_user.send("Login or password was entered incorrectly!\nYou are disabled!".encode('utf-8'))


def authorization(new_user):
    login = new_user.recv(1024).decode('utf-8')
    password = new_user.recv(1024).decode('utf-8')
    checker(new_user, login, password)


def user(new_socket):
    while True:
        new_user = new_socket.accept()[0]
        new_user.send("You have joined the server!".encode('utf-8'))
        authorization(new_user)


def main():
    new_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    new_socket.bind((CONFIG.ip, CONFIG.port))
    new_socket.listen()

    print("Server is up!")
    user(new_socket)


if __name__ == '__main__':
    asyncio.run(main())
