x = 0
exit_flag = True

while exit_flag:
    x += 1
    if x % 100 == 0:
        exit_flag = False
    elif x % 50 == 0:
        print "Reached 50%!"
    elif x % 75 == 0:
        print "Reached 75%!"
    elif x % 95 == 0:
        print "Critical 95%!"
