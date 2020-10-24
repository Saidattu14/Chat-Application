import select
import socket
import sys
import time
import re
class socket_server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        try:
            self.server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print('socket created waitig for clients.........')
        except socket.error:
            print('Socked not created check address and port number')
            sys.exit()
        self.server_sock.bind((self.host,self.port))
        self.server_sock.listen(100)
        self.server_sock.setblocking(1)
    def server_run(self):
        client_list = [self.server_sock]
        nick_list =[]
        dic = {}
        while True:
            read_list,write_list,error_list = select.select(client_list,[],[])
            if self.server_sock in read_list:
                connection ,address = self.server_sock.accept()
                print('New_connection {} established'.format(address))
                nick_name = connection.recv(1024)
                sys.stdout.flush()
                nick_len = len(nick_name)
                msg1 = ('Hello {}'.format(nick_name))
                msg1 = bytes(msg1,'utf-8')
                connection.send(msg1)
                connection.setblocking(0)
                nick_list.append(nick_name)
                client_list.append(connection)
                dic [connection] = 1
            for client in read_list:
                if client != self.server_sock:
                    try:
                        data = client.recv(1024)
                        sys.stdout.flush()
                        if dic[client] == 1:
                            data = data.decode('utf-8')
                            data1 = data[5:]

                            if data[0:4] !='NICK':
                                msg2 = 'Error occured in nick name format it should be in NICK and nickname'
                                msg2 = bytes(msg2,'utf-8')
                                client.send(msg2)
                            else:
                                if len(data1)<=12 and len(data1)>=0:
                                    list = ['!','@','#','$','%','^','&','*','(',')','{','}','[',']',':','/','>','<','~','.','|']
                                    count = 0
                                    for i in range(len(list)):
                                        if list[i] in data1:
                                            count = count +1
                                    if count==0:
                                        print('okay nickname is verified')
                                        msg3 = 'ok Nick name has been stored'
                                        msg3 = bytes(msg3,'utf-8')
                                        client.send(msg3)
                                        dic[client] = 0
                                    else:
                                        msg4 = ('error check the nickname: nickname should contain  A-Z,a-z and 0-9')
                                        msg4 = bytes(msg4,'utf-8')
                                        client.send(msg4)
                                else:
                                    msg6 = 'ERROR : in nick name length'
                                    msg6= bytes(msg6,'utf-8')
                                    client.send(msg6)
                        else:
                            msg5 = data.decode('utf-8')
                            msg7 = msg5.strip('MSG')

                            if msg5[0:3] != 'MSG':
                                data2 = 'Message should be send in MSG and text format'
                                data2 = bytes(data2,'utf-8')
                                client.send(data2)
                            else:
                                if len(msg5) <= 255:
                                    count =0
                                    for i in msg5[:-1]:
                                        if ord(i)<31:
                                            count = count +1
                                        else:
                                            pass
                                    if count != 0:
                                        data3 = 'Error occured in in control characters'
                                        data3 = bytes(data3,'utf-8')
                                        client.send(data3)
                                    else:
                                        if msg7 ==' quit':
                                            print("client {} has been disconnected".format(data1))
                                            data4 = ('client' +' ' + data1+ 'is Disconnected')
                                            data4 = bytes(data4,'utf-8')
                                            client.send(data4)
                                            for i in client_list:
                                                if i!=self.server_sock and i!=client:
                                                    i.send(data4)
                                                elif i == client:
                                                    client_list.remove(i)
                                        else:
                                            for i in client_list:
                                                if i!=self.server_sock and i!=client:
                                                    data5 = ('MSG' +" "+ data1+ " "+msg7)
                                                    data5 = bytes(data5,'utf-8')
                                                    i.send(data5)
                                elif len(msg5) >256:
                                    data4 = 'message should be less than 256 characters'
                                    data4 = bytes(data4,'utf-8')
                                    client.send(data4)
                    except IOError:
                        continue
        self.server_sock.close()                               
def main():
    ser = socket_server(sys.argv[1],int(sys.argv[2]))
    ser.server_run()
if __name__ == "__main__":
    main()
