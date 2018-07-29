# spider

一、简易动态IP池--Proxy_pool.py

1.自己写了一个动态IP池脚本，定时爬取西刺免费代理网站的前两页，每10分钟重新爬区一次，从而保证爬取到的IP都是新鲜的IP。

2.采用socket服务器与客户端通讯的方式来获取，最新的代理IP。使用socket客户端向服务器发送get proxy指令即可获取代理IP。

3.基本使用方法：

    import socket #导入socket模块

    def main():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #建立一个socket客户端
        s.connect(('127.0.0.1', 9999))                         #连接到ip池服务器相应的地址默认是127.0.0.1:9999  可以自己在代码中修改。
        print(s.recv(1024).decode('utf-8'))                    #显示服务器欢迎信息
	a = input('请输入你要干什么:')
        s.send(a.encode('utf-8'))                              #输入get a new proxy
        print(s.recv(1024).decode('utf-8'))                    #打印获取到的proxy详情
        s.send(b'exit')                                        #向服务器发送exit来停止服务器的接收功能
        s.close()                                              #关闭客户端和服务器的链接
    
    if __name__ == '__main__':
        main() 
