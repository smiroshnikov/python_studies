from fabric.api import env, run, local, execute, task
from fabric.operations import put
from fabric.context_managers import settings

env.hosts = ['192.168.1.167']  # Default remote host IP address. Overridden during deployment
env.user = 'root'  # Default VMs user name
env.password = 'root'  # Default VMs password
env.disable_known_hosts = True  # Accept new hosts without prompting to store key (for ssh)
env.no_keys = True
localpath = '/Users/sergei.miroshnikov/Desktop/C_code/brainstorm.c'
remotepath = '/home/debian/Desktop/scripts/brainstorm.c'


# port to Mac


@task
def run_command(ip, command):  # fab run_command:10.20.4.25,"ls -lorthx" - # works !
    """
    Run command on remote host
    :param ip: IP address of remote host
    :param command: Command text
    :return:
    """
    with settings(host_string=ip):  # overrides with "with"
        result = run(command, pty=False)
        return result.return_code


run_command(env.hosts[0], "ls -laorth /home/debian/Desktop/scripts")
run_command(env.hosts[0], "rm -f /home/debian/Desktop/scripts/brainstorm.c")


@task
def put_file(ip):
    with settings(host_string=ip):  # overrides with "with"
        put(local_path=localpath, remote_path=remotepath)


run_command(env.hosts[0], "ls -laorth /home/debian/Desktop/scripts")

put_file(env.hosts[0])

run_command(env.hosts[0], "ls -laorth /home/debian/Desktop/scripts")
