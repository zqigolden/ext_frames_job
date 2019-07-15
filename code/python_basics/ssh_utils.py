"""
Author: ykliu@aibee.com
Date: 2018/10/15 16:56
"""
import paramiko
from utils import Utils


class SSHUtils(object):
    def __init__(self, ip, user, pwd, port=22):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=user, password=pwd, port=port)

        self.ssh = ssh

        self.sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())

    def exe_cmd(self, cmd):
        Utils.log('ssh execute cmd: %s' % cmd)
        return self.ssh.exec_command(cmd)

    def get_sftp(self):
        return self.sftp

    def put(self, local_path, remote_path):
        self.sftp.mkdir()
        self.sftp.put(local_path, remote_path)
        Utils.log('put from %s to %s' % (local_path, remote_path))

    def destruct(self):
        self.ssh.close()
        self.sftp.close()

    def exists(self, file_path):
        command = 'find %s' % file_path
        stdin, stdout, stderr = self.exe_cmd(command)
        res_file = stdout.read().strip()
        res_file = res_file.decode()

        return res_file == file_path
