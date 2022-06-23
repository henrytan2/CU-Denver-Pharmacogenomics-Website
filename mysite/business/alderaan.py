import paramiko
import os
import logging

error_logger = logging.getLogger('django.error')
info_logger = logging.getLogger('django.info')


class Alderaan:
    client = None

    def __init__(self):
        host = os.getenv('ALDERAAN_IP')
        username = os.getenv('ALDERAAN_USER')
        password = os.getenv('ALDERAAN_PASSWORD')
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, username=username, password=password)
        self.transport = paramiko.Transport((host, 22))
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def run_command(self, command):
        _stdin, _stdout, _stderr = self.client.exec_command(command)
        stdout = _stdout.read().decode()
        stderr = _stderr.read().decode()
        success = True
        if len(stderr) > 0:
            success = False
            error_logger.error(stderr)

        return stdout, success

    def send_batch(self, path, command):
        f = self.sftp.open(f'{path}', "wb")
        f.write(f'{command}')
        f.close()