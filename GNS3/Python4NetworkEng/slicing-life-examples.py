traceroute = "80.179.166.85.static.012.net.il (80.179.166.85)  123.910 ms "
OSPRF = "O 5.0.0.0/8 [110/128] via 6.0.0.2, 22:55:44, Serial0"

second_ip = traceroute[traceroute.find("(") + 1: traceroute.find(")")]
print ("Second IP is %s" % second_ip)
print "*** + %s" % second_ip[:-10]
print traceroute.strip(".")  # ffs! this is not working !
print second_ip.split(".")[3]  # this will be useful
"""
a = "80.179.166.85"
print a.strip(".")
print a[::-1]  # this is reverse , I want the last octet
"""
