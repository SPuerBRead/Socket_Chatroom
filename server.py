# -*- coding: UTF-8 -*-
import socket
import threading
import time
import user
import chatroom
import json
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class lts_server():
    def __init__(self):
        self.alluser = []
        self.roomlist = []
        self.ISOTIMEFORMAT='%Y-%m-%d %X'

    def useraction(self,u):
        isStop = True
        try:
            logindata = u.sock.recv(1024) #username=input
            while self.user_check(logindata.split('=')[1].encode('utf-8')):
                u.send_msg('1')
                logindata = u.sock.recv(1024)
            u.username = logindata.split('=')[1].encode('utf-8')
            u.send_msg('             你正在使用2016年最古老最辣鸡的聊天室！！！！少侠，准备好跑起这个抠脚的程序了么？')
            time.sleep(0.01)
            u.send_msg('tab1') #------------------------------------------------------
            time.sleep(0.05)
            if len(self.roomlist) == 0:
                u.send_msg('[*]当前没有活动的房间，请创建。')
            else:
                u.send_msg('[+]存在可加入房间，请选择房间号加入，或创建新的房间。   e.g.:join 1')
                time.sleep(0.05)
                self.executive(u,'command=show rooms')
            while(isStop):
                data = u.sock.recv(1024)
                if data == 'logout':
                    isStop = False
                    u.send_msg('[+]下线成功。')
                    u.logout()
                    self.alluser.remove(u)
                elif data.startswith('cmd'):
                    self.executive(u,data)
                elif data.startswith('join'):
                    roomid = data.split(' ')[1]
                    u.house = roomid
                    flag = 0
                    for i in self.roomlist:
                        if i.ID == roomid:
                            i.addnewmember(u)
                            u.isinroom = True
                            flag = 1
                            u.send_msg('[+]加入房间成功。当前为命令模式，可获得聊天室相关信息，聊天模式请输入chat mode进行切换')
                            nowtime = str(time.strftime(self.ISOTIMEFORMAT, time.localtime(time.time()))).encode('utf-8')
                            for _u in self.alluser:
                                if _u.house == u.house and _u.username != u.username:
                                    _u.send_msg(u.username+'    加入本聊天室。  time: '+nowtime)
                            break
                    if flag == 0:
                        u.send_msg('[+]没有找到整个房间ID，请重新输入。')
                elif data == 'leave room':
                    for i in self.alluser:
                        if i.house == u.house and i.username != u.username:
                            i.send_msg(u.username+'    离开本聊天室。  time: '+nowtime)
                    for room in self.roomlist:
                        if room.ID == u.house:
                            room.remmember(u)
                    u.send_msg('[+]已经离开房间，等待命令。')
                    u.isinroom = False
                    u.house = 'None'
                elif data == 'chat mode':
                    self.chat_mode(u)
                else:
                    u.send_msg('[*] 未知的命令，或格式错误，请重新输入。')
        except:
            isStop = False
            for i in self.alluser:
                if i.house == u.house and i.username != u.username:
                    i.send_msg(u.username+'    离开本聊天室。  time: '+nowtime)
            u.logout()
            self.alluser.remove(u)

    def user_check(self,name):
        flag = 0
        for _ in self.alluser:
            if _.username == name:
                flag = 1
                break
        if flag == 0:
            return False
        else:
            return True

    def roomid_check(self,ID):
        try:
            intid = int(ID)
        except:
            return True
        flag = 0
        for _ in self.roomlist:
            if _.ID == ID:
                flag = 1
                break
        if flag == 0:
            return False
        else:
            return True


    def chat_mode(self,u):
        u.send_msg('[+]已经入聊天模式，所有的输入都会以聊天形式发出，cmd=*等命令不再有效，普通模式请输入normal mode进行切换。')
        while True:
            msg = u.sock.recv(1024)
            nowtime = str(time.strftime(self.ISOTIMEFORMAT, time.localtime(time.time()))).encode('utf-8')
            if msg == 'normal mode':
                break
            if msg == 'leave room':
                for i in self.alluser:
                    if i.house == u.house and i.username != u.username:
                        i.send_msg(u.username+'    离开本聊天室。  time: '+nowtime)
                for room in self.roomlist:
                    if room.ID == u.house:
                        room.remmember(u)
                    u.send_msg('[+]已经离开房间，自动切换至normal mode，等待命令。')
                    u.isinroom = False
                    u.house = 'None'
                    break
            for i in self.alluser:
                if i.house == u.house and i.username != u.username:
                    i.send_msg(u.username+': '+msg.encode('utf-8')+'                  time:'+nowtime)



    def executive(self,usersock,command):
        cmd = command.split('=')[1]
        if cmd == 'show user':
            returndict = {}
            userlist = []
            for _ in self.alluser:
                userlist.append(_.username)
            returndict['当前在线用户列表'] = userlist
            usersock.send_msg(json.dumps(returndict,ensure_ascii=False))
        elif cmd.startswith('create room'):  #create room:1:chat
            roomdetil = cmd.split(':')
            if self.roomid_check(roomdetil[1]):
                usersock.send_msg('[+]创建房间失败，房间ID不能重复，且必须为整数。请检查后重新输入。')
                return 
            r = chatroom.ChartRoom(roomdetil[1],roomdetil[2])
            self.roomlist.append(r)
            r.addnewmember(usersock)
            usersock.isinroom =True
            usersock.house=roomdetil[1].encode('utf-8')
            usersock.send_msg('[+]创建房间成功,ID: %s,name: %s! 已自动加入本房间' %(roomdetil[1],roomdetil[2])) 
        elif cmd == 'show rooms':
            returndict = {}
            msg = []
            for _ in self.roomlist:
                msg.append(str(_.ID+':'+_.name))
            returndict['当前活动房间列表'] = msg
            usersock.send_msg(json.dumps(returndict,ensure_ascii=False))
        elif cmd == 'show member':
            memberdict = {}
            if usersock.isinroom == True:
                for i in self.roomlist:
                    if i.ID == usersock.house:
                        memberdict['当前房间在线列表'] = i.getallmumber()
                        usersock.send_msg(json.dumps(memberdict,ensure_ascii=False))
        else:
            usersock.send_msg('[*] 未知的命令，或格式错误，请重新输入。') 


    def main(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(('0.0.0.0',9999))
        sock.listen(10)
        while(True):
            sk,addr = sock.accept()
            u = user.user(sk)
            self.alluser.append(u)
            th = threading.Thread(target=self.useraction,args=(u,))
            th.start()
        sock.close()

S = lts_server()
S.main()

