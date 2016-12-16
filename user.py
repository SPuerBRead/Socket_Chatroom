# -*- coding: UTF-8 -*-
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class user():
    def __init__(self,sock,username='None'):
        self.sock = sock
        self.username = username
        self.house = 'None'
        self.isinroom = False

    def join_room(self,ID):
        self.house = ID

    def send_msg(self,msg):
        self.sock.send(msg)

    def leave_house(self):
        self.house = 'None'
        
    def logout(self):
        self.sock.close()
