def funny(s):
    slist = s.split(" ")

    result = [e[::-1].capitalize() for e in slist]  # this crap is called list comprehension
    # need to retry this in Java or C#

    #  s2 = slist[0][::-1].capitalize() + " " + slist[1][::-1].capitalize()
    # result = []
    # for e in slist:
    #    result.append(e[::-1].capitalize())

    return ' '.join(result)


result = funny("Foo bar")
print(result)
assert result == "Oof Rab"

result = funny("The quick brown fox")
print(result)
assert result == "Eht Kciuq Nworb Xof"

print("OK")

f = open("name")
s = f.read()
f.close()

with open("file") as f:
    s = f.read()
    # will close file automatically
