import socket
import threading
import re
import random
import time
from urllib import request, parse
import gc

HOST, PORT = "0.0.0.0", 1699


class Singleton(object):
    __instance = None
    __LinkedNum = 0
    __lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get():
        Singleton.__lock.acquire()
        num = Singleton.__LinkedNum
        Singleton.__lock.release()
        return num

    @staticmethod
    def increase():
        Singleton.__lock.acquire()
        Singleton.__LinkedNum += 1
        Singleton.__lock.release()

    @staticmethod
    def decrease():
        Singleton.__lock.acquire()
        Singleton.__LinkedNum -= 1
        Singleton.__lock.release()

    def __new__(cls, *args, **kwd):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls, *args, **kwd)
            # Singleton.__lock = threading.Lock
        return Singleton.__instance


def rand_str(length):
    string = "abcdefghijklmnopqrstuvwxyz123456789"
    t = int(round(time.time() * 1000))
    ret = ""
    for i in range(0, length):
        num = random.randrange(0, len(string) - 1)
        ret += string[num]
    return ret + str(t)


def customer(client_connection):
    Singleton().increase()
    des = ""
    http_response = ""
    # time.sleep(3)
    try:
        request = client_connection.recv(1024)
        try:
            print(request.decode('utf8'))
            des = re.findall("/des=(.*?) HTTP", request.decode('utf8'))[0]
            print(des)
            des = parse.unquote(des)
        except:
            http_response += "format error"
            pass
        ## event
        if des != "":
            http_response = "o1k"
        http_head = "HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: " + str(len(http_response)) + "\r\nContent-Type: text/html\r\n\r\n"
        res = http_head + http_response
        print(res)
        client_connection.send(res.encode("utf-8"))
    except:
        print('err')
        pass
    finally:
        client_connection.close()
        Singleton().decrease()
        gc.collect()


def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(5)
    while True:
        client_connection, client_address = listen_socket.accept()
        # print(Singleton().get())
        if Singleton().get() > 10:
            client_connection.close()
        else:
            threading.Thread(target=customer, args=(client_connection,)).start()


if __name__ == '__main__':
    main()
