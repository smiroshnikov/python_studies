GNS_SERVER = '10.20.4.200'  # GNS server IP address
LOCAL_PATH = 'C:\DRot\\'


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


set_persistent_route()
#  res = put(LOCAL_PATH + 'route-eth0', '/etc/sysconfig/network-scripts/route-eth0', mode=0755, use_sudo=True)
#  run('/etc/init.d/network restart')
#    if res.failed:
#        raise Exception("Failed to configure persistent route.")
