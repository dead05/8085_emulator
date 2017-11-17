import out
import func
import sizes
import regi

def select(cmd):
    cmd = cmd.strip().split(" ")
    #  LOAD AND STORE COMMANDS
    if cmd[0] == "LDA" and len(cmd) > 1:
        func.LDA(cmd[1])

    elif cmd[0] == "MOV" and len(cmd) > 1:
        regs = cmd[1].strip().split(",")
        func.MOV(regs[0], regs[1])

    elif cmd[0] == "STA" and len(cmd) > 1:
        func.STA(cmd[1])

    elif cmd[0] == "MVI" and len(cmd) > 1:
        operand = cmd[1].strip().split(",")
        func.MVI(operand[0], operand[1])

    elif cmd[0] == "LXI" and len(cmd) > 1:
        operand = cmd[1].strip().split(",")
        func.LXI(operand[0],operand[1].strip())

    elif cmd[0] == "LHLD" and len(cmd) > 1:
        func.LHLD(cmd[1])

    elif cmd[0] == "SHLD" and len(cmd) > 1:
        func.SHLD(cmd[1])

    elif cmd[0] == "XCHG":
        func.XCHG()

    elif cmd[0] == "STAX" and len(cmd) > 1:
        func.STAX(cmd[1])

    # ARITHMETIC COMMANDS

    elif cmd[0] == "ADD" and len(cmd) > 1:
        func.ADD(cmd[1])

    elif cmd[0] == "SUB" and len(cmd) > 1:
        func.SUB(cmd[1])

    elif cmd[0] == "ADI" and len(cmd) > 1:
        func.ADI(cmd[1])

    elif cmd[0] == "INR" and len(cmd) > 1:
        func.INR(cmd[1])

    elif cmd[0] == "DCR" and len(cmd) > 1:
        func.DCR(cmd[1])

    elif cmd[0] == "INX" and len(cmd) > 1:
        func.INX(cmd[1])

    elif cmd[0] == "DCX" and len(cmd) > 1:
        func.DCX(cmd[1])

    elif cmd[0] == "DAD" and len(cmd) > 1:
        func.DAD(cmd[1])

    elif cmd[0] == "SUI" and len(cmd) > 1:
        func.SUI(cmd[1])

    # LOGICAL COMMANDS

    elif cmd[0] == 'CMP' and len(cmd) > 1:
        func.CMP(cmd[1])

    elif cmd[0] == 'CMA':
        func.CMA()

    # BRANCHING COMMANDS

    elif cmd[0] == 'JMP' and len(cmd) > 1:
        return func.JMP(cmd[1])

    elif cmd[0] == 'JC' and len(cmd) > 1:
        return func.JC(cmd[1])

    elif cmd[0] == 'JNC' and len(cmd) > 1:
        return func.JNC(cmd[1])

    elif cmd[0] == 'JZ' and len(cmd) > 1:
        return func.JZ(cmd[1])

    elif cmd[0] == 'JNZ' and len(cmd) > 1:
        return func.JNZ(cmd[1])

    # EXTRA COMMANDS

    elif cmd[0] == "SET" and len(cmd) > 1:
        operand = cmd[1].strip().split(",")
        func.SET(operand[0], operand[1])

    elif cmd[0] == "HLT":
        out.show()
        if regi.dBugOn == True:
            return
        exit(1)
    else:
        print "operand missing:", cmd
        exit(1)


def start_exec(mem, isStep=False):

    while True:
        cmd = regi.memory[mem]
        t = cmd.strip().split(" ")
        mem_int = int(mem, 16)
        mem_int+=sizes.getSize(t[0])
        mem = format(mem_int, "0x")
        if t[0] == "JMP" or t[0] == "JNC" or t[0] == "JC" or t[0] == "JZ" or t[0] == "JNZ":
            tmp_mem = mem
            mem = select(cmd)
            if mem is None:
                mem = tmp_mem
        else:
            select(cmd)
        if regi.dBugOn == True and cmd.strip() == "HLT":
            return
        if isStep:
            print "Executing:", cmd
            query = raw_input("Press Enter For Next Instruction Execution(q to quit step execution):")
            if query == "q" or query == "quit":
                return
