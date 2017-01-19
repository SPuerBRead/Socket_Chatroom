# Socket_Chatroom
应付作业弄个小聊天室-。-只是写写，可能还存在一些小问题

python多线程socket终端下的聊天室demo。

实现了基本的聊天室功能，可以在windows和linux下运行，中文没有问题，使用系统的编码进行输出，不会出现乱码问题。

#使用说明：

    使用流程：
  
        1.输入昵称
        
        2.创建或加入房间（昵称和房间号都是唯一的，不能为空。）
        
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
        
        
        
#启动方法

服务器 python server.py

客户端 python client.py -u 127.0.0.1 -p 9999
