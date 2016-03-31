import string
import traceback
import uuid

from fabric.api import env, run, local, execute, task
from fabric.context_managers import settings
from fabric.contrib.files import exists
from fabric.network import disconnect_all
from fabric.operations import put, get
from ilogue.fexpect import expect, expecting, run as erun  # user for answer prompt question

env.hosts = ['10.20.4.228']  # Default remote host IP address. Overridden during deployment
env.user = 'root'  # Default VMs user name
env.password = '123456'  # Default VMs password
env.disable_known_hosts = True  # Accept new hosts without prompting to store key (for ssh)
env.no_keys = True


@task
def run_command(ip, command):  # fab run_command:10.20.4.25,"ls -lorthx" - # works !
    """
    Run command on remote host
    :param ip: IP address of remote host
    :param command: Command text
    :return:
    """
    with settings(host_string=ip):
        result = run(command, pty=False)
        return result.return_code
