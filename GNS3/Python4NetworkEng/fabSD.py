import string
import traceback
import uuid

from fabric.api import env, run, local, execute, task
from fabric.context_managers import settings
from fabric.contrib.files import exists
from fabric.network import disconnect_all
from fabric.operations import put, get
from ilogue.fexpect import expect, expecting, run as erun  # user for answer prompt question

# Alexey
from UITests.CRUD.Create.CreateAccounts import CreateAccounts
from UITests.CRUD.Create.CreateSites import CreateSites, CreateCPEs_defense, CreateGREs_defense, CreateDFs_defense, \
    CreateCPEs_mssp
from UITests.CRUD.Create.CreateUsers import CreateUsers
from UITests.CRUD.Create.CreateAssets import CreateAssets_mssp, CreateAssets_defense
from UITests.CRUD.Delete.DeleteAccounts import DeleteAccounts
from UITests.CRUD.Delete.DeleteSites import DeleteSites, DeleteCPEs, DeleteGREs, DeleteDFs
from UITests.CRUD.Delete.DeleteUsers import DeleteUsers
from UITests.CRUD.Delete.DeleteAssets import DeleteAssets
from UITests.CRUD.Edit.EditAccounts import EditAccounts
from UITests.CRUD.Edit.EditSites import EditSites, EditCPEs_defense, EditGREs_defense, EditDFs_defense, EditCPEs_mssp
from UITests.CRUD.Edit.EditUsers import EditUsers
from UITests.CRUD.Edit.EditAssets import EditAssets_mssp, EditAssets_defense
from UITests.Features.SDK_API import SDK_API
from UITests.Features.Reports import ReportTemplates
from UITests.Features.SessionExpiration import SessionExpiration
from UITests.Common.SDCCLogin import Set_DB_IP, Set_PORTAL_IP

# Alexey
from EmailLibrary import *
from ReporterLibrary import ReporterLibrary
from VSphereClient import *
from Variables import *
from XenClient import *
from helpers import *

env.hosts = ['10.20.4.228']  # Default remote host IP address. Overidden during deployment
env.user = 'root'  # Default VMs user name
env.password = '123456'  # Default VMs password
env.disable_known_hosts = True  # Accept new hosts without prompting to store key (for ssh)
env.no_keys = True

GIT_USER = 'alexeyfren'
GIT_PASSWORD = 'A642275f'
GIT_LOCAL = '/root/sdcc_%s/' % ''.join(random.choice(string.ascii_letters) for i in range(6))
LOCAL_PATH = '/root/automation_finland/'
REPORT_PATH = LOCAL_PATH + 'Reports/'
LOG_PATH = LOCAL_PATH + 'logs/'
SC_CONF_PATH = LOCAL_PATH + 'sdcc_create_sc.conf'
SC_EMPTY_CONF_PATH = LOCAL_PATH + 'sdcc_create_sc_empty.conf'
BE_NAME = 'master'  # Back End default name
STORAGE = 'Local storage'  # XEN storage name

ESX_SERVER_1 = '10.20.4.201'
ESX_SERVER_2 = '10.20.4.233'
PF_SENSE_CLIENT_1 = '192.168.1.106'
PF_SENSE_CLIENT_2 = '192.168.2.6'
ESX_SERVER = ESX_SERVER_1  # ESX server IP address
GNS_SERVER = '10.20.4.200'  # GNS server IP address
XEN_SERVER = '10.20.4.231'  # XEN server IP address

VM_TEMPLATES = {'empty': 'ClearCentOS',
                'mssp_all_in_one': 'DeploymentTemplate_mssp_all_in_one',
                'defense_all_in_one': 'DeploymentTemplate_defense_all_in_one'}

server_list = {}
ha_server_list = {}
vmNames = []
recepient = ['alexeyf@securitydam.com', 'evgenyv@securitydam.com', 'alexd@securitydam.com', 'elig@securitydam.com']
start = time.time()


class Logger(object):
    """
    Wrapping stdout so that output will be displayed on screen and in log file simulatniously
    """

    def __init__(self, fileName):
        """
        :param fileName: create log file with defined name
        :return:
        """
        self.fileName = fileName
        self.terminal = sys.stdout
        self.curr_time = get_time()
        self.log = open(LOG_PATH + "%s__%s.log" % (self.fileName, self.curr_time), "a")
        self.flush = sys.stdout.flush

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.flush()

    def reset_log(self):
        self.log.close()
        self.log = open("%s__%s.log" % (self.fileName, get_time()), "a")

    def close(self):
        self.terminal.close()
        self.log.close()

    def __del__(self):
        sys.stdout = self.terminal
        self.log.flush()
        self.log.close()


