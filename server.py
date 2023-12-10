"""
Author: Daniel Ben Bassat
Date: 10/12/2023
Description: server side
"""
import socket
import functions
import logging
import os
import protocol


IP = '0.0.0.0'
PORT = 1011
QUEUE_LEN = 1

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


def call_func(msg):
    """
    calls function according to the cmd and returns its value
    :param msg: the cmd that the server receive
    :return: return the value of the func with the parameter
    """
    if msg[0] == "DIR":
        return functions.dir(msg[1])
    if msg[0] == "DELETE":
        return functions.delete(msg[1])
    if msg[0] == "COPY":
        return functions.copy(msg[1])
    if msg[0] == "EXECUTE":
        return functions.execute(msg[1])
    if msg[0] == "SCREENSHOT":
        return functions.screenshot()
    if msg[0] == "SENDPHOTO":
        return functions.send_photo()


def main():
    """

    connect to the client and receive the cmd and the parameter the client sends.
    sends to client the name of the cmd and the response from the func "call func
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind((IP, PORT))
        my_socket.listen(QUEUE_LEN)

        while True:
            client_socket, client_address = my_socket.accept()

            try:
                check = True
                while check:
                    msg = protocol.receive_protocol(client_socket)
                    logging.debug(msg)
                    if msg[0] != "EXIT":
                        response = call_func(msg)
                        client_socket.send(protocol.protocol_send(msg[0], response))
                        logging.debug(protocol.protocol_send(msg[0], response))
                    else:
                        check = False

            except socket.error as err:

                print('received socket error on client socket' + str(err))

            finally:
                print("client left")
                client_socket.close()

    except socket.error as err:
        print('received socket error on server socket' + str(err))

    finally:
        my_socket.close()


if __name__ == "__main__":
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    assert functions.dir(r"C:\work\cyber") != functions.ERROR_MSG
    assert functions.copy(r"C:\work\cyber\old.txt C:\work\cyber\new.txt") == functions.SUCCEED_MSG
    assert functions.delete(r"C:\work\cyber\new.txt") == functions.SUCCEED_MSG
    #assert functions.execute(r'C:\Windows\System32\notepad.exe') == functions.SUCCEED_MSG
    assert call_func(("DIR", r"C:\work\cyber")) == functions.dir(r"C:\work\cyber")
    #assert call_func(("EXECUTE", r'C:\Windows\System32\notepad.exe')) == functions.execute(r'C:\Windows\System32\notepad.exe')
    assert protocol.protocol_send("daniel", "ben") == b'6!daniel3!ben'
    assert protocol.protocol_send("dir", "cyber") == b'3!dir5!cyber'
    main()
