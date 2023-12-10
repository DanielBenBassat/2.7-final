"""
Author: Daniel Ben Bassat
Date: 10/12/2023
Description: client side
"""
import socket
import logging
import os
import protocol
import functions

IP = '127.0.0.1'
PORT = 1011

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/client.log'

INITIAL_MSG = """enter one of these functions:
                 DIR + 1 parameter   
                 DELETE + 1 parameter
                 COPY + 2 parameter
                 EXECUTE + 1 parameter
                 SCREENSHOT
                 EXIT """


def valid_func(cmd):
    """
    get a command and check if its valid
    :param cmd: the command that was entered
    :return: true if the command is valid and false if not
    """
    cmd_list = ['DIR', 'DELETE', 'COPY', 'EXECUTE', 'SCREENSHOT', 'EXIT']
    if cmd in cmd_list:
        return True
    return False


def enter_par(cmd):
    """
    tells us if we need to enter a parameter or not according to the command
    :param cmd: the command that was entered
    :return: the parameter empty if the cmd is screenshot or exit, or our input
    """
    if cmd == "DIR" or cmd == "DELETE" or cmd == "COPY" or cmd == "EXECUTE":
        par = input("enter one parameter or two with space if the cmd is copy: ")
    else:
        par = ""
    return par


def main():
    """
    first thing create connection between client and server
    enter a cmd and add its parameter
    send the cmd and the parameter to the server
    receive the cmd and the response and print it
    if cmd is exit close socket
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        print(INITIAL_MSG)
        check = True
        while check:
            cmd = input("enter the cmd: ")
            if valid_func(cmd):
                parameter = enter_par(cmd)
                my_socket.send(protocol.protocol_send(cmd, parameter))
                logging.debug(protocol.protocol_send(cmd, parameter))
                if cmd != "EXIT":
                    response = protocol.receive_protocol(my_socket)
                    if cmd != "SCREENSHOT":
                        print('the command is: ' + response[0] + ' ,the response is: ' + response[1])
                        logging.debug('Received the command: ' + response[0] + ' and the response: ' + response[1])
                    else:
                        logging.debug(response[1])
                        print(functions.save_image(response[1]))

                        logging.debug(functions.save_image(response[1]))

                else:
                    check = False
            else:
                print("wrong input, enter again")

    except socket.error as err:
        print('received socket error ' + str(err))

    finally:
        print("client left the server")
        my_socket.close()


if __name__ == "__main__":
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    assert valid_func("DIR")
    assert valid_func("DELETE")
    assert valid_func("COPY")
    assert valid_func("EXECUTE")
    assert valid_func("SCREENSHOT")
    assert valid_func("EXIT")
    assert enter_par("EXIT") == ""
    assert enter_par("SCREENSHOT") == ""
    assert protocol.protocol_send("daniel", "ben") == b'6!daniel3!ben'
    assert protocol.protocol_send("dir", "cyber") == b'3!dir5!cyber'
    main()