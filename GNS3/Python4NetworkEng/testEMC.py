from fabric.api import env, run, local, execute, task
from fabric.context_managers import settings

# env.hosts = ['10.20.4.228']  # Default remote host IP address. Overridden during deployment
env.hosts = ['10.64.136.150']  # VD
env.user = 'sergeim'  # Default VMs user name
env.password = '******'  # Default VMs password
env.disable_known_hosts = True  # Accept new hosts without prompting to store key (for ssh)
env.no_keys = True


@task
def run_command(command, ip="10.64.136.150"):  # fab run_command:10.20.4.25,"ls -lorthx" - # works !
    """
    Run command on remote host
    :param ip: IP address of remote host
    :param command: Command text
    :return:
    """
    with settings(host_string=ip):
        result = run(command, pty=False)
        return result.return_code


run_command("uptime")
run_command("whoami")
run_command("cd /home/sergeim/Desktop/")
run_command("mkdir testRemote")
run_command("ls -lorth ")
