# -*- coding: utf-8 -*-
import socket


def get_local_ip():
    localIP = socket.gethostbyname(socket.gethostname())
    return localIP

def is_inuse(port, ip_list=None):
    if not ip_list:
        ip_list = ("127.0.0.1", "0.0.0.0", get_local_ip())
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = True
    for ip in ip_list:
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            flag = True
            break
        except:
            flag = False
    return flag


def find_serial_port(start_port, count=1):
    """
    获取连续可用端口
    :param start_port:
    :param count:
    :return:
    """
    if count and count < 1:
        count = 1
    ip_list = ("127.0.0.1", "0.0.0.0", get_local_ip())
    while True:
        flag = True
        end_port = start_port
        for i in range(count):
            if is_inuse(end_port, ip_list):
                flag = False
                break
            else:
                end_port += 1

        if flag:
            break
        else:
            start_port = end_port + 1

    return [start_port + i for i in range(count)] if count > 1 else start_port


def find_port(start_port, count=1):
    """
    获取可用端口
    :param start_port:
    :param count:
    :return:
    """
    if count and count < 1:
        count = 1
    ip_list = ("127.0.0.1", "0.0.0.0", get_local_ip())
    port_list = []
    while True:
        if port_list.__len__() == count:
            break
        if not is_inuse(start_port, ip_list):
            port_list.append(start_port)
        start_port += 1
    return port_list if count > 1 else port_list[0]