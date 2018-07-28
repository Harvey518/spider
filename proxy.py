import re
import time
import requests
import random
import socket
import threading as td
import subprocess as sp

base_url = 'http://www.xicidaili.com/nn/'

page = 2

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

proxy_pool = []

def get_proxy(html):
    infos = re.findall(r'<tr\sclass.*?</td>.*?>(.*?)</.*?<td>(.*?)</.*?"country">.*?<td>(.*?)</',html, re.S)
    for info in infos:
        yield {
            'ip': info[0],
            'port': info[1],
            'style': info[2]
        }

def choose_proxy(pools):
    proxy = random.choice(pools)
    ip = proxy['ip']
    cmd = f'ping -t 3 {ip}'
    a = sp.Popen(cmd,stdin=sp.PIPE, stdout=sp.PIPE,stderr=sp.PIPE, shell=True)
    stdout = a.stdout.read().decode('utf8')
    compile = re.compile(r'(timout)',re.S)
    timeout = re.search(compile,stdout)
    if not timeout:
        return ip,proxy['port'], proxy['style']
    else:
        pools.remove(proxy)
        return get_proxy(pools)

def set_get_choose():
    global page, proxy_pool
    print('Start to build proxy pool..')
    while True:
        print('Start to refresh proxy pool..')
        for i in range(1, page + 1):
            url = base_url + str(i)
            response = requests.get(url=url, headers=headers)
            proxies = get_proxy(response.text)
            for proxy in proxies:
                proxy_pool.append(proxy)
        return proxy_pool
        time.sleep(300)

# def get_a_new_proxy(pool)

def tcplink(sock, addr, proxypool):
    print(f'Accept new connection from {addr}...')
    sock.send(b'Welcome to proxypool...')
    while True :
        data = sock.recv(1024)
        time.sleep(1)
        if data.decode('utf-8') == 'exit' :
            break
        print(data.decode('utf-8'))

        if data.decode('utf-8') == 'get a new proxy':

            ip, port, style = choose_proxy(proxypool)
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


def main():
    proxypool = set_get_choose()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    print('Waiting for conecting...')
    while True:
        sock, addr = s.accept()
        t = td.Thread(target=tcplink, args=(sock, addr, proxypool))
        t.start()


if __name__ == '__main__':
    main()