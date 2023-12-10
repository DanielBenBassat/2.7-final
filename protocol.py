def protocol_send(cmd, param):
    cmd_len = len(cmd)
    param_len = len(param)
    final_message = str(cmd_len).encode() + b'!' + cmd.encode() + str(param_len).encode() + b'!' + param.encode()
    return final_message


def receive_protocol(my_socket):
    cmd_len = ''
    par_len = ''
    try:
        cur_char = my_socket.recv(1).decode()
        while cur_char != '!':
            cmd_len += cur_char
            cur_char = my_socket.recv(1).decode()

        cmd = my_socket.recv(int(cmd_len)).decode()

        cur_char = my_socket.recv(1).decode()
        while cur_char != '!':
            par_len += cur_char
            cur_char = my_socket.recv(1).decode()
        param = my_socket.recv(int(par_len)).decode()
        final_message = (cmd, param)

    except:
        final_message = ('Error', '')
    finally:
        return final_message