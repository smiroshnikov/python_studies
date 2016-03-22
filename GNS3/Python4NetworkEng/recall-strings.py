# remeber that string re immutable

device_type = "Cisco Switch"
router_type = "Cisco"
model_number = "29601"
print device_type.count("c")
print device_type.find("i")
print device_type.find("xyz")
print (device_type.upper() + "-> string remained immutable")
print device_type.startswith("k")
print device_type.endswith("h")

# 3 important methods for string manipulation
# split, strip, join


a = "     Cisco Router     "
print (a.strip())
c = "$$$Cisco router$$$"
print ("***", c.strip("$"))
print (a.replace(" ", ""))  # immutable
print a
d = "cisco,f5,brocade,nortel,hp,juniper"
providers_list = d.split(",")
print d
print providers_list
print ("-".join(router_type))
# concatenation
print router_type + " " + model_number
print ("o" in (router_type + model_number))
print ("b" not in router_type)
# %f float , %d - digits , %s strings
print ("Cisco model: %s, %d WAN slots , IOS %.1f " % ("2600XM", 2, 12.4))
