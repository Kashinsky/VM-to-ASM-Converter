#!/usr/bin/python
import sys, getopt, re
from Reader import VMReader
from Writer import VMWriter


# Calls the error message function with the programs usage
def printUsage(errCode):
    printerr("USAGE: python vmcompiler.py [-h][-l][-d] <file.vm>",errCode)

def printAdd(args, writer):
    if len(args) > 0:
        writer.error("Add does not take args")
    writer.prepare(";--add--")
    printSimplePop(writer)
    writer.prepare('D=M')
    printSimplePop(writer)
    writer.prepare('D=D+M')
    writer.prepare('M=D')
    writer.prepare('@SP')
    writer.prepare('M=M+1')

def printSub(args, writer):
    if len(args) > 0:
        writer.error("Sub does not take args")
    writer.prepare(';--subtract--')
    printSimplePop(writer)
    writer.prepare('D=-M')
    printSimplePop(writer)
    writer.prepare('D=D+M')
    writer.prepare('M=D')
    writer.prepare('@SP')
    writer.prepare('M=M+1')


def printNeg(args, writer):
    if len(args) > 0:
        writer.error("Neg does not take args")
    writer.prepare(';--negate--')
    printSimplePop(writer)
    writer.prepare('M=-M')
    writer.prepare('@SP')
    writer.prepare('M=M+1')

def printEq(args, writer):
    if len(args) > 0:
        writer.error("Eq does not take args")
    writer.prepare(';--equals--')
    printSimplePop(writer)
    writer.prepare('D=M')
    writer.prepare('@13')
    writer.prepare('M=D')
    printSimplePop(writer)
    writer.prepare('D=M')
    writer.prepare('@13')
    writer.prepare('D=D-M')
    passL = genLabel("eq.pass")
    writer.prepare('@' + passL)
    writer.prepare('D;JEQ')
    writer.prepare('@SP')
    writer.prepare('A=M')
    writer.prepare('M=0')
    writer.prepare('@SP')
    writer.prepare('M=M+1')
    afterL = genLabel("eq.after")
    writer.prepare('@' + afterL)
    writer.prepare('0;JMP')
    writer.prepare('(' + passL + ')')
    writer.prepare('@SP')
    writer.prepare('A=M')
    writer.prepare('M=-1')
    writer.prepare('@SP')
    writer.prepare('M=M+1')
    writer.prepare('(' + afterL + ')')


def printGt(args, writer):
    if len(args) > 0:
        printerr("GT does not take args",1)
    writer.prepare(';--greater than--')
    printSimplePop(writer)
    writer.prepare('D=M')
    writer.prepare('@13')
    writer.prepare('M=D')
    printSimplePop(writer)
    writer.prepare('D=M')
    writer.prepare('@13')
    writer.prepare('D=D-M')
    passL = genLabel("gt.pass")
    writer.prepare('@' + passL)
    writer.prepare('D;JGT')
    writer.prepare('@SP')
    writer.prepare('A=M')
    writer.prepare('M=0')
    writer.prepare('@SP')
    writer.prepare('M=M+1')
    afterL = genLabel("gt.after")
    writer.prepare('@' + afterL)
    writer.prepare('0;JMP')
    writer.prepare('(' + passL + ')')
    writer.prepare('@SP')
    writer.prepare('A=M')
    writer.prepare('M=-1')
    writer.prepare('@SP')
    writer.prepare('M=M+1')
    writer.prepare('(' + afterL + ')')

def printLt(args, writer):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('LT')

def printAnd(args, writer):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('AND')

def printOr(args, writer):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('OR')

def printNot(args, writer):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('NOT')

def printPush(args, writer):
    if len(args) > 2:
        printerr("Push does not take args",1)
    print ('PUSHING',args)

def printPop(args, writer):
    if len(args) > 2: 
        printerr("Eq does not take args",1)
    print ('POPPING')

def printSimplePop(writer):
    writer.prepare('@SP\nAM=M-1')

def processVM(argv):
    reader = VMReader(argv[0])
    writer = VMWriter(re.sub(r'.vm','.asm',argv[0])) 
    hackDict = {'add':printAdd, 'sub':printSub, 'neg':printNeg, 'eq':printEq, 'gt':printGt, 'lt':printLt, 'and':printAnd, 'or':printOr, 'not':printNot, 'push':printPush, 'pop':printPop}
    line = reader.next()
    while line != "**EOF**":
        entry = hackDict[line[0]]
        if entry == None:
            writer.error("Cannot find symbol " + line[0] + " at line " + reader.lno)
        entry(line[1:],writer)
        line = reader.next()

if __name__ == '__main__':
    processVM(sys.argv[1:])

