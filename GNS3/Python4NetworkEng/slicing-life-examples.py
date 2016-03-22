import re  # is this regular expression

traceroute = "80.179.166.85.static.012.net.il (80.179.166.85)  123.910 ms "
OSPRF = "O 5.0.0.0/8 [110/128] via 6.0.0.2, 22:55:44, Serial0"

second_ip = traceroute[traceroute.find("(") + 1: traceroute.find(")")]
print traceroute.strip(".")  # ffs!
a = "80.179.166.85"
print a.strip(".")
print a[::-1]  # this is reverse , I want the last octet
