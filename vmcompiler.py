#!/usr/bin/python
import sys, getopt, re


# Calls the error message function with the programs usage
def printUsage(errCode):
    printerr("USAGE: python vmcompiler.py [-h][-l][-d] <file.vm>",errCode)

# Prints passed error message with the specified error code
def printerr(message, errCode):
    print message,"\n",
    sys.exit(errCode)

def processVM(argv):
    scr = open(argv[0], "r")
    hackDict = {'add':printAdd, 'sub':printSub, 'neg':printNeg, 'eq':printEq, 'gt':printGt, 'lt':printLt, 'and':printAnd, 'or':printOr, 'not':printNot, 'push':printPush, 'pop':printPop}
    lno = 0;
    for line in src:
        line = re.sub(r'\/\/.*','',line)
        if line == "\n" or re.match(r'^\s+$',line):
            continue
        
def main(argv):
    printHack(argv)
    


main(sys.argv[1:])

