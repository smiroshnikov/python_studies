import sys
import time

"""" Ain't working withing conda virtual ENV """

print ("\nThis script determines if executed inside virtual env!")
print("Wait : %s" % time.ctime())
time.sleep(3)
if hasattr(sys, 'real_prefix'):
    print ("Yeah you are in virtual env")
else:
    print ("\nRunning in real env!!! Careful ")
