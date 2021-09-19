#coding:utf-8
import paramiko
import time

hostname = "xxx"
username = "xxx"
password = "xxx"
shadow_password = "xxx"

def main():
    paramiko.util.log_to_file('syslogin.log')     #发送paramiko日志到syslogin.log文件
    print(hostname)
    print(username)

    ssh = paramiko.SSHClient()          #创建一个SSH客户端client对象
    ssh.load_system_host_keys()         #获取客户端host_keys,默认~/.ssh/known_hosts,非默认路径需指定ssh.load_system_host_keys(/xxx/xxx) 
    ssh.connect(hostname=hostname,username=username,password=password)    #创建SSH连接
    
    invoke = ssh.invoke_shell()

    print("---------")
    result = invoke.recv(4096).decode("utf-8")
    print(result)

    print("---------")
    invoke.send("ls -l\n")
    time.sleep(2)
    result = invoke.recv(4096).decode("utf-8")
    print(result)


    print("---------")
    invoke.send("ps -AT | grep sha\n")
    time.sleep(2)
    result = invoke.recv(4096).decode("utf-8")
    print(result)
    

    print("---------")
    lines = result.strip().split("\n")
    print(len(lines))
    for line in lines:
        print(line)
    cmd = lines[0]
    ret = lines[1:]
    if (len(ret) > 1):
        listlist = ret[0].strip().split()
        print(listlist)
        pid = int(listlist[0])
        print(pid)

        kill_cmd = "kill -9 {}\n".format(pid)
        invoke.send(kill_cmd)
        time.sleep(2)
        result = invoke.recv(4096).decode("utf-8")
        print(result)

    print("---------")
    invoke.send("ps -AT | grep sha\n")
    time.sleep(2)
    result = invoke.recv(4096).decode("utf-8")
    print(result)
    

    # stdin,stdout,stderr = ssh.exec_command('ls -l')      #调用远程执行命令方法exec_command()
    # print(stdout.read().decode('utf-8'))        #打印命令执行结果，得到Python列表形式，可以使用stdout_readlines()
    # ssh.close()

    # ------------------- download 
    cmd = "wget --no-check-certificate -O shadowsocks-all.sh https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-all.sh"
    invoke.send(cmd + '\n')
    time.sleep(2)
    result = invoke.recv(4096).decode("utf-8")
    print(result)

    cmd = "chmod +x shadowsocks-all.sh"
    invoke.send(cmd + '\n')
    time.sleep(2)
    result = invoke.recv(4096).decode("utf-8")
    print(result)


    cmd = "./shadowsocks-all.sh 2>&1 | tee shadowsocks-all.log"
    invoke.send(cmd + '\n')
    while (1):
        time.sleep(2)
        result = invoke.recv(4096).decode("utf-8")
        print(result)
        if ("Please enter a number" in result):
            break
    cmd = "3"
    invoke.send(cmd + "\n")
    while (1):
        time.sleep(2)
        result = invoke.recv(4096).decode("utf-8")
        print(result)
        if ("Please enter password" in result):
            break
    cmd = shadow_password
    invoke.send(cmd + '\n')
    while(1):
        time.sleep(2)
        result = invoke.recv(4096).decode("utf-8")
        print(result)
        if ("Please enter a port" in result):
            break
    cmd = "\n"
    invoke.send(cmd + '\n')
    while(1):
        time.sleep(2)
        result = invoke.recv(4096).decode("utf-8")
        print(result)
        if ("Which cipher you'd select" in result):
            break
    cmd = "aes-256-cfb"
    invoke.send(cmd + '\n')
    while (1):
        time.sleep(30)
        result = invoke.recv(4096).decode("utf-8")
        print(result)
        if ("Enjoy it!" in result):
            break

if __name__ == "__main__":
    main()