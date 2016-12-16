# -*- coding: UTF-8 -*-
import socket
import argparse
import threading
import time
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

class lts_client():
    def __init__(self,host,port):
        self.isStop =True
        self.host = host
        self.port = port

    def recv_msg(self,s):
        while self.isStop:
            data = s.recv(1024)
            try:
                jsondata = json.loads(data, encoding='utf-8')
                print '\033[1;31;40m%s\033[0m' %jsondata.keys()[0].decode('utf-8').encode(sys.stdin.encoding)
                for _ in jsondata[jsondata.keys()[0]]:
                    print '\033[1;31;40m%s\033[0m' %_.decode('utf-8').encode(sys.stdin.encoding)
            except:
                if data == 'tab1':
                    print '\033[1;32;40m-------------------------------------------------------------------------------------------------------\033[0m' 
                else:
                    print '\033[1;31;40m%s\033[0m' %data.decode('utf-8').encode(sys.stdin.encoding)

    

    def main(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((self.host,int(self.port)))
            while True:
                username = raw_input('请输入你的昵称：'.encode(sys.stdin.encoding))
                s.send('username='+username.decode(sys.stdin.encoding).encode('utf-8'))
                data = s.recv(1024)
                if data == '1':
                    print '\033[1;31;40m昵称已被占用\033[0m'.encode(sys.stdin.encoding)
                else:
                    break
            th = threading.Thread(target=self.recv_msg,args=(s,))
            th.start()
        except:
            self.isStop = False
            print 'error'
        while self.isStop:
            msg = raw_input()
            s.send(msg.decode(sys.stdin.encoding).encode('utf-8'))
            if msg == 'logout':
                self.isStop = False
        s.close()


def show_help():
    print '''
    使用流程：
        1.输入昵称
        2.创建或加入房间
        3.选择模式 1）聊天模式 2）命令模式

    命令（部分仅在命令模式下）：
        1.创建房间 cmd=create room:1:聊天室1 第一个冒号后边为房间ID，第二个为房间名称，ID不能冲突
        2.加入房间 join 1 即join 房间ID
        3.查看所有在线用户 cmd=show user
        4.查看所有房间 cmd=show rooms
        5.查看房间内所有用户 cmd=show member
        6.切换聊天模式 chat mode 默认为命令模式
        7.切换到命令模式 normal mode
        8.离开房间 leave room
        9.下线 logout
    '''.encode(sys.stdin.encoding)

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-u', dest = 'host' , help = '127.0.0.1')
    parse.add_argument('-p', dest = 'port' ,type=int,help = '9999')
    parse.add_argument('--allhelp', dest = 'allhelp' ,action = 'store_true', default = False , help = 'show all help')
    args = parse.parse_args()
    host = args.host
    port = args.port
    ishelp = args.allhelp
    if ishelp:
        show_help()
        exit()
    else:
        c = lts_client(host,port)
        c.main()