# region Additional Tasks
@task
def get_free_ips():
    print 'Searching free IPs in range 10.20.4.1 - 10.20.4.200 ...'
    usedIPs = []

    arpclean = Popen('ip -s -s neigh flush all', shell=True, stdout=PIPE, stderr=PIPE)  # opens sub process
    arpclean.communicate()
    p = Popen('arp-scan --interface=eth0 10.20.4.1-10.20.4.200', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()  # need to import Popoen dependencies

    print '\nFree IPs are:'
    print '-------------'
    for line in out.split('\n'):  # parsing out taking only ip addresses
        if len(line.split()) > 2 and validIP(line.split()[0]):
            usedIPs.append(line.split()[0])

    for i in range(1, 200):
        ip = '10.20.4.' + str(i)
        if ip not in usedIPs:
            print ip  # cool


@task
def put_and_run(ip, script):  # no need for credentials defined in env above
    """
    Puts script from local host to remote host on /tmp and runs it
    :param ip: IP address of remote host
    :param script: Script path to run
    :return:
    """
    with settings(host_string=ip):
        tmp = script.split('/')
        scriptName = tmp[len(tmp) - 1]
        print 'Copying ' + scriptName + ' to: ' + ip + ' ...'
        put(script, '/tmp/' + scriptName, mode=0755)

        print 'Running ' + scriptName + ' on: ' + ip + ' ...'
        result = run('cd /tmp;./' + scriptName, pty=False)

        return result.return_code


@task
def put_file(ip, localFilePath, remoteDirectoryPath):
    """
    Puts file from local host to remote host
    :param ip: IP address of remote host
    :param localFilePath: Path to loval file
    :param remoteDirectoryPath: Path to remote directory
    """
    with settings(host_string=ip):
        tmp = localFilePath.split('/')
        fileName = tmp[len(tmp) - 1]
        print 'Copying file [' + fileName + '] to: ' + ip + ' ...'
        put(localFilePath, remoteDirectoryPath + fileName, mode=0755)


@task
def get_file(ip, remoteFilePath, localDirectoryPath='/tmp'):
    """
    Gets file from remote host to local host
    :param ip: IP address of remote host
    :param remoteFilePath: Path to remote file
    :param localDirectoryPath: Path to local directory
    """
    with settings(host_string=ip):  #
        tmp = remoteFilePath.split('/')
        fileName = tmp[len(tmp) - 1]
        print 'Copying file [' + fileName + '] from: ' + ip + ' to: ' + localDirectoryPath + ' ...'
        get(remoteFilePath, localDirectoryPath)


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


@task
def create_vms(vmName, vmCount=1, vmServer='xen', xen=XEN_SERVER, esx=ESX_SERVER, vmTemplate='empty'):
    """
    Creates virtual machines on XEN/ESX servers

    :param vmName:      Name of VM
    :param vmCount:     Count of VMs to create
    :param vmServer:    Server to create VMs (xen or esx)
    :param xen:         IP address of XEN server
    :param esx:         IP address of ESX server
    :param vmTemplate:  Template name (empty | mssp_all_in_one | defense_all_in_one)
    :return:
    """

    vmIPs = {}
    if vmServer == 'xen':
        global XEN_SERVER
        if xen != XEN_SERVER:
            XEN_SERVER = xen

        sys.stdout = Logger('create_vms_%s' % vmName)
        MINrequiredMemorySize = 768 * 1024 * 1024 * int(vmCount)
        xen = XenClient(ip=XEN_SERVER)
        availableMemory = xen.GetXenAvailableMemory()
        if availableMemory < MINrequiredMemorySize:
            print "XEN Server has " + str(availableMemory / 1024 / 1024) + " MB of RAM. Needed at least " + str(
                MINrequiredMemorySize / 1024 / 1024) + " MB free RAM.\n"
            print "Exiting task ..."
            xen.Disconect()
            return 1

        xen.Disconect()

        print '\nCreating %s VMs on XEN server %s ...\n' % (vmCount, XEN_SERVER)

        for index in range(0, int(vmCount)):
            vmIPs[index] = create_vm_xen(vmName, vmTemplate)

        print '\nFinished to create %s VMs on XEN server %s.\n' % (vmCount, XEN_SERVER)
    else:
        global ESX_SERVER
        if esx != ESX_SERVER:
            ESX_SERVER = esx

        print '\nCreating %s VMs on ESX server %s ...\n' % (vmCount, ESX_SERVER)

        for index in range(0, int(vmCount)):
            vmIPs[index] = create_vm_esx(vmName, vmTemplate)

        print '\nFinished to create %s VMs on ESX server %s.\n' % (vmCount, ESX_SERVER)

    print '\nIPs of created VMs are:\n'
    for index in range(0, int(vmCount)):
        print 'VM ' + str(index + 1) + ': ' + vmIPs[index]


@task
def create_scrubbing_center(ip, scName, conf=SC_CONF_PATH, beName=BE_NAME):
    """
    Creates and configures Scrubbing Center on existing SDCC server

    :param ip:      IP address of SDCC backend
    :param scName:  Name of Scrubbing Center
    :param conf:    SC config file path
    :param beName:  Name of backend
    """

    env.hosts = [ip]
    execute(create_sc, scName, conf, beName)


@task
def sdcc_stop(db, be, portal):
    print "Stopping SDCC ..."
    with settings(host_string=be):
        run('sdcc stop')

    print "Stopping DB ..."
    with settings(host_string=db):
        run('service mongod stop')
        run('chkconfig mongod off')

    print "Stopping Portal ..."
    with settings(host_string=portal):
        run('sdcc-portal stop')
        run('chkconfig nginx off')


# endregion


# region SDCC deployment - radware image
@task
def deploy_ova_image(branch='master', tag=None, esx=ESX_SERVER, threeNode=False):
    global ESX_SERVER
    if esx != ESX_SERVER:
        ESX_SERVER = esx

    global imageTag, vmNames

    if threeNode:
        # region Three node
        if not tag:
            tag = GetLatestTag('3node', branch)

        imageTag = tag

        print '\nDeploying three node SDCC image (branch: %s, tag: %s) to ESX server %s ...\n' % (
        branch, tag, ESX_SERVER)

        for role in ['be', 'db', 'fe']:
            ip = find_free_ip()
            if not ip:
                exit(1)

            imageName = 'rw-' + role + '-' + branch + '-' + tag + '.ova'
            imagePath = '/mnt/nfs/storage1/rw_images/3node/' + branch + '/' + tag + '/' + imageName
            vmName = 'SDCC-' + role + '-' + branch + '-' + tag + '-' + ip

            vmNames.append(vmName)

            local(
                '/usr/bin/ovftool --powerOn --network="NAT Network" --name=' + vmName + ' --datastore=datastore1 ' + imagePath + ' vi://root:\$ecurityd@m@' + ESX_SERVER)
            print 'VM name: %s, ip: %s.' % (vmName, ip)

            time.sleep(60)
            print '\nUpdating network configuration to static IP address.'
            esxSer = ESXClient(ip=ESX_SERVER)
            macAddr = esxSer.GetVMMAC(vmName)
            tempIP = FindIPAddressOfCreatedVM(macAddr)
            if tempIP:
                env.hosts = [tempIP]
            else:
                exit(1)

            execute(UpdateESXNetworkData, ip, 'eth0')
            time.sleep(3)
            with settings(host_string=env.hosts[0]):
                try:
                    run('service network restart', pty=False, warn_only=True, timeout=60)
                except:
                    print 'Service network restarted.'

            time.sleep(3)
            esxSer.ChangeVMNetworkLabel(vmName)
            time.sleep(3)
            esxSer.Disconect()

            if find_ip(macAddr) != ip:
                print 'Failed to update network configuration with new static IP.'
                exit(1)

            server_list[role] = ip

        env.hosts = [server_list['be']]
        # endregion
    else:
        # region Single node
        if not tag:
            tag = GetLatestTag('1node', branch)

        imageTag = tag

        print '\nDeploying single node SDCC image (%s, ver: %s) to ESX server %s ...\n' % (branch, tag, ESX_SERVER)
        ip = find_free_ip()
        if not ip:
            return 1

        imageName = 'rw-all-in-one-' + branch + '-' + tag + '.ova'
        imagePath = '/mnt/nfs/storage1/rw_images/1node/' + branch + '/' + tag + '/' + imageName
        vmName = 'SDCC-' + branch + '-' + tag + '-' + ip

        vmNames.append(vmName)

        local(
            '/usr/bin/ovftool --powerOn --network="NAT Network" --name=' + vmName + ' --datastore=datastore1 ' + imagePath + ' vi://root:\$ecurityd@m@' + ESX_SERVER)

        print '\nDeploying SDCC image finished successfully.'
        print 'VM name: %s, ip: %s.' % (vmName, ip)

        print 'Waiting to loading Centos ...'
        time.sleep(60)
        print '\nUpdating network configuration to static IP address.'
        esxSer = ESXClient(ip=ESX_SERVER)
        macAddr = esxSer.GetVMMAC(vmName)
        tempIP = FindIPAddressOfCreatedVM(macAddr)
        if tempIP:
            env.hosts = [tempIP]
        else:
            return 1

        execute(UpdateESXNetworkData, ip, 'eth0')
        time.sleep(3)
        with settings(host_string=env.hosts[0]):
            try:
                run('service network restart', pty=False, warn_only=True, timeout=60)
            except:
                print 'Service network restarted.'

        time.sleep(3)
        esxSer.ChangeVMNetworkLabel(vmName)
        time.sleep(3)
        esxSer.Disconect()

        if find_ip(macAddr) != ip:
            print 'Failed to update network configuration with new static IP.'
            return 1

        env.hosts = [ip]
        # endregion

    execute(UpdateServersINI, threeNode)
    execute(configure_email)
    print '\nDeploying SDCC image finished successfully.'
    return 0


# endregion


# region SDCC deployment - single node
@task
def full_deployment_sni(vmName='NewVM', branch='master', ip=None, content='sdcc', vmServer='xen', xen=XEN_SERVER,
                        esx=ESX_SERVER, RAM=1024, beName=BE_NAME, scName=None, scConf=SC_CONF_PATH,
                        services=DEFENSE_SERVICE, email=False):
    """
    Installs single node SDCC on created/existing VM

    :param vmName:   Name of VM
    :param branch:   SDCC Branch
    :param ip:       IP address of SDCC server. In this case, VM will not be created
    :param content:  Content to install on existing host (sdcc or all)
    :param vmServer: Server to create VM (xen or esx)
    :param xen:      IP address of XEN Serer
    :param esx:      IP address of ESX Serer
    :param RAM:      VM memory size
    :param beName:   Name of backend host
    :param scName:   Scrubbing center name, if None - Scrubbing center will not be created
    :param scConf:   Scrubbing center configuration file path
    :param services: Services to install
    :param email:    Whether to configure email settings or not
    """

    global XEN_SERVER  # will keep changed value and wont go back to default
    if xen != XEN_SERVER:
        XEN_SERVER = xen

    global ESX_SERVER
    if esx != ESX_SERVER:
        ESX_SERVER = esx

    global BE_NAME
    if beName != BE_NAME:
        BE_NAME = beName

    sys.stdout = Logger('full_deployment_sni_%s' % vmName)
    print "\nSDCC Deployment Details (1 node installation):"
    print "-----------------------------------------------"
    if ip is None:
        if vmServer == 'xen':
            print "Target (XEN): \t".expandtabs(8), XEN_SERVER  # string format
        else:
            print "Target (ESX): \t".expandtabs(8), ESX_SERVER
        print "VM name: \t".expandtabs(8), vmName
        print "VM RAM (MB): \t".expandtabs(8), RAM
    else:
        print "SDCC IP: \t".expandtabs(8), ip

    print "Branch: \t".expandtabs(8), branch
    print "BE name: \t".expandtabs(8), beName
    print "Service: \t".expandtabs(8), services
    if scName:
        print "SC name: \t".expandtabs(8), scName
    print "-----------------------------------------------"
    print "Installation will be start in 10 sec ..."
    print "if you want to abort, press ctrl^C now!"

    for i in xrange(10, 0, -1):  # waits to cancel install
        time.sleep(1)
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()  # clears buffer

    if services == MSSP_SERVICE:
        vmTemplate = 'mssp_all_in_one'
    elif services == DEFENSE_SERVICE:
        vmTemplate = 'defense_all_in_one'
    else:
        vmTemplate = 'empty'

    if ip is None:
        print '\n\nCreating VM for SDCC deployment ...\n'

        if vmServer == 'xen':
            MINrequiredMemorySize = int(RAM) * 1024 * 1024
            xen = XenClient(ip=XEN_SERVER)
            availableMemory = xen.GetXenAvailableMemory()
            if availableMemory < MINrequiredMemorySize:
                print "XEN Server has " + str(availableMemory / 1024 / 1024) + " MB of RAM. Needed about " + str(
                    RAM) + " MB free RAM to deploy SDCC installation.\n"
                print "Exiting deployment task ..."
                xen.Disconect()
                return 1

            vm_ip = create_vm_xen(vmName, vmTemplate)
            env.hosts = [vm_ip]

            if int(RAM) > 1024:
                if int(RAM) < 4097:
                    ramInBytes = int(RAM) * 1024 * 1024
                    xen.SetMemory(str(ramInBytes), currentVM)

            xen.Disconect()
        else:  # esx
            vm_ip = create_vm_esx(vmName, vmTemplate)
            env.hosts = [vm_ip]

        if vmTemplate == 'empty':
            content = 'all'
    else:
        env.hosts = [ip]

    if vmTemplate != 'empty' and not ip:
        update_mongod_config(env.hosts[0])

    print '\nSDCC installation started.\n'
    execute(clone_sdcc, branch)
    execute(create_answers, branch, services)
    execute(copy_remote_install_scripts, branch)
    execute(sdcc_install, branch, services, 'allin1', content)

    if scName:
        execute(create_sc, scName, scConf)

    execute(enable_modules)

    if email:
        execute(configure_email)

    print '\nSDCC installation finished.\n'
    print "SDCC-Portal IP: %s" % env.hosts[0]

    elapsed(start)

    try:
        sys.stdout.flush()
    except:
        pass

    return 0


# endregion


# region SDCC deployment - tree node
@task
def full_deployment_tni(vmName='NewVM', branch='master', db=None, be=None, portal=None, vmServer='xen', xen=XEN_SERVER,
                        esx=ESX_SERVER, beName=BE_NAME, scName=None, scConf=SC_CONF_PATH, services=DEFENSE_SERVICE,
                        email=False):
    """
    Installs three node SDCC on created/existing VMs

    :param vmName:   Name of VM
    :param branch:   SDCC branch
    :param db:       Database host IP address
    :param be:       Backend host IP address
    :param portal:   Portal host IP address
    :param vmServer: Server to create VM (xen or esx)
    :param xen:      XEN server IP address
    :param esx:      ESX server IP address
    :param beName:   Name of backend host
    :param scName:   Scrubbing center name, if None - SC will not be created
    :param scConf:   Scrubbing center configuration file path
    :param services: Services to install
    :param email:    Configures email settings, if true
    """

    sys.stdout = Logger('full_deployment_tni_%s' % vmName)
    MINrequiredMemorySize = 2048 * 1024 * 1024 * 3

    global XEN_SERVER
    if xen != XEN_SERVER:
        XEN_SERVER = xen

    global ESX_SERVER
    if esx != ESX_SERVER:
        ESX_SERVER = esx

    global BE_NAME
    if beName != BE_NAME:
        BE_NAME = beName

    print "\nSDCC Deployment Details (3 nodes installation):"
    print "--------------------------------------------------"
    if db is None and be is None and portal is None:
        if vmServer == 'xen':
            print "Target (XEN): \t".expandtabs(8), XEN_SERVER
        else:
            print "Target (ESX): \t".expandtabs(8), ESX_SERVER
        print "VM name: \t".expandtabs(8), vmName
    else:
        print "SDCC-DB IP: \t".expandtabs(8), db
        print "SDCC-BE IP: \t".expandtabs(8), be
        print "SDCC-Portal IP: ".expandtabs(8), portal

    print "Branch: \t".expandtabs(8), branch
    print "BE name: \t".expandtabs(8), beName
    print "Service: \t".expandtabs(8), services
    if scName:
        print "SC name: \t".expandtabs(8), scName
    print "----------------------------------------------------"
    print "Installation will be start in 10 sec ..."
    print "if you want to abort, press ctrl^C now!"

    for i in xrange(10, 0, -1):
        time.sleep(1)
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()

    if db is None or be is None or portal is None:  # Creates 3 VMs on xen server
        if vmServer == 'xen':
            xen = XenClient(ip=XEN_SERVER)
            availableMemory = xen.GetXenAvailableMemory()
            if availableMemory < MINrequiredMemorySize:
                print "XEN Server has " + str(
                    availableMemory / 1024 / 1024) + " MB of RAM. Needed a least 2.3 GB free RAM to deploy 3 node SDCC installation.\n"
                print "Exiting deployment task ..."
                xen.Disconect()
                exit(1)
            xen.Disconect()

            for role in ['be', 'db', 'fe']:
                print '\n\nCreating VM for: ' + role + ' ...\n'
                server_list[role] = create_vm_xen(vmName + '_[' + role.upper() + ']')
        else:
            for role in ['be', 'db', 'fe']:
                print '\n\nCreating VM for: ' + role + ' ...\n'
                server_list[role] = create_vm_esx(vmName + '_[' + role.upper() + ']')
    else:
        server_list['db'] = db
        server_list['be'] = be
        server_list['fe'] = portal

    print '\nSDCC installation started.\n'
    execute(clone_sdcc, branch)
    execute(create_answers, branch, services, tni=True)

    # Run SDCC-DB installation script
    env.hosts = [server_list['db']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_install, branch, services, 'database', 'pkgs')

    # Run SDCC-Core installation script
    env.hosts = [server_list['be']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_install, branch, services, 'backend', 'all', 'hybrid')

    # Run SDCC-Portal installation script
    env.hosts = [server_list['fe']]
    execute(copy_remote_install_scripts, branch)
    execute(sdcc_install, branch, services, 'portal', 'all')

    # Run Post installation action (copy sdcc.conf file from the back-end to portal machine and restart the service)
    print "\nRunning post installation action ...\n"
    prompts = expect(r'Are you sure you want to continue connecting (yes/no)?', 'yes')
    prompts += expect(r'password:', env.password)
    with settings(host_string=server_list['fe']):
        with expecting(prompts):
            erun('scp root@%s:/etc/sdcc/sdcc.conf  /etc/sdcc/' % server_list['be'])
        run('chown -R sdcc:sdcc /etc/sdcc; sdcc-portal restart')

    if scName:
        env.hosts = [server_list['be']]
        execute(create_sc, scName, scConf)

    env.hosts = [server_list['be']]
    execute(enable_modules)

    if email:
        execute(configure_email)

    print '\nSDCC installation finished.\n'
    print "SDCC-DB IP:".expandtabs(8), server_list['db']
    print "SDCC-BE IP:".expandtabs(8), server_list['be']
    print "SDCC-FE IP:".expandtabs(8), server_list['fe']

    elapsed(start)
    try:
        sys.stdout.flush()
    except:
        pass


# endregion


# region SDCC deployment - high availability
@task
def full_deployment_hai(vmName, branch='master', scName=None, scConf=SC_CONF_PATH, vmServer='xen', xen=XEN_SERVER,
                        esx=ESX_SERVER, beName=BE_NAME, services=DEFENSE_SERVICE):
    """
    Installs high availability SDCC on created VMs

    :param vmName:   Name of VM
    :param branch:   SDCC branch
    :param scName:   Scrubbing center name, if None - SC will not be created
    :param scConf:   Scrubbing center configuration file path
    :param vmServer: Server to create VM (xen or esx)
    :param xen:      XEN server IP address
    :param esx:      ESX server IP address
    :param beName:   Name of backend host
    :param services: Services to install
    """

    sys.stdout = Logger('full_deployment_hai_%s' % vmName)
    MINrequiredMemorySize = 1024 * 1024 * 1024 * 7

    global XEN_SERVER
    if xen != XEN_SERVER:
        XEN_SERVER = xen

    global ESX_SERVER
    if esx != ESX_SERVER:
        ESX_SERVER = esx

    global BE_NAME
    if beName != BE_NAME:
        BE_NAME = beName

    print "\nSDCC Setup Details (High availability installation):"
    print "------------------------------------------"
    if vmServer == 'xen':
        print "Target (XEN): \t".expandtabs(8), XEN_SERVER
    else:
        print "Target (ESX): \t".expandtabs(8), ESX_SERVER
    print "VM name: \t".expandtabs(8), vmName
    print "Branch: \t".expandtabs(8), branch
    print "BE name: \t".expandtabs(8), beName
    print "Service: \t".expandtabs(8), services
    if scName:
        print "SC name: \t".expandtabs(8), scName
    print "------------------------------------------"
    print "Installation will be start in 10 sec ..."
    print "if you want to abort, press ctrl^C now!"

    for i in xrange(10, 0, -1):
        time.sleep(1)
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()

    # region Creating VMs
    if vmServer == 'xen':
        xen = XenClient(ip=XEN_SERVER)
        availableMemory = xen.GetXenAvailableMemory()
        if availableMemory < MINrequiredMemorySize:
            print "XEN Server has " + str(
                availableMemory / 1024 / 1024) + " MB of RAM. Needed a least 5.4 GB free RAM to deploy high availability SDCC installation.\n"
            print "Exiting deployment task ..."
            xen.Disconect()
            exit(1)
        xen.Disconect()

        for role in ['be', 'db', 'fe', 'be_sec', 'db_sec', 'fe_sec', 'db_arb']:
            print '\n\nCreating VM for: ' + role + ' ...\n'
            ha_server_list[role] = create_vm_xen(vmName + '_[' + role.upper() + ']')
    else:
        for role in ['be', 'db', 'fe', 'be_sec', 'db_sec', 'fe_sec', 'db_arb']:
            print '\n\nCreating VM for: ' + role + ' ...\n'
            ha_server_list[role] = create_vm_esx(vmName + '_[' + role.upper() + ']')
    # endregion

    # region Installing SDCC
    print '\nSDCC installation started.\n'

    execute(clone_sdcc, branch)

    print '\n----------- Three node set 1 ------------\n'
    server_list['db'] = ha_server_list['db']
    server_list['be'] = ha_server_list['be']
    server_list['fe'] = ha_server_list['fe']
    execute(create_answers, branch, services, tni=True)

    # Run SDCC-DB installation script (Primary DB)
    env.hosts = [ha_server_list['db']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_install, branch, services, 'database', 'pkgs')

    # Run SDCC-Core installation script (Primary BE)
    env.hosts = [ha_server_list['be']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_install, branch, services, 'backend', 'all', 'hybrid')

    # Run SDCC-Portal installation script (Primary FE)
    env.hosts = [ha_server_list['fe']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_install, branch, services, 'portal', 'all')

    print '\n----------- Three node set 2 ------------\n'

    server_list['db'] = ha_server_list['db_sec']
    server_list['be'] = ha_server_list['be_sec']
    server_list['fe'] = ha_server_list['fe_sec']
    execute(create_answers, branch, services, tni=True)

    # Run SDCC-DB installation script (Secondary DB)
    env.hosts = [ha_server_list['db_sec']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_install, branch, services, 'database', 'pkgs')

    # Run SDCC-Core installation script (Secondary BE)
    env.hosts = [ha_server_list['be_sec']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_install, branch, services, 'backend', 'all', 'hybrid')

    # Run SDCC-Portal installation script (Secondary FE)
    env.hosts = [ha_server_list['fe_sec']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_install, branch, services, 'portal', 'all')

    print '\n----------- Additional DB ------------\n'

    # Run SDCC-DB installation script (Arbiter DB)
    env.hosts = [ha_server_list['db_arb']]
    execute(copy_remote_install_scripts, branch, True)
    execute(sdcc_install, branch, services, 'database', 'pkgs')
    # endregion

    # region Running post installation action (copy sdcc.conf file from the back-end to portal machine and restart the service)
    print "\nRunning post installation action ...\n"  # uses pexpect
    prompts = expect(r'Are you sure you want to continue connecting (yes/no)?', 'yes')
    prompts += expect(r'password:', env.password)
    with settings(host_string=ha_server_list['fe']):
        with expecting(prompts):
            erun('scp root@%s:/etc/sdcc/sdcc.conf  /etc/sdcc/' % ha_server_list['be'])  # expected run
        run('chown -R sdcc:sdcc /etc/sdcc; sdcc-portal restart')

    with settings(host_string=ha_server_list['fe_sec']):
        with expecting(prompts):
            erun('scp root@%s:/etc/sdcc/sdcc.conf  /etc/sdcc/' % ha_server_list['be_sec'])
        run('chown -R sdcc:sdcc /etc/sdcc; sdcc-portal restart')
    # endregion

    # region Creating Scrubbing Center
    if scName:
        env.hosts = [ha_server_list['be']]
        execute(create_sc, scName, scConf)

        env.hosts = [ha_server_list['be_sec']]
        execute(create_sc, scName, scConf)
    # endregion

    # region Enabling Modules
    env.hosts = [ha_server_list['be']]
    execute(enable_modules)

    env.hosts = [ha_server_list['be_sec']]
    execute(enable_modules)
    # endregion

    # region Running replica and cluster scripts
    with settings(host_string=ha_server_list['be_sec']):
        run('sdcc stop')

    with settings(host_string=ha_server_list['fe_sec']):
        run('sdcc-portal stop')

    # Run replica_installation script
    env.hosts = [ha_server_list['be']]
    execute(replica_installation)

    # Run sdcc_build_two_nodes_cluster script for BE
    print 'Searching free Virtual IP for BE cluster ...'
    be_vip = find_free_ip()
    if not be_vip:
        exit(1)

    env.hosts = [ha_server_list['be']]
    execute(sdcc_build_two_nodes_cluster, 'backend', be_vip)

    # Run sdcc_build_two_nodes_cluster script for FE
    print 'Searching free Virtual IP for FE cluster ...'
    fe_vip = find_free_ip()
    if not fe_vip:
        exit(1)

    env.hosts = [ha_server_list['fe']]
    execute(sdcc_build_two_nodes_cluster, 'portal', fe_vip)
    # endregion

    print '\nSDCC installation finished.\n'
    print "SDCC-DB-PRIMARY IP:".expandtabs(8), ha_server_list['db']
    print "SDCC-BE-PRIMARY IP:".expandtabs(8), ha_server_list['be']
    print "SDCC-FE-PRIMARY IP:".expandtabs(8), ha_server_list['fe']
    print "SDCC-DB-SECONDARY IP:".expandtabs(8), ha_server_list['db_sec']
    print "SDCC-BE-SECONDARY IP:".expandtabs(8), ha_server_list['be_sec']
    print "SDCC-FE-SECONDARY IP:".expandtabs(8), ha_server_list['fe_sec']
    print "SDCC-DB-ARBITER IP:".expandtabs(8), ha_server_list['db_arb']
    print "SDCC-BE VIRTUAL IP:".expandtabs(8), be_vip
    print "SDCC-FE VIRTUAL IP:".expandtabs(8), fe_vip

    elapsed(start)
    try:
        sys.stdout.flush()
    except:
        pass


def replica_installation():
    # Runs replica_installation.sh script on BE

    print "\nRunning replica_installation.sh script ...\n"
    with settings(warn_only=True):  # setting "warn_only" so that script continue to run
        ret = run('/root/replica_installation.sh -P %s -S %s -A %s' % (
        ha_server_list['db'], ha_server_list['db_sec'], ha_server_list['db_arb']), pty=False)

        if ret.return_code != 0:
            sys.stdout.flush()
            raise Exception("\nreplica_installation.sh script failed.\n")
        else:
            print "\nreplica_installation.sh script finished successfully.\n"
            pass


def sdcc_build_two_nodes_cluster(hostType, virtualIP):
    # Run sdcc_build_two_nodes_cluster.sh script on BE/FE

    print "\nRunning sdcc_build_two_nodes_cluster.sh script ...\n"

    if hostType == 'backend':
        primaryIP = ha_server_list['be']
        secondaryIP = ha_server_list['be_sec']
    else:
        primaryIP = ha_server_list['fe']
        secondaryIP = ha_server_list['fe_sec']

    with settings(warn_only=True):  # setting "warn_only" so that script continue to run
        ret = run('/root/sdcc_build_two_nodes_cluster.sh -T %s -P %s -S %s -V %s' % (
        hostType, primaryIP, secondaryIP, virtualIP), pty=False)

        if ret.return_code != 0:
            sys.stdout.flush()
            raise Exception("\nsdcc_build_two_nodes_cluster.sh failed.\n")
        else:
            print "\nsdcc_build_two_nodes_cluster.sh finished successfully.\n"
            pass


# endregion


# region SDCC deployment - help methods
def clone_sdcc(branch="master"):  # cloning GIT sdcc GIT repository (defult is master)
    if file_exist():
        print "Removing old folder %s" % GIT_LOCAL
        os.popen('rm -rf %s' % GIT_LOCAL)  # removes old folder if exist

    local("git clone https://%s:%s@github.com/SecurityDam/sdcc.git -b %s %s" % (
    GIT_USER, GIT_PASSWORD, branch, GIT_LOCAL))


def copy_remote_install_scripts(branch, removeGITfolder=True):
    """
    Copying answers.txt and sdcc-get-install-scripts to remote host
    Delete  answers.txt if exist

    :param removeGITfolder:
    :param branch:
    """

    put('%sinstall/scripts/get-sdcc' % GIT_LOCAL, '/root/get-sdcc', mode=0755)
    run('~/get-sdcc %s' % branch)  # run sdcc script on remote machine

    if exists('~/answers.txt'):  # deletes old answers file if exist
        run('rm answers.txt')
    put('answers.txt',
        '~/')  # puts new created answers.txt in remote vm root folder (to be used by sdcc silent installation)

    if removeGITfolder:
        print "Removing GIT folder %s ..." % GIT_LOCAL

        try:
            os.popen('rm -rf %s' % GIT_LOCAL)
        except:
            pass


def create_answers(branch, services="defense-pipe", tni=False):
    if os.path.isfile('answers.txt'):
        print "Removing existing answers.txt file ..."
        local('rm answers.txt')

    with open('answers.txt', 'w') as fid:

        db_server = env.hosts[0]
        be_server = env.hosts[0]
        fe_server = env.hosts[0]

        if tni:
            db_server = server_list['db']
            be_server = server_list['be']
            fe_server = server_list['fe']

        fid.write('export DB_SERVER=%s\n' % db_server)
        fid.write('export DB_SSH_USER=%s\n' % env.user)
        fid.write('export DB_SSH_PASSWD=%s\n' % env.password)
        fid.write('export DB_SSH_PORT=%s\n\n' % '22')

        fid.write('export DB_NAME=sdcc\n')
        fid.write('export DB_PORT=27017\n')
        fid.write('export DB_USER=\n')
        fid.write('export DB_PASSWD=\n')
        fid.write('export DB_SERVER_SYSCHK=%s\n\n' % db_server)

        fid.write('export PORTAL_SERVER=%s\n' % fe_server)
        fid.write('export PORTAL_USER=%s\n' % env.user)
        fid.write('export PORTAL_PASSWD=%s\n\n' % env.password)

        fid.write('export BE_IP=%s\n' % be_server)
        fid.write('export BE_NAME=%s\n' % BE_NAME)
        fid.write('export BE_SSH_USER=%s\n' % env.user)
        fid.write('export BE_SSH_PASSWD=%s\n\n' % env.password)

        fid.write('export github_user=%s\n' % GIT_USER)
        fid.write('export github_password=%s\n' % GIT_PASSWORD)
        fid.write('export TAG=%s\n' % branch)
        fid.write('export START_SCRIPT=yes\n')
        fid.write('export IS_CONF_DB=no\n\n')

        fid.write('export IS_CONF_EMAIL=no\n')
        fid.write('export SMTP_SERVER=\n')
        fid.write('export SMTP_PORT=\n')
        fid.write('export SMTP_USER=\n')
        fid.write('export SMTP_PASSWD=\n\n')

        fid.write('export RETRANSMIT_AMOUNT=\n')
        fid.write('export SENDER_EMAIL_ADDRESS=\n')
        fid.write('export RECIPIENT_EMAIL_ADDRESS=\n\n')

        if services:
            fid.write('export SERVICES_TO_INSTALL="%s"\n' % services)


def set_persistent_route():
    """
    Set persistent route to remote vm
    :return:
    """
    with open(LOCAL_PATH + 'route-eth0', 'w') as fid:
        fid.write('10.20.4.0/24 dev eth0\n')
        fid.write('default via 10.20.4.254\n')
        fid.write('172.20.10.0/24 via %s\n' % GNS_SERVER)
        fid.write('172.21.0.0/16 via %s\n' % GNS_SERVER)
        fid.write('172.22.0.0/16 via %s\n' % GNS_SERVER)
    res = put(LOCAL_PATH + 'route-eth0', '/etc/sysconfig/network-scripts/route-eth0', mode=0755, use_sudo=True)
    run('/etc/init.d/network restart')
    if res.failed:
        raise Exception("Failed to configure persistant route.")


def enable_modules():
    print "Activating SDCC modules ..."

    eth = run("ifconfig -a | sed 's/[ \t].*//;/^\(lo\|\)$/d'")
    print 'Active interface is: ' + eth

    prompts = expect(r'Are you sure to proceed.*', 'yes')
    with expecting(prompts):
        erun('sdcc-manage-module -a activate -i ' + eth + ' -m all', pty=True)
    with settings(warn_only=True):
        for i in range(2):
            run('initctl emit sdcc-stop')
            time.sleep(2)
        run('initctl emit sdcc-start')


def list_branch(remote='https://%s:%s@github.com/SecurityDam/sdcc.git' % (GIT_USER, GIT_PASSWORD), display=True):
    """
    Gets available branches from GIT

    :param remote:  SDCC path on GIT
    :param display:
    :return:        List of available branches
    """
    with settings(warn_only=True):  # task continues even if failed (set by "warn_only" setting)
        branch_list = []
        ret = local('git ls-remote --heads %s' % remote, capture=True)
        try:
            for branch in ret.split('\n'):
                tmpBranch = branch.rsplit('/', 1)[1]
                if display:
                    print tmpBranch
                branch_list.append(tmpBranch)
            return branch_list  # returns branch list to calling function
        except:
            return False


def check_branch_exists(branch):
    ret = execute(list_branch, display=False)
    for key, val in ret.items():
        if branch not in val:
            print "Branch: ", branch
            print "\nWrong Branch, available branches are:"
            fmtcols(val, 3)
            sys.exit(1)
    return


def file_exist(tmp=GIT_LOCAL):
    if os.path.exists(tmp):
        print "Path Exist."
        return True
    else:
        print "File %s not exist." % tmp
        return False


def configure_email():
    print 'Configuring email settings for user: %s ...' % EMAIL_USER
    if os.path.isfile('email.conf'):
        print "Removing existing email.conf file ..."
        local('rm email.conf')

    with open('email.conf', 'w') as fid:
        fid.write('{\n')
        fid.write('    "retries": 5,\n')
        fid.write('    "smtp_host": "localhost",\n')
        fid.write('    "smtp_port": 25,\n')
        fid.write('    "user": "",\n')
        fid.write('    "password": "",\n')
        fid.write('    "from": "alerts@securitydam.com",\n')
        fid.write('    "to": "%s@localhost"\n' % EMAIL_USER)
        fid.write('}\n')

    put('email.conf', '/etc/sdcc/email.conf', mode=0600)

    prompts = expect(r'are you sure to override?.*', 'y')
    with expecting(prompts):
        run('sdcc-config-email -c /etc/sdcc/email.conf -f')

    run('sdcc restart')
    run('adduser ' + EMAIL_USER)


def create_sc(name, sc_conf_file=SC_CONF_PATH, backend=None):
    print "\nCreating Scrubbing Center: " + name + " according to: " + sc_conf_file + " ...\n"
    edit_sc(sc_conf_file, 1, '\t%s:\n'.expandtabs(4) % name)
    put(sc_conf_file, '/root/sdcc_create_sc.conf', mode=0755)
    time.sleep(2)

    if not backend:
        backend = BE_NAME

    with settings(warn_only=True):
        result = run('sdcc-create-sc -c %s -b %s' % ('/root/sdcc_create_sc.conf', backend))
        if result.return_code == 0:
            pass

    if sc_conf_file == LOCAL_PATH + 'sdcc_create_sc_gns3.conf':
        execute(set_persistent_route)


def sdcc_install(branch, services, target, content, role=''):
    with settings(warn_only=True):
        if role == '':
            ret = run(
                '/root/sdcc-install -c install -b %s -sv %s -tg %s -ty %s -s' % (branch, services, target, content),
                pty=False)
        else:
            ret = run('/root/sdcc-install -c install -b %s -sv %s -tg %s -ty %s -r %s -s' % (
            branch, services, target, content, role), pty=False)

        if ret.return_code != 0:
            sys.stdout.flush()
            raise Exception("SDCC installation failed.")
        else:
            print "SDCC installation finished successfully."
            pass


def sdcc_update(branch, services, target, content):
    with settings(warn_only=True):
        prompts = expect(r'Your choice.*', '1')
        with expecting(prompts):
            if content == 'pkgs' and services:
                ret = run(
                    '/root/sdcc-install -c upgrade -b %s -sv %s -tg %s -ty %s -s' % (branch, services, target, content),
                    pty=False)
            else:
                ret = run('/root/sdcc-install -c upgrade -b %s -tg %s -ty %s -s' % (branch, target, content), pty=False)

            if ret.return_code != 0:
                sys.stdout.flush()
                raise Exception("SDCC upgrade failed.")
            else:
                print "SDCC upgrade finished successfully."
                pass


def update_mongod_config(ip):
    print 'Updating mongod.conf with host IP address %s ...' % ip
    with settings(host_string=ip):
        get('/etc/mongod.conf', '/root/mongod.conf')
        replace('/root/mongod.conf', "bind_ip=127.0.0.1,", "bind_ip=127.0.0.1," + ip)
        put('/root/mongod.conf', '/etc/mongod.conf', mode=0755, use_sudo=True)
        local('rm /root/mongod.conf')

        run('service mongod restart')


# endregion


# region SDCC upgrade
@task
def sdcc_upgrade_sni(branch, ip, services=None, content='sdcc'):
    """
    Upgrades single node SDCC on VM

    :param branch:   SDCC branch
    :param ip:       IP address of SDCC server
    :param services: Services to upgrade
    :param content:  Content to upgrade (sdcc or all)
    """

    sys.stdout = Logger('sdcc_upgrade_sni_%s' % branch)
    print '\nSDCC upgrade started.\n'
    env.hosts = [ip]

    if content != 'pkgs':
        services = None

    execute(clone_sdcc, branch)
    execute(create_answers, branch, services)
    execute(copy_remote_install_scripts, branch)
    execute(sdcc_update, branch, services, 'allin1', content)


@task
def sdcc_upgrade_tni(branch, be, db, fe, services=None, content='sdcc'):
    """
    Upgrades three node SDCC on VMs

    :param branch:   SDCC branch
    :param be:       IP address of BE
    :param db:       IP address of DB
    :param fe:       IP address of FE
    :param services: Services to upgrade
    :param content:  Content to upgrade (sdcc or all)
    """

    sys.stdout = Logger('sdcc_upgrade_tni_%s' % branch)

    server_list['be'] = be
    server_list['db'] = db
    server_list['fe'] = fe

    if content != 'pkgs':
        services = None

    env.hosts = [be]

    execute(clone_sdcc, branch)
    execute(create_answers, branch, services, tni=True)

    # Upgrade BE
    env.hosts = [server_list['be']]
    execute(copy_remote_install_scripts, branch, False)
    execute(sdcc_update, branch, services, 'backend', content)

    # Upgrade FE
    env.hosts = [server_list['fe']]
    execute(copy_remote_install_scripts, branch, True)
    execute(sdcc_update, branch, services, 'portal', content)


# endregion


# region SDCC uninstall
@task
def sdcc_uninstall_sni(ip):
    """
    Removes single node SDCC from VM

    :param ip: IP address of SDCC server
    """

    print "\nSDCC uninstall started.\n"

    with settings(host_string=ip):
        prompts = expect(r'Enter an IP address of the database server.*', ip)
        prompts += expect(r'Enter a username for accessing.*', env.user)
        prompts += expect(r'Enter password for.*', env.password)
        prompts += expect(r'Enter an IP address of the Portal.*', ip)
        prompts += expect(r'Do you want to uninstall SDCC.*', 'yes')
        with expecting(prompts):
            erun('sdcc-cleanup')


@task
def sdcc_uninstall_tni(be, db, fe):
    """
    Removes three node SDCC from VM

    :param be:   IP address of BE
    :param db:   IP address of DB
    :param fe:   IP address of FE
    """

    print "\nSDCC uninstall started.\n"

    with settings(host_string=be):
        prompts = expect(r'Enter an IP address of the database server.*', db)
        prompts += expect(r'Enter a username for accessing.*', env.user)
        prompts += expect(r'Enter password for.*', env.password)
        prompts += expect(r'Enter an IP address of the Portal.*', fe)
        prompts += expect(r'Do you want to uninstall.*', 'yes')
        with expecting(prompts):
            erun('sdcc-cleanup')


# endregion


# region XEN methods
def deploy_template(vmName, vmTemplate):
    """
    Deploy VM from Template

    :param vmName: the VM desired name
    :param vmTemplate: xen template to be used (must be pre-configured in xen server)
    :return:
    """

    global currentVM, server_list, template_mac

    xen = XenClient(ip=XEN_SERVER)
    storage = xen.GetXenStorageName()

    if vmName in xen.ListVM():
        raise Exception("VM with this name already exist. (%s)" % vmName)

    template_mac = xen.GetTemplateMAC('', template_name=vmTemplate)

    currentVM = xen.CreateNewVM(vmName, vmTemplate, storage)
    xen.Disconect()

    for tries in range(2):
        ip = find_ip(template_mac)  # Finds IP of created VM from a given MAC Address

        if ip:
            env.hosts = [ip]
            disconnect_all()
            return
        else:
            xen = XenClient(ip=XEN_SERVER)
            xen.RebootVM(False, currentVM)
            xen.Disconect()

    sys.stdout.flush()
    print 'Failed to find new VM IP.'
    xen = XenClient(ip=XEN_SERVER)
    xen.RemoveVM(currentVM)
    xen.Disconect()
    exit(1)


def update_network_config(ip):
    global new_mac
    new_mac = randomMAC()
    print 'Updating ifcfg-eth0 file with the following data:\n'
    print 'HWADDR=' + new_mac + ' (new generated MAC)'
    print 'IPADDR=' + ip
    print 'NETMASK=255.255.255.0'
    print 'GATEWAY=10.20.4.254'
    print ''

    tmpFile = str(uuid.uuid1())[:8]

    with open('/root/%s' % tmpFile, 'w') as fid:
        fid.write('DEVICE=eth0\n')
        fid.write('BOOTPROTO=static\n')
        fid.write('HWADDR=%s\n' % new_mac)
        fid.write('ONBOOT=yes\n')
        fid.write('TYPE=Ethernet\n')
        fid.write('IPADDR=%s\n' % ip)
        fid.write('NETMASK=255.255.255.0\n')
        fid.write('GATEWAY=10.20.4.254')

    put('/root/%s' % tmpFile, '/etc/sysconfig/network-scripts/ifcfg-eth0', mode=0755, use_sudo=True)
    local('rm /root/%s' % tmpFile)


def update_mac(currVM):
    print "Changing VM MAC to: ", new_mac
    xen = XenClient(ip=XEN_SERVER)
    vif_uuid = xen.GetVifUUID(currVM)
    net_uuid = xen.GetInterface(XEN_BRIDGE)
    xen.StopVM(currVM)
    xen.DestroyVif(vif_uuid)
    xen.SetInterface(currVM, net_uuid, new_mac)
    xen.StartVM(currVM)
    xen.Disconect()

    for tries in range(2):
        ip = find_ip(new_mac)

        if ip:
            env.hosts = [ip]
            disconnect_all()
            return
        else:
            xen = XenClient(ip=XEN_SERVER)
            xen.RebootVM(False, currentVM)
            xen.Disconect()

    sys.stdout.flush()

    print 'New MAC was not found. Removing created VM.'
    xen = XenClient(ip=XEN_SERVER)
    xen.RemoveVM(currVM)
    xen.Disconect()

    raise Exception("Failed to obtain IP for VM.")


def create_vm_xen(vmName, vmTemplate='empty'):
    global vmNames
    ip = find_free_ip()
    if not ip:
        exit(1)

    vmName = vmName + '_' + ip

    execute(deploy_template, vmName, VM_TEMPLATES[vmTemplate])
    execute(update_network_config, ip)
    execute(update_mac, currentVM)

    vmNames.append(currentVM)
    disconnect_all()
    return ip


# endregion


# region ESX methods
def create_vm_esx(vmName, vmTemplate='empty'):
    global vmNames
    ip = find_free_ip()
    if not ip:
        exit(1)

    imagePath = '/root/VMTemplates/' + VM_TEMPLATES[vmTemplate] + '.ova'
    vmName = vmName + '_' + ip
    vmNames.append(vmName)

    local(
        '/usr/bin/ovftool --powerOn --network="NAT Network" --name=' + vmName + ' --datastore=datastore1 ' + imagePath + ' vi://root:\$ecurityd@m@' + ESX_SERVER)

    print '\nCreating VM finished successfully.'
    print 'VM name: %s, ip: %s.' % (vmName, ip)
    time.sleep(30)

    print '\nUpdating network configuration to static IP address.'
    esxSer = ESXClient(ip=ESX_SERVER)
    macAddr = esxSer.GetVMMAC(vmName)
    tempIP = FindIPAddressOfCreatedVM(macAddr)
    if tempIP:
        env.hosts = [tempIP]
    else:
        exit(1)

    with settings(host_string=env.hosts[0]):
        eth = run("ifconfig -a | sed 's/[ \t].*//;/^\(lo\|\)$/d'")

    execute(UpdateESXNetworkData, ip, eth)
    with settings(host_string=env.hosts[0]):
        try:
            run('service network restart', pty=False, warn_only=True, timeout=60)
        except:
            print 'Service network restarted.'

    esxSer.ChangeVMNetworkLabel(vmName)
    esxSer.Disconect()

    if find_ip(macAddr) != ip:
        print 'Failed to update network configuration with new static IP.'
        exit(1)

    return ip


def FindIPAddressOfCreatedVM(mac):
    for attempt in range(20):
        print "Searching VM with MAC: %s." % mac

        if ESX_SERVER == ESX_SERVER_1:
            with settings(host_string=PF_SENSE_CLIENT_1):
                run('ip -s -s neigh flush all')
                out = run('arp-scan --interface=eth0 192.168.1.2-192.168.1.254')
        else:
            with settings(host_string=PF_SENSE_CLIENT_2):
                run('ip -s -s neigh flush all')
                out = run('arp-scan --interface=eth1 192.168.2.2-192.168.2.254')

        for line in out.split('\n'):
            if mac.lower() in line.lower():
                print "\nMAC is found. IP address of VM is: " + line.split()[0]
                return line.split()[0]

        time.sleep(30)

    print "IP of VM is not found."
    return None


def UpdateESXNetworkData(ip, eth):
    tmpFile = str(uuid.uuid1())[:8]
    print 'Getting ifcfg-' + eth + ' from created VM ...'
    get('/etc/sysconfig/network-scripts/ifcfg-' + eth, '~/%s' % tmpFile)

    local('chmod 755 ~/%s' % tmpFile)
    add_ip('/root/%s' % tmpFile, ip)
    add_dns('/root/%s' % tmpFile)
    replace('/root/%s' % tmpFile, "BOOTPROTO=dhcp", "BOOTPROTO=static")

    put('/root/%s' % tmpFile, '/etc/sysconfig/network-scripts/ifcfg-' + eth, mode=0755, use_sudo=True)
    local('rm /root/%s' % tmpFile)


def UpdateServersINI(threeNode=False):
    print 'Updating servers.ini ...'
    tmpFile = str(uuid.uuid1())[:8]

    if threeNode:
        file_handle = open('/root/%s' % tmpFile, 'w')
        file_handle.write('[singlenode]\n')
        file_handle.write('single ansible_ssh_host=0.0.0.0 ansible_ssh_user=root ansible_ssh_pass=password\n\n')
        file_handle.write('[triplenode]\n')
        file_handle.write('db ansible_ssh_host=' + server_list[
            'db'] + ' ansible_ssh_user=' + env.user + ' ansible_ssh_pass=' + env.password + '\n')
        file_handle.write('be ansible_ssh_host=' + server_list[
            'be'] + ' ansible_ssh_user=' + env.user + ' ansible_ssh_pass=' + env.password + '\n')
        file_handle.write('fe ansible_ssh_host=' + server_list[
            'fe'] + ' ansible_ssh_user=' + env.user + ' ansible_ssh_pass=' + env.password)
        file_handle.close()
    else:
        file_handle = open('/root/%s' % tmpFile, 'w')
        file_handle.write('[singlenode]\n')
        file_handle.write('single ansible_ssh_host=%s ansible_ssh_user=%s ansible_ssh_pass=%s\n\n' % (
        env.hosts[0], env.user, env.password))
        file_handle.write('[triplenode]\n')
        file_handle.write('db ansible_ssh_host=0.0.0.0 ansible_ssh_user=root ansible_ssh_pass=password\n')
        file_handle.write('be ansible_ssh_host=0.0.0.0 ansible_ssh_user=root ansible_ssh_pass=password\n')
        file_handle.write('fe ansible_ssh_host=0.0.0.0 ansible_ssh_user=root ansible_ssh_pass=password')
        file_handle.close()

    put('/root/%s' % tmpFile, '/etc/sdcc/servers.ini', mode=0644, use_sudo=True)

    print 'Running sdcc-system-config ...'
    if threeNode:
        run('sdcc-system-config --3')
    else:
        run('sdcc-system-config --1')

    local('rm /root/%s' % tmpFile)


def GetLatestTag(node, branch):
    search_dir = '/mnt/nfs/storage1/rw_images/' + node + '/' + branch + '/'
    os.chdir(search_dir)
    directories = filter(os.path.isdir, os.listdir(search_dir))

    emptyDirs = []
    for directory in directories:
        files = os.listdir('/mnt/nfs/storage1/rw_images/' + node + '/' + branch + '/' + directory + '/')
        if len(files) == 0:
            emptyDirs.append(directory)

    for emptyDir in emptyDirs:
        directories.remove(emptyDir)

    directories.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    print 'Latest SDCC tag is: %s' % directories[0]
    return directories[0]


# endregion


# region Sanity Test Sets
@task
def Sanity(branch='master', services=DEFENSE_SERVICE, threeNode=False, vmServer='esx'):
    reportsFolder = REPORT_PATH + datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + '/'
    local('mkdir ' + reportsFolder)
    local('cp ' + LOCAL_PATH + 'ReportTemplate.xls ' + reportsFolder + 'RunReport.xls')
    reporter = ReporterLibrary(reportsFolder + 'RunReport.xls')

    print '\nSanity Test Set started.\n'
    testSetStartTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # region SDCC deployment
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print '\nCreating VM and installing SDCC ...\n'
    res = execute(full_deployment_sni, 'Sanity_' + branch + '_' + services, branch, vmServer=vmServer,
                  scName='SCRUBBING', scConf=SC_CONF_PATH, services=services, email=True)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    reporter.AddTestToReport('Deployment', 'SDCC Deployment', startTime, endTime, GetTestStatus(res.values()[0]))
    if res.values()[0] != 0:
        print 'Sanity Test Set is aborted due to failure in SDCC deployment.'
        return 1

    time.sleep(5)
    # endregion

    sys.stdout = Logger('Sanity_' + branch + '_' + services)

    # region Configuration section
    if threeNode:
        env.hosts = [server_list['fe']]
        dbIP = server_list['db']
        beIP = server_list['be']
        Set_PORTAL_IP(server_list['fe'])
        Set_DB_IP(server_list['db'])
    else:
        dbIP = env.hosts[0]
        beIP = env.hosts[0]
        Set_PORTAL_IP(env.hosts[0])
        Set_DB_IP(env.hosts[0])
    # endregion

    # region CRUD tests
    print '\nTest [CreateAccounts] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = CreateAccounts(2)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'CreateAccounts', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [CreateAccounts] finished. (%s)' % GetTestStatus(res)

    print '\nTest [CreateUsers] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = CreateUsers(2)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'CreateUsers', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [CreateUsers] finished. (%s)' % GetTestStatus(res)

    print '\nTest [CreateSites] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = CreateSites(2)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'CreateSites', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [CreateSites] finished. (%s)' % GetTestStatus(res)

    print '\nTest [CreateCPEs] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if services == DEFENSE_SERVICE:
        res, comments = CreateCPEs_defense(2)
    else:
        res, comments = CreateCPEs_mssp()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'CreateCPEs', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [CreateCPEs] finished. (%s)' % GetTestStatus(res)

    if services == DEFENSE_SERVICE:
        print '\nTest [CreateGREs] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = CreateGREs_defense(2)
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'CreateGREs', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [CreateGREs] finished. (%s)' % GetTestStatus(res)

        print '\nTest [CreateDFs] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = CreateDFs_defense(2)
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'CreateDFs', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [CreateDFs] finished. (%s)' % GetTestStatus(res)

    if services == DEFENSE_SERVICE:
        print '\nTest [CreateNetworkAssets] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = CreateAssets_defense(2, NETWORK_ASSET_TYPE)
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'CreateNetworkAssets', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [CreateNetworkAssets] finished. (%s)' % GetTestStatus(res)

        print '\nTest [CreateServerAssets] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = CreateAssets_defense(2, SERVER_ASSET_TYPE)
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'CreateServerAssets', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [CreateServerAssets] finished. (%s)' % GetTestStatus(res)

    else:
        print '\nTest [CreateAssets] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = CreateAssets_mssp(2)
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'CreateAssets', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [CreateAssets] finished. (%s)' % GetTestStatus(res)

    print '\nTest [EditAccounts] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = EditAccounts()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'EditAccounts', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [EditAccounts] finished. (%s)' % GetTestStatus(res)

    print '\nTest [EditUsers] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = EditUsers()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'EditUsers', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [EditUsers] finished. (%s)' % GetTestStatus(res)

    print '\nTest [EditSites] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = EditSites()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'EditSites', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [EditSites] finished. (%s)' % GetTestStatus(res)

    print '\nTest [EditCPEs] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if services == DEFENSE_SERVICE:
        res, comments = EditCPEs_defense()
    else:
        res, comments = EditCPEs_mssp()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'EditCPEs', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [EditCPEs] finished. (%s)' % GetTestStatus(res)

    if services == DEFENSE_SERVICE:
        print '\nTest [EditGREs] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = EditGREs_defense()
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'EditGREs', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [EditGREs] finished. (%s)' % GetTestStatus(res)

        print '\nTest [EditDFs] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = EditDFs_defense()
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'EditDFs', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [EditDFs] finished. (%s)' % GetTestStatus(res)

    print '\nTest [EditAssets] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if services == DEFENSE_SERVICE:
        res, comments = EditAssets_defense()
    else:
        res, comments = EditAssets_mssp()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'EditAssets', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [EditAssets] finished. (%s)' % GetTestStatus(res)

    print '\nTest [DeleteUsers] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = DeleteUsers()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'DeleteUsers', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [DeleteUsers] finished. (%s)' % GetTestStatus(res)

    print '\nTest [DeleteAssets] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = DeleteAssets()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'DeleteAssets', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [DeleteAssets] finished. (%s)' % GetTestStatus(res)

    print '\nTest [DeleteCPEs] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = DeleteCPEs()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'DeleteCPEs', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [DeleteCPEs] finished. (%s)' % GetTestStatus(res)

    if services == DEFENSE_SERVICE:
        print '\nTest [DeleteGREs] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = DeleteGREs()
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'DeleteGREs', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [DeleteGREs] finished. (%s)' % GetTestStatus(res)

        print '\nTest [DeleteDFs] started.'
        print '----------------------------------------'
        startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        res, comments = DeleteDFs()
        endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        reporter.AddTestToReport('CRUD', 'DeleteDFs', startTime, endTime, GetTestStatus(res), comments)
        print '----------------------------------------'
        print 'Test [DeleteDFs] finished. (%s)' % GetTestStatus(res)

    print '\nTest [DeleteSites] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = DeleteSites()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'DeleteSites', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [DeleteSites] finished. (%s)' % GetTestStatus(res)

    print '\nTest [DeleteAccounts] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = DeleteAccounts()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('CRUD', 'DeleteAccounts', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [DeleteAccounts] finished. (%s)' % GetTestStatus(res)
    # endregion

    # region SDK_API test
    print '\nTest [SDK API] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = SDK_API('Dummy', 'Dummy', 'Dummy', env.hosts[0], PORTAL_USERNAME, PORTAL_PASSWORD, dbIP)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('SDK', 'SDK_API', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [SDK API] finished. (%s)' % GetTestStatus(res)
    # endregion

    # region SessionExpiration test
    print '\nTest [SessionExpiration] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = SessionExpiration()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('General', 'SessionExpiration', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [SessionExpiration] finished. (%s)' % GetTestStatus(res)
    # endregion

    # region ReportTemplates test
    print '\nTest [ReportTemplates] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = ReportTemplates()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('Report', 'ReportTemplates', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [ReportTemplates] finished. (%s)' % GetTestStatus(res)
    # endregion

    # region Not supported
    """

    # region ChangeAccountProvider test
    print '\nTest [ChangeAccountProvider] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = ChangeAccountProvider()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('MSSP', 'ChangeAccountProvider', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [ChangeAccountProvider] finished. (%s)' % GetTestStatus(res)
    # endregion

    # region AttackDetection tests
    print '\n[AttackDetectionPreconditionFlow] started.'
    resPre, commentPre = AttackDetectionPreconditionFlow(be=beIP)
    print '[AttackDetectionPreconditionFlow] finished. (%s)' % GetTestStatus(resPre)

    print '\nTest [DetectAttack] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if resPre == 0:
        res, comments = DetectAttack()
    else:
        res, comments = resPre, '[DetectAttack] test cannot be run due to failure in precondition process.\n' + commentPre
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('Attack', 'DetectAttack', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [DetectAttack] finished. (%s)' % GetTestStatus(res)

    print '\nTest [SecurityAlerts] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if resPre == 0:
        res, comments = SecurityAlerts()
    else:
        res, comments = resPre, '[SecurityAlerts] test cannot be run due to failure in precondition process.\n' + commentPre
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('Attack', 'SecurityAlerts', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [SecurityAlerts] finished. (%s)' % GetTestStatus(res)

    print '\nTest [OperationalAlerts] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if resPre == 0:
        res, comments = OperationalAlerts()
    else:
        res, comments = resPre, '[OperationalAlerts] test cannot be run due to failure in precondition process.\n' + commentPre
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('Attack', 'OperationalAlerts', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [OperationalAlerts] finished. (%s)' % GetTestStatus(res)

    print '\nTest [EmailAlerts] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if resPre == 0:
        res, comments = EmailAlerts(be=beIP)
    else:
        res, comments = resPre, '[EmailAlerts] test cannot be run due to failure in precondition process.\n' + commentPre
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    reporter.AddTestToReport('Attack', 'EmailAlerts', startTime, endTime, GetTestStatus(res), comments)
    print '----------------------------------------'
    print 'Test [EmailAlerts] finished. (%s)' % GetTestStatus(res)

    print '\n[AttackDetectionPostFlow] started.'
    AttackDetectionPostFlow()
    print '[AttackDetectionPostFlow] finished.'
    # endregion

    """
    # endregion

    print '\nSanity Test Set finished.\n'
    testSetEndTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    reporter.AddGeneralInformation(env.hosts[0], branch, threeNode, testSetStartTime, testSetEndTime)

    # region Remove/Stop VMs
    if reporter.GetFailedCount() == 0:
        allPass = True
    else:
        allPass = False

    try:
        if vmServer == 'esx':
            esx = ESXClient(ip=ESX_SERVER)
            for vm in vmNames:
                if allPass:
                    esx.RemoveVM(vm)
                else:
                    esx.PowerOFF(vm)
            esx.Disconect()
        else:
            xen = XenClient(ip=XEN_SERVER)
            for vm in vmNames:
                if allPass:
                    xen.RemoveVM(vm)
                else:
                    xen.StopVM(vm)
            xen.Disconect()
    except:
        traceback.print_exc()
    # endregion

    # region Send Email
    mail = EmailLibrary()

    subject = "Sanity Automation Report "
    if threeNode:
        subject += '(3 node)'
    else:
        subject += '(1 node)'

    message = 'Sanity Automation Report from: ' + datetime.datetime.now().strftime('%d/%m/%Y') + '.\n\n'

    if threeNode:
        for host in server_list.keys():
            message += host.upper() + ' IP:  \t\t' + (server_list[host] + '\n').expandtabs(8)
    else:
        message += 'SDCC IP: \t\t' + (env.hosts[0] + '\n').expandtabs(8)

    message += 'Branch: \t\t' + (branch + '\n').expandtabs(8)
    message += 'Service: \t\t' + (services + '\n').expandtabs(8)

    message += '---------------------------------------\n'
    message += 'Total Passed: \t' + (str(reporter.GetPassedCount()) + '\n').expandtabs(8)
    message += 'Total Failed: \t' + (str(reporter.GetFailedCount()) + '\n').expandtabs(8)
    message += '---------------------------------------\n'
    message += 'Total: \t\t\t' + (str(reporter.GetTotalCount()) + '\n').expandtabs(8)
    mail.SendMail(subject, message, 'automation@securitydam.com', [reportsFolder + 'RunReport.xls'], recepient)
    # endregion

    return 0


@task
def SanityDev():
    env.hosts = ['10.20.4.184']
    Set_PORTAL_IP(env.hosts[0])
    Set_DB_IP(env.hosts[0])

    print '\nTest [CreateAccounts] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = CreateAccounts(2)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print '----------------------------------------'
    print 'Test [CreateAccounts] finished. (%s)' % GetTestStatus(res)

    print '\nTest [CreateSites] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = CreateSites(2)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print '----------------------------------------'
    print 'Test [CreateSites] finished. (%s)' % GetTestStatus(res)

    print '\nTest [CreateNetworkAssets] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = CreateAssets_defense(2, NETWORK_ASSET_TYPE)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print '----------------------------------------'
    print 'Test [CreateNetworkAssets] finished. (%s)' % GetTestStatus(res)

    print '\nTest [CreateServerAssets] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = CreateAssets_defense(2, SERVER_ASSET_TYPE)
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print '----------------------------------------'
    print 'Test [CreateServerAssets] finished. (%s)' % GetTestStatus(res)

    print '\nTest [EditSites] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = EditSites()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print '----------------------------------------'
    print 'Test [EditSites] finished. (%s)' % GetTestStatus(res)

    print '\nTest [EditAssets] started.'
    print '----------------------------------------'
    startTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    res, comments = EditAssets_defense()
    endTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print '----------------------------------------'
    print 'Test [EditAssets] finished. (%s)' % GetTestStatus(res)

    return 0


# endregion


if __name__ == '__main__':
    print ' '
