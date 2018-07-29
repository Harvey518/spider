import re
import time
import random
import socket
import requests
import multiprocessing as mp
import threading as td
import subprocess as sp

# 设置代理池爬取得基础网页地址
base_url = 'http://www.xicidaili.com/nn/'

# 设置需要爬取的代理网站的页数
page = 2

# 设置headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

# 创建一个multiprocessing的Manager对象，并创建一个list,用来设置进程间的通讯
mgr = mp.Manager()
d = mgr.list()


def get_proxy(html):
    # 利用正则表达式把需要获取的信息相关信息爬取下来，并yield一个存放ip信息的字典迭代器
    infos = re.findall(r'<tr\sclass.*?</td>.*?>(.*?)</.*?<td>(.*?)</.*?"country">.*?<td>(.*?)</',html, re.S)
    for info in infos:
        yield {
            'ip': info[0],
            'port': info[1],
            'style': info[2]
        }

def choose_proxy(pools):
    # 随机从存放ip字典的列表中选取一个列表
    proxy = random.choice(pools)
    ip = proxy['ip']
    # 利用subproces中的Popen,来在终端输入相应的判断ip是否是无效IP的指令，并获取返回文本
    cmd = f'ping -t 3 {ip}'
    a = sp.Popen(cmd,stdin=sp.PIPE, stdout=sp.PIPE,stderr=sp.PIPE, shell=True)
    stdout = a.stdout.read().decode('utf8')
    # 利用正则表达式匹配timout关键字，来判断ip是否非法。
    compile = re.compile(r'(timout)',re.S)
    timeout = re.search(compile,stdout)
    if not timeout:
        # 若不是非法ip则返回相应的ip,端口号，类型
        return ip,proxy['port'], proxy['style']
    else:
        # 若是非法IP则从列表中删除对应的IP所属的字典,并重新调用本身函数
        pools.remove(proxy)
        return get_proxy(pools)

def set_get_choose(d):
    # 一个建立IP池，爬取IP，选择合法IP的综合函数
    global page
    print('Start to build proxy pool..')
    a = 0
    while True:
        if a >= 1:
            print('Start to refresh proxy pool..')
        for i in range(1, page + 1):
            # 每次只爬取前两页的内容
            url = base_url + str(i)
            response = requests.get(url=url, headers=headers)
            proxies = get_proxy(response.text)
            for proxy in proxies:
                d.append(proxy)
        # 每隔10分钟刷新一次保证IP池的新鲜性
        time.sleep(600)
        a += 1



def tcplink(sock, addr, proxypool):
    # 处理服务器与客户端的之间的交流
    print(f'Accept new connection from {addr}...')
    # 服务器向客户端发送欢迎消息
    sock.send(b'Welcome to proxypool...')
    while True :
        data = sock.recv(1024)
        time.sleep(1)
        # 如果客户端发送exit则服务器断开与客户端的链接
        if data.decode('utf-8') == 'exit' :
            break
        if data.decode('utf-8') == 'get proxy':
            # 如果发送 get proxy指令则服务器调用choose_proxy函数获取相关信息
            ip, port, style = choose_proxy(proxypool)
            # 判断ip相应的协议类型，并格式化返回给客户端
            if style == 'HTTP':
                new_ip = f'http://{ip}:{port}'
                sock.send(new_ip.encode('utf-8'))
                print(f'Send {new_ip} to {addr}')
            else:
                new_ip = f'https://{ip}:{port}'
                sock.send(new_ip.encode('utf-8'))
                print(f'Send {new_ip} to {addr}')
    sock.close()
    print(f'Connection from {addr} closed.')


def set_socket(d):
    # 建立socket服务器
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听127.0.0.1:9999端口
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    print('Waiting for conecting...')
    while True:
        # 创建一个新线程来专门处理服务器与客户端的链接
        sock, addr = s.accept()
        t = td.Thread(target=tcplink, args=(sock, addr, d))
        t.start()

def main():
    # IP池的主程序,创建一个进程来运行爬取IP的主函数
    p1 = mp.Process(target=set_get_choose, args=(d,))
    p1.start()
    # 运行socket服务器函数
    set_socket(d)

if __name__ == '__main__':
    main()
