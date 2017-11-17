import ext
import regi
import set_flags
import validate


#####################################################
#                ARITHMETICS                        #
#####################################################

def ADD(register):
    if not validate.validate_reg(register):
        print "Invalid Register: %s"%register
        exit(1)
    a = int(regi.reg["A"], 16)
    if register == "M":
        b = ext.getPair('H', 'L')
        if ext.chkMemory(b):
            b = int(regi.reg[register], 16)
        else:
            print " Invalid Memory:", b
            exit(1)
    else:
        b = int(regi.reg[register], 16)
    t = a + b
    a = int(ext.getLowerNibble(format(a, '0x')), 2)
    b = int(ext.getLowerNibble(format(b, '0x')), 2)
    if not validate.validate_data(t):
        print "\n////-----OverFlow Detected----////\n"
        t = format(t,"02x")
        t = set_flags.setCarry(t)
        set_flags.setFlags(a, b, t, isAbnormalFlow=True)
        tmp = {"A": t[1:]}
    else:
        t = format(t, "02x")
        tmp = {"A": t}
        set_flags.setFlags(a,b,t)
    regi.reg.update(tmp)


def SUB(register):
    if not validate.validate_reg(register):
        print "Invalid Register: %s"%register
        exit(1)
    a = int(regi.reg["A"],16)
    if register == "M":
        b = ext.getPair('H', 'L')
        if ext.chkMemory(b):
            b = int(regi.reg[register], 16)
        else:
            print " Invalid Memory:", b
            exit(1)
    else:
        b = int(regi.reg[register], 16)
    t = a - b
    a = int(ext.getLowerNibble(format(a, '0x')), 2)
    b = int(ext.getLowerNibble(format(b, '0x')), 2)
    if not validate.validate_data(t):
        print "\n////-----UnderFlow Detected----////\n"
        t = format(t,"02x")
        t = set_flags.setCarry(t)
        set_flags.setFlags(a, b, t, isAbnormalFlow=True)
        tmp = {"A": t[1:]}
    else:
        t = format(t, "02x")
        set_flags.setFlags(a, b, t)
        tmp = {"A": t}
        set_flags.setFlags(a,b,t)
    regi.reg.update(tmp)


def ADI(data):
    a = int(regi.reg['A'], 16)
    b = int(data, 16)
    res = format((a + b), '02x')
    a = int(ext.getLowerNibble(format(a, '0x')), 2)
    b = int(ext.getLowerNibble(format(b, '0x')), 2)
    if validate.validate_data(int(res, 16)):
        regi.reg['A'] = res
        set_flags.setFlags(a, b, res)
    else:
        print "\n Overflow Detected ADI", data
        print "Register Data[A]:", regi.reg['A']
        exit(1)


def INR(register):
    if validate.validate_reg(register):
        if register == 'M':
            a = ext.getPair('H', 'L')
            if ext.chkMemory(a):
                b = int(regi.memory[a], 16) + 1
                if b > 255:
                    b = 0
                regi.memory[a] = format(b, '0x')
            else:
                print "invalid memory:", a
                exit(1)
        else:
            b = int(regi.reg[register], 16) + 1
            if b > 255:
                b = 0
            regi.reg[register] = format(b, '0x')


def DCR(register):
    if validate.validate_reg(register):
        if register == 'M':
            a = ext.getPair('H', 'L')
            if ext.chkMemory(a):
                b = int(regi.memory[a], 16) - 1
                if b < 0:
                    b = 255
                regi.memory[a] = format(b, '0x')
            else:
                print "invalid memory:", a
                exit(1)
        else:
            b = int(regi.reg[register], 16) - 1
            if b < 0:
                b = 255
            regi.reg[register] = format(b, '0x')


def INX(reg1):
    if validate.validate_reg(reg1):
        try:
            reg2 = regi.reg_pair[reg1]
        except:
            print "invalid register pair", reg1
            exit(1)
        a = ext.getPair(reg1, reg2)
        a = int(a, 16) + 1
        if a > 65535:
            a = 0
        a = format(a, '04x')
        regi.reg[reg1] = a[:2]
        regi.reg[reg2] = a[2:]
    else:
        print "invalid register", reg1
        exit(1)


def DCX(reg1):
    if validate.validate_reg(reg1):
        try:
            reg2 = regi.reg_pair[reg1]
        except:
            print "invalid register pair", reg1
            exit(1)
        a = ext.getPair(reg1, reg2)
        a = int(a, 16) + 1
        if a < 0:
            a = 65535
        a = format(a, '04x')
        regi.reg[reg1] = a[:2]
        regi.reg[reg2] = a[2:]
    else:
        print "invalid register", reg1
        exit(1)


