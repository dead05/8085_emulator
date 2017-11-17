import regi


def show():
    print "____________________________"
    print "_________Memory_____________"
    for addr,data in regi.memory.items():
        if data.strip().split(" ")[0] == "HLT":print addr,data+"\n"
        else:print addr,data
    print "____________________________"

    print "_________regi__________"
    for reg,val in regi.reg.items():
        print reg,val
    print "____________________________"

    print "___________Flags____________"
    for f,val in regi.flag.items():
        print f,val
    print "____________________________"


    print "___________Labels___________"
    for l, val in regi.label.items():
        print l, val
    print "____________________________"
