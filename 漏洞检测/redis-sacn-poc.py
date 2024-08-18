#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys


def check(ip, port, timeout, users_file=None, pass_file=None, test_usernames=False, test_passwords=True):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, int(port)))
            s.sendall(b"INFO\r\n")
            result = s.recv(1024).decode('utf-8')

            if "redis_version" in result:
                return f"[+] IP:{ip} ***************************存在未授权访问********************************"
            elif "Authentication" in result:
                if test_usernames and users_file:
                    with open(users_file, 'r') as uf:
                        users = [user.strip() for user in uf.readlines()]
                    for user in users:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_auth:
                            s_auth.connect((ip, int(port)))
                            auth_cmd = f"AUTH {user}\r\n".encode('utf-8')
                            s_auth.sendall(auth_cmd)
                            result = s_auth.recv(1024).decode('utf-8')
                            if 'OK' in result:
                                return f"[+] IP:{ip} 存在弱用户名：{user}"
                if test_passwords and pass_file:
                    with open(pass_file, 'r') as pf:
                        passwords = [passwd.strip() for passwd in pf.readlines()]
                    for passwd in passwords:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_auth:
                            s_auth.connect((ip, int(port)))
                            auth_cmd = f"AUTH {passwd}\r\n".encode('utf-8')
                            s_auth.sendall(auth_cmd)
                            result = s_auth.recv(1024).decode('utf-8')
                            if 'OK' in result:
                                return f"[+] IP:{ip} 存在弱口令，密码：{passwd}"
        return f"[-] IP:{ip} 无法访问或不易检测"
    except Exception as e:
        return f"[+] IP:{ip} 已过滤或无法连接: {str(e)}"


def get_ips():
    choice = input("选择 IP 获取方式：\n1. 从 IP.txt 文件中读取\n2. 输入单个 IP 地址\n请输入 1 或 2: ")

    if choice == '1':
        try:
            with open('IP.txt', 'r') as f:
                ips = [line.strip() for line in f.readlines()]
            if not ips:
                print("IP.txt 文件为空，请添加 IP 地址后再试。")
                sys.exit(1)
        except FileNotFoundError:
            print("未找到 IP.txt 文件，请确认文件存在后再试。")
            sys.exit(1)
    elif choice == '2':
        ip = input("请输入 IP 地址: ")
        ips = [ip]
    else:
        print("无效输入，请重新运行脚本并选择 1 或 2。")
        sys.exit(1)

    return ips


if __name__ == '__main__':
    ips = get_ips()
    port = input("请输入要扫描的端口号: ")
    timeout = int(input("请输入超时时间（秒）: "))

    auth_required = input("是否需要测试认证？(y/n): ").strip().lower()
    users_file = pass_file = None
    test_usernames = False
    test_passwords = True

    if auth_required == 'y':
        test_usernames = input("是否要测试用户名字典？(y/n): ").strip().lower() == 'y'
        test_passwords = input("是否要测试密码字典？(y/n): ").strip().lower() == 'y'

        if test_usernames:
            users_file = input("请输入用户名字典文件的路径 (默认: user.txt): ").strip() or 'user.txt'
        if test_passwords:
            pass_file = input("请输入密码字典文件的路径 (默认: pass.txt): ").strip() or 'pass.txt'

    for ip in ips:
        result = check(ip, port, timeout, users_file, pass_file, test_usernames, test_passwords)
        print(result)