def DAD(reg1):
    if validate.validate_reg(reg1):
        c = 0
        try:
            reg2 = regi.reg_pair[reg1]
        except:
            print "invalid register pair", reg1
            exit(1)
        a = int(regi.reg[reg2], 16)
        res = int(regi.reg['L'], 16) + a
        if res > 255:
            c = 1
            res -= 256
        regi.reg['L'] = format(res, '02x')
        a = int(regi.reg[reg1], 16)
        res = int(regi.reg['H'], 16) + a + c
        res = format(res, '02x')
        if not validate.validate_data(int(res, 16)):
            res = set_flags.setCarry(res)
        regi.reg['H'] = res
    else:
        print 'invalid register pair:', reg1
        exit(1)


def SUI(data):
    a = int(regi.reg['A'], 16)
    b = int(data, 16)
    res = a - b
    res = format(res, '02x')
    if not validate.validate_data(int(res, 16)):
        res = set_flags.setCarry(res)
        set_flags.setFlags(a, b, res, isAbnormalFlow=True)
    else:
        set_flags.setFlags(a, b, res)

    regi.reg['A'] = res

#####################################################
#               LOAD AND STORE                      #
#####################################################

def MOV(reg1, reg2):
    if not validate.validate_reg(reg1):
        print "Invalid Register: %s"%reg1
        exit(1)
    if not validate.validate_reg(reg2):
        print "Invalid Register: %s"%reg2
        exit(1)
    if reg1 == 'M':
        a = ext.getPair('H','L')
        if ext.chkMemory(a):
            regi.memory[a] = regi.reg[reg2]
        else: print " Invalid Memory:",a

    elif reg2 == 'M':
        a = ext.getPair('H', 'L')
        regi.reg[reg1] = regi.memory[a]
    else:
        regi.reg[reg1] = regi.reg[reg2]


def LDA(addr):
    data = regi.memory[addr]
    if validate.validate_data(int(data, 16)):
        regi.reg['A'] = data
    else:
        print "Data Invalid. Please Retry"

def STA(addr):
    regi.memory[addr] = regi.reg["A"]


def MVI(reg, data):
    if reg == 'M':
        a = ext.getPair('H','L')
        regi.memory[a] = data
    elif validate.validate_reg(reg):
        regi.reg[reg] = data
    else: print "Invalid Register"


def LXI(register, data):
    if validate.validate_reg(register):
        regi.reg[register] = data[:2]
        if len(data[2:]) > 1:
            regi.reg[regi.reg_pair[register]] = data[2:]
    else:
        print "Invalid Register",register
        exit(1)


def LHLD(addr):
    if ext.chkMemory(addr) and ext.chkMemory(str(int(addr) + 1)):
        regi.reg['L'] = regi.memory[addr]
        regi.reg['H'] = regi.memory[str(int(addr) + 1)]
    else:
        print "Pointing Invalid Memory:", addr


def SHLD(mem):
    a = ext.getPair('H', 'L')
    regi.memory[mem] = a


def XCHG():
    regi.reg['D'], regi.reg['H'] = regi.reg['H'], regi.reg['D']
    regi.reg['E'], regi.reg['L'] = regi.reg['L'], regi.reg['E']


def STAX(register):
    if validate.validate_reg(register):
        a = ext.getPair(register, regi.reg_pair[register])
        regi.memory[a] = regi.reg['A']
    else:
        print "Invalid Register:", register
        exit(1)


#####################################################
#               LOGICAL OPERATIONS                  #
#####################################################

def CMP(register):
    if validate.validate_reg(register):
        a_data = int(regi.reg['A'], 16)
        if register == 'M':
            a = ext.getPair('H', 'L')
            if validate.validate_memory(a):
                a = int(regi.memory[a], 16)
            else:
                print "Invalid Memory:", a
                exit(1)
        else:
            a = int(regi.reg[register], 16)
        if a_data < a:
            regi.flag['CY'] = 1
        elif a_data == a:
            regi.flag['Z'] = 1
        else:
            regi.flag['CY'] = 0
            regi.flag['Z'] = 0
    else:
        print "Invalid Register:", regi
        exit(1)


def CMA():
    data = regi.reg['A']
    regi.reg['A'] = format(255 - int(data, 16), '0x')


#####################################################
#            BRANCHING OPERATIONS                   #
#####################################################

def JMP(addr):
    if ext.chkLable(addr):
        return regi.label[addr]
    elif ext.chkMemory(addr):
        return addr
    else:
        print 'pointing to invalid memory:', addr
        exit(1)


def JC(addr):
    if regi.flag['CY'] == 1:
        return JMP(addr)
    else:
        return


def JNC(addr):
    if regi.flag['CY'] == 0:
        return JMP(addr)
    else:
        return


def JNZ(addr):
    if regi.flag['Z'] == 0:
        return JMP(addr)
    else:
        return


def JZ(addr):
    if regi.flag['Z'] == 1:
        return JMP(addr)
    else:
        return


#####################################################
#                   ext                          #
#####################################################

def SET(addr, data):
    if validate.validate_data(int(data,16)):
        regi.memory[addr] = data
    else:
        print "Data Invalid.\nPlease Enter Valid Data at Memory Location: %s"%addr
        exit(1)
