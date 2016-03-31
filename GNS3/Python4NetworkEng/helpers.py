import random
import re
import time
import datetime
import socket
from subprocess import Popen, PIPE
import base64
from Crypto.Cipher import AES
from Crypto import Random
from socket import inet_ntoa
from struct import pack
from pbkdf2 import crypt


def validIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True


def local_ip():
    # return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0].strip()
    return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in
            [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


def randomMAC():
    mac = [0, 1, 0xAC,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]

    return ':'.join(map(lambda x: "%02x" % x, mac))


def randomIP(subnet='10.20.4.0/24'):
    print ' '
    ip_prefix = ''
    ip = subnet.split('/')[0]
    subnet = subnet.split('/')[1]
    if subnet == '24':
        ip_prefix = '.'.join(ip.split('.')[:3]) + '.'

    return ip_prefix + str(random.randint(2, 200))
    # return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


def arp_scan(mac):
    cmd = 'arp-scan --interface=eth0 10.20.4.1-10.20.5.254'  # --localnet'# | grep -io %s'%mac
    arp_clean_cmd = 'ip -s -s neigh flush all'
    arpclean = Popen(arp_clean_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    arp_out, arp_err = arpclean.communicate()
    # print "Arp Cleaned: ", arp_out

    for attempt in range(10):
        print "Attempting IP detection ..."
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()

        for line in out.split('\n'):
            if validIP(mac.lower()):  # IP
                if (mac.lower() in line.lower()) and (mac.lower() == line.split()[0]):
                    print "Found: ", line
                    return line.split()[0]
            else:  # MAC
                if mac.lower() in line.lower():
                    print "Found: ", line
                    return line.split()[0]

        if validIP(mac.lower()):
            return False

        time.sleep(8)
    print "== IP of VM Not Found =="
    return False


def find_free_ip():
    for i in range(1, 10):
        ip = randomIP()
        print 'Validating random IP address: ' + ip + ' ...\n'

        if find_ip(ip):
            print "\nIP address: " + ip + " is not available.\n"
            continue
        else:
            print "\nIP address: " + ip + " is available.\n"
            return ip
    print "\nNo free IPs was found.\n"
    return False


def find_mac(fileName):
    # tmpfile = None
    mac = ''
    with open(fileName, 'r') as fid:
        tmpfile = fid.read().split('\n')

    for line in tmpfile:
        try:
            mac = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', line, re.I).group()
            return line.split('=')[1]
        except:
            pass

    return mac


def find_ip(new_mac):
    """
    Run arp scan tool to find matching IP for a given MAC in the network
    :param new_mac: MAC address to find its matching IP address
    :return:
    """

    ip = arp_scan(new_mac)
    if ip:
        time.sleep(5)
        return ip
    elif validIP(new_mac):
        return False
    else:
        print "Failed to obtain IP after reset."
        return False


def replace(fileName, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(fileName, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(fileName, 'w')
    file_handle.write(file_string)
    file_handle.close()


def add_ip(fileName, ip):
    print "Updating IP configuration in ifcfg-eth file ..."
    print 'IP=%s, NETMASK=255.255.255.0, GATEWAY=10.20.4.254' % ip
    with open(fileName, "a") as f:
        f.write("IPADDR=%s\nNETMASK=255.255.255.0\nGATEWAY=10.20.4.254\n" % ip)


def add_dns(fileName):
    print "Updating DNS configuration in ifcfg-eth file ..."
    with open(fileName, "a") as f:
        f.write("\nDNS1=8.8.8.8\nDNS2=8.8.4.4\n")


def get_time(date=True, hour=True):
    if date and hour:
        return datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    elif date and not hour:
        return datetime.datetime.now().strftime("%Y-%m-%d")
    elif hour and not date:
        return datetime.datetime.now().strftime("%H-%M-%S")
    else:
        return


def edit_sc(src_file, line_num, text, dst_file=None):
    lines = open(src_file, 'r').readlines()
    lines[line_num] = text
    if dst_file:
        out = open(dst_file, 'w')
    else:
        out = open(src_file, 'w')
    out.writelines(lines)
    out.close()


def fmtcols(mylist, cols):
    """
    Format list items in columns with fixed width
    :param mylist: List to work on
    :param cols: Number of columns
    :return:
    """
    maxwidth = max(map(lambda x: len(x), mylist))
    justifyList = map(lambda x: x.ljust(maxwidth), mylist)
    lines = (' '.join(justifyList[i: i + cols])
             for i in xrange(0, len(justifyList), cols))
    print "\n".join(lines)


def elapsed(start):
    end = time.time()
    total = end - start
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    print "Elapsed Time - %d:%02d:%02d" % (h, m, s)


def crypt_encrypt(plaintext, key):
    # Encrypt a value using a key in a secure and reversible manner. This is a
    # simple wrapper around AES encryption using PyCrypt

    # The returned value is a string containing both the IV and the ciphertext.
    # The IV is normally 16 bytes but this may be implementation dependant. In any
    # case as long as the text is decrypted with crypt_decrypt this should work

    iv = Random.get_random_bytes(AES.block_size)
    cipher = AES.new(base64.b64decode(key), AES.MODE_CFB, iv)
    return base64.b64encode(iv + cipher.encrypt(plaintext))


def crypt_decrypt(ciphertext, key):
    # Decrypt a value encrypted using crypt_encrypt. This is a simple wrapper
    # around AES encryption using PyCrypt

    # `ciphertext` must be the value as returned by crypt_encrypt: the first bytes
    # are the IV, the rest is the ciphertext. Will return the original plain-text value.

    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[0:AES.block_size]
    cipher = AES.new(base64.b64decode(key), AES.MODE_CFB, iv)
    return cipher.decrypt(ciphertext[16:])


def crypt_generate_key(key_size=32):
    """
    Generate a key usable by the crypt_encrypt and crypt_decrypt functions. This
    is normally only required once during installation.

    The returned value is base64 encoded, as expected by these functions.
    :param key_size:
    """

    if key_size not in (16, 24, 32):
        raise ValueError("Key size can only be one of 16, 24 or 32 bytes")
    return base64.b64encode(Random.get_random_bytes(key_size))


def CryptPassword(password):
    return crypt(password, iterations=1200)


def CheckPassword(password, cryptedPassword):
    return crypt(password, cryptedPassword, iterations=1200)


def get_subnet_mask(mask):
    mask = int(mask)
    bits = 0
    for i in xrange(32 - mask, 32):
        bits |= (1 << i)
    return inet_ntoa(pack('>I', bits))


def GetTestStatus(status):
    if status == 0:
        return 'PASS'
    else:
        return 'FAIL'


def ToBoolen(val):
    if val.lower() == 'true':
        return True
    else:
        return False


if __name__ == "__main__":
    print ''
