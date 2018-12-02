# coding=utf-8
import paramiko
import os

class SshConnect(object):
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._connect()

    def _connect(self):
        transport = paramiko.Transport((self._host, self._port))
        transport.connect(username=self._username, password=self._password)
        self._transport = transport

    # 下载
    def download(self, remotepath, localpath):

        # if not os.path.exists(localpath):
        #     os.mknod(localpath)

        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remotepath, localpath)

    # 上传
    def put(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localpath, remotepath)

    # 执行命令
    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            return str(data,encoding='utf8')
        err = stderr.read()
        if len(err) > 0:
            return err

    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()


# if __name__ == "__main__":

    # conn = SSHConnection('120.79.170.12', 22, 'root', '123123aA')
    # sftp = conn.download('/tmp/node_conf_10.121.143.1_云1_2.log', '../log_states/node_conf_10.121.143.1_云1_2.log')
    #
    # conn = SSHConnection('192.168.87.200', 22, 'username', 'password')
    # localpath = 'hello.txt'
    # remotepath = '/home/hupeng/WorkSpace/Python/test/hello.txt'
    # print 'downlaod start'
    # conn.download(remotepath, localpath)
    # print 'download end'
    # print 'put begin'
    # conn.put(localpath, remotepath)
    # print 'put end'
    #
    # conn.exec_command('whoami')
    # conn.exec_command('cd WorkSpace/Python/test;pwd')  #cd需要特别处理
    # conn.exec_command('pwd')
    # conn.exec_command('tree WorkSpace/Python/test')
    # conn.exec_command('ls -l')
    # conn.exec_command('echo "hello python" > python.txt')
    # conn.exec_command('ls hello')  #显示错误信息
    # conn.close()
