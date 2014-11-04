#!/usr/bin/python
import sys, getopt, re

dest = None

# Calls the error message function with the programs usage
def printUsage(errCode):
    printerr("USAGE: python vmcompiler.py [-h][-l][-d] <file.vm>",errCode)

def printerr(message, errCode):
    print (message)
    sys.exit(errCode)

def printAdd(args):
    if len(args) > 0:
        printerr("Add does not take args", 1)
    print ('@SP')
    print ('AM=M-1')
    print ('D=M')
    print ('@SP')
    print ('AM=M-1')
    print ('D=D+M')
    print ('M=D')
    print ('@SP')
    print ('M=M+1')

def printSub(args):
    if len(args) > 0:
        printerr("Sub does not take args",1)
    print ('SUBTRACTING',args)

def printNeg(args):
    if len(args) > 0:
        printerr("Neg does not take args",1)
    print ('NEGATING')

def printEq(args):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('EQ')

def printGt(args):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('GT')

def printLt(args):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('LT')

def printAnd(args):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('AND')

def printOr(args):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('OR')

def printNot(args):
    if len(args) > 0:
        printerr("Eq does not take args",1)
    print ('NOT')

def printPush(args):
    if len(args) > 2:
        printerr("Push does not take args",1)
    print ('PUSHING',args)

def printPop(args):
    if len(args) > 2: 
        printerr("Eq does not take args",1)
    print ('POPPING')

def processVM(argv):
    src = open(argv[0], "r")
    dest = open(argv[0].replace(".vm",".asm"), "w")
    hackDict = {'add':printAdd, 'sub':printSub, 'neg':printNeg, 'eq':printEq, 'gt':printGt, 'lt':printLt, 'and':printAnd, 'or':printOr, 'not':printNot, 'push':printPush, 'pop':printPop}
    lno = 1;
    IC = 0;
    for line in src:
        lno = lno + 1;
        line = re.sub(r'\/\/.*','',line)
        if line == "\n" or re.match(r'^\s+$',line):
            continue
        cList = line.split()
        funcName = cList[0]
        hackDict[funcName](cList[1:])


if __name__ == '__main__':
    processVM(sys.argv[1:])

