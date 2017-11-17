import ext
import init
import regi
import validate

breakPoint = -1
def isDebuggerOn():
    if regi.dBugOn:
        return True
    else:
        return False


def prnt(addr):
    try:
        if validate.validate_reg(addr):
            print regi.reg[addr]

        elif ext.chkMemory(addr):
            print regi.memory[addr]

        else:
            print " Invalid Memory or Register!!"
    except:
        print "invalid command type help for list of commands!!"



def hlp():
    print "Setting BreakPoint          --------  break 3 or b 3"
    print "Run Program (or till BreakPoint) ---  run or r "
    print "Step by Step Execution      --------  step or s"
    print "Print Data From Register or Mem) ---  print A or p 2500"
    print "Quit Debugger               --------  quit or q"
    print "Show Available Commands     --------  help"


def step(isCmdLine=False):
    init.memInit(isStep=True, isCmdLine=isCmdLine)


def run(breakPoint, isCmdLine=False):
    if breakPoint >= 0:
        init.memInit(count=breakPoint, isCount=True, isCmdLine=isCmdLine)
    else:
        init.memInit(isCmdLine=isCmdLine)


def startDebugger(isCmdLine=False):
    while isDebuggerOn():
        cmd = raw_input("Enter Debugger Command: ").strip().split(" ")
        if (cmd[0] == "break" or cmd[0] == "b") and len(cmd) > 1:
            breakPoint = int(cmd[1])
        elif cmd[0] == "run" or cmd[0] == "r":
            try:
                run(breakPoint, isCmdLine=isCmdLine)
            except:
                run(-1,isCmdLine=isCmdLine)
        elif cmd[0] == "step" or cmd[0] == "s":
            step(isCmdLine=isCmdLine)
        elif (cmd[0] == "print" or cmd[0] == "p") and len(cmd) > 1:
            prnt(cmd[1])
        elif cmd[0] == "help":
            hlp()
        elif cmd[0] == "quit" or cmd[0] == "q":
            regi.dBugOn = False
            return
        else:
            print "invalid command type help for list of commands!!"

