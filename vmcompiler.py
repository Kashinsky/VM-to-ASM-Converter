# Name:
#   Dillon Yeh <yehda194@potsdam.edu>
# File:
#   vmcompiler.py
# Description:
#   Program is designed to parse nand2tetris vm code and produce the
#   corresponding assembly code.
# Command Line:
#   The .vm file to be parsed

#!/usr/bin/python
import sys, getopt, re
from Reader import VMReader
from Writer import VMWriter

# Writes the assembly code associated with the add operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printAdd(args, lno, writer):
    if len(args) > 0:
        writer.error("Add does not take args at line " + lno)
        return
    writer.prepare("//--add--")
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=M')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=D+M')
    writer.prepare('M=D')
    writer.prepare('@SP')
    writer.prepare('M=M+1')

# Writes the assembly code associated with the sub operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printSub(args, lno, writer):
    if len(args) > 0:
        writer.error("Sub does not take args at line " + lno)
        return
    writer.prepare('//--subtract--')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=M')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=D-M')
    writer.prepare('M=D')
    writer.prepare('@SP')
    writer.prepare('M=M+1')

# Writes the assembly code associated with the neg operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printNeg(args, lno, writer):
    if len(args) > 0:
        writer.error("Neg does not take args at line" + lno)
        return
    writer.prepare('//--negate--')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('M=-M')
    writer.prepare('@SP')
    writer.prepare('M=M+1')


# Writes the assembly code associated with the eq operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printEq(args, lno, writer):
    if len(args) > 0:
        writer.error("Eq does not take args at line" + lno)
        return
    writer.prepare('//--equals--')
    prepareComparison(writer)
    passL = writer.genLabel("eq.pass")
    afterL = writer.genLabel("eq.after")
    printComparison(writer, 'D;JEQ', passL, afterL)

# Writes the assembly code associated with the gt operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printGt(args, lno, writer):
    if len(args) > 0:
        writer.error("GT does not take args at line" + lno)
        return
    writer.prepare('//--greater than--')
    prepareComparison(writer)
    passL = writer.genLabel("gt.pass")
    afterL = writer.genLabel("gt.after")
    printComparison(writer, 'D;JGT', passL, afterL)

# Writes the assembly code associated with the lt operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printLt(args, lno, writer):
    if len(args) > 0:
        writer.error("Lt does not take args at line" + lno)
        return
    writer.prepare('//--less than--')
    prepareComparison(writer)
    passL = writer.genLabel("gt.pass")
    afterL = writer.genLabel("gt.after")
    printComparison(writer, 'D;JLT', passL, afterL)

# Writes the assembly code associated with the and operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printAnd(args, lno, writer):
    if len(args) > 0:
        writer.error("And does not take args at line" + lno)
        return
    writer.prepare('//--And--')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=M')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=D&M')
    writer.prepare('M=D')
    writer.prepare('@SP')
    writer.prepare('M=M+1')

# Writes the assembly code associated with the or operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printOr(args, lno, writer):
    if len(args) > 0:
        writer.error("Or does not take args at line" + lno)
        return
    writer.prepare('//--Or--')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=M')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=D|M')
    writer.prepare('M=D')
    writer.prepare('@SP')
    writer.prepare('M=M+1')


# Writes the assembly code associated with the not operation
# to the writer object.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printNot(args, lno, writer):
    if len(args) > 0:
        writer.error("Not does not take args at line" + lno)
        return
    writer.prepare('//--Not--')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('M=!M')
    writer.prepare('@SP')
    writer.prepare('M=M+1')


# Calls appropriate methods to print the assembly instructions for each
# memory segment and formats the arguments accordingly to asm code
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printPush(args, lno, writer):
    if len(args) > 2:
        writer.error("Push must take two args at line " + lno)
        return
    # Checks if decimal argument is negative. Writes an error if it is. 
    if int(args[1]) < 0:
        writer.error("Cannot have a negative offset at line " + lno )
        return
    writer.prepare('//--Pushing ' + args[0] + ' ' +  args[1] + '--')
    if args[0] == "constant":
        writer.prepare("@" + args[1])
        writer.prepare("D=A")
        writer.prepare("@SP")
        writer.prepare("A=M")
        writer.prepare("M=D")
        writer.prepare("@SP")
        writer.prepare("M=M+1")
    elif args[0] == "static":
        if int(args[1]) > 238:
            writer.error("Static value cannot exceed 238 at line " + lno)
            return
        handleOffsetPush(args[1], 16, writer)
    elif args[0] == "temp":
        if int(args[1]) > 7:
            writer.error("Temp value cannot exceed 7 at line " + lno)
            return
        handleOffsetPush(args[1], 5, writer)
    elif args[0] == "pointer":
        if int(args[1]) > 1:
            writer.error("Pointer value cannot exceed 1 at line " + lno)
        handleOffsetPush(args[1], 3, writer)
    else:
        handleNamedPush(args, lno, writer)

# Calls appropriate methods to print the asm code representing the pop
# operation for each memory segment and formats the arguments
# accordingly to asm code.
# Params: args, the command line arguments associated with the operation
#         lno, the integer containing the line number the operation was seen on
#         writer, the VMWriter object tasked with storing the expected output string
def printPop(args, lno, writer):
    if len(args) > 2: 
        writer.error("Pop must take two args")
        return
    if int(args[1]) < 0:
        writer.error("Cannot have a negative offset at line " + lno)
    writer.prepare('//--Popping to ' + args[0] + ' ' + args[1] + '--')
    if args[0] == "static":
        if int(args[1]) > 238:
            writer.error("Static value cannot exceed 238 at line " + lno)
            return
        handleOffsetPop(args[1], 16, writer)
    elif args[0] == "temp":
        if int(args[1]) > 7:
            writer.error("Temp value cannot exceed 7 at line " + lno)
            return
        handleOffsetPop(args[1], 5, writer)
    elif args[0] == "pointer":
        if int(args[1]) > 1:
            writer.error("Pointer value cannot exceed 1 at line " + lno)
        handleOffsetPop(args[1], 3, writer)
    else:
         handleNamedPop(args, lno, writer)
    writer.prepare("@SP")
    writer.prepare("AM=M-1")
    writer.prepare("D=M")
    writer.prepare("@14")
    writer.prepare("A=M")
    writer.prepare("M=D")


# Prints the correctly formatted pop command that is not using a
# built in label in hack assemblr
# Params: offset, the string representing the integer offset
#         base, the integer containing the location of the 1st location of
#               the not built in label
#         writer, the VMWriter object tasked with storing the output string
def handleOffsetPop(offset, base, writer):
    loc = str(int(offset) + base)
    writer.prepare("@" + loc)
    writer.prepare("D=A")
    writer.prepare("@14")
    writer.prepare("M=D")

# Writes the assembly code associated with the pop command when using
# hack assembler built in labels to the writer object's output string
# Params: args, the array containing the arguments associated the pop operation
#         lno, the line number the pop operation was seen
#         writer, the VMWriter object tasked with storing the output string
def handleNamedPop(args, lno, writer):
    reservedLocs = {
        "argument":"ARG",
        "local":"LCL",
        "this":"THIS",
        "that":"THAT",
    }
    if not(args[0] in reservedLocs):
        writer.error("Invalid pop argument " + args[0] + " at line " + lno)
        return
    baseLoc = reservedLocs[args[0]]
    writer.prepare("@" + args[1])
    writer.prepare("D=A")
    writer.prepare("@" + baseLoc)
    writer.prepare("D=D+M")
    writer.prepare("@14")
    writer.prepare("M=D")

# Prints the correctly formatted push command that is not using a
# built in label in hack assembler
# Params: offset, the string representing the integer offset
#         base, the integer containing the location of the 1st location of
#               the not built in label
#         writer, the VMWriter object tasked with storing the output string
def handleOffsetPush(offset, base, writer):
        loc = str(int(offset) + base)
        writer.prepare("@" + loc)
        writer.prepare("D=M")
        writer.prepare("@SP")
        writer.prepare("A=M")
        writer.prepare("M=D")
        writer.prepare("@SP")
        writer.prepare("M=M+1")

# Writes the assembly code associated with the push command when using
# hack assembler built in labels to the writer object's output string.
# Params: args, the array containing the arguments associated the pop operation
#         lno, the line number the pop operation was seen
#         writer, the VMWriter object tasked with storing the output string
def handleNamedPush(args, lno, writer):
    reservedLocs = {
        "argument":"ARG",
        "local":"LCL",
        "this":"THIS",
        "that":"THAT",
    }
    if not (args[0] in reservedLocs):
        writer.error("Invalid push argument " + args[0] + " at line " + lno)
        return
    baseLoc = reservedLocs[args[0]]
    writer.prepare("@" + baseLoc)
    writer.prepare("D=M")
    writer.prepare("@" + args[1])
    writer.prepare("D=D+A")
    writer.prepare("A=D")
    writer.prepare("D=M")
    writer.prepare("@SP")
    writer.prepare("A=M")
    writer.prepare("M=D")
    writer.prepare("@SP")
    writer.prepare("M=M+1")


# Writes the assembly code associated with comparisions.
# Params: writer, the VMWriter object tasked with storing the output string
#         jumpType, the string specifying the type of assembly comparision
#                   needed to be performed
#         passL, the string representing the label used when a value passes
#                a comparision
#         afterL, the string representing the label jumped to at the end of
#                 a comparision  
def printComparison(writer, jumpType, passL, afterL):
    writer.prepare('@' + passL)
    writer.prepare(jumpType)
    writer.prepare('@SP')
    writer.prepare('A=M')
    writer.prepare('M=0')
    writer.prepare('@SP')
    writer.prepare('M=M+1')
    writer.prepare('@' + afterL)
    writer.prepare('0;JMP')
    writer.prepare('(' + passL + ')')
    writer.prepare('@SP')
    writer.prepare('A=M')
    writer.prepare('M=-1')
    writer.prepare('@SP')
    writer.prepare('M=M+1')
    writer.prepare('(' + afterL + ')')


# Writes the assembly preparations for comparisions
# Param: writer, the VMWriter object tasked with storing the output string
def prepareComparison(writer):
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=M')
    writer.prepare('@13')
    writer.prepare('M=D')
    writer.prepare('@SP')
    writer.prepare('AM=M-1')
    writer.prepare('D=M')
    writer.prepare('@13')
    writer.prepare('D=D-M')

# Main loop that takes string read from VMReader object and calls the
# correct function to print the correct assembly instructions
# Param: argv, the string containing the target vm file to be parsed
def processVM(argv):
    reader = VMReader(argv[0])
    writer = VMWriter(re.sub(r'.vm$','.asm',argv[0]))
    writer.prepare("@256\nD=A\n@SP\nM=D")
    hackDict = {
            'add':printAdd,
            'sub':printSub,
            'neg':printNeg,
            'eq':printEq,
            'gt':printGt,
            'lt':printLt,
            'and':printAnd,
            'or':printOr,
            'not':printNot,
            'push':printPush,
            'pop':printPop
    }
    line = reader.next()
    while line != "**EOF**":
        if not(line[0] in hackDict):
            writer.error("Cannot find symbol " + line[0] +
                         " at line " + reader.lno)
            continue
        entry = hackDict[line[0]]
        entry(line[1:], reader.lno, writer)
        line = reader.next()
    writer.prepare("(end)\n@end\n0;JMP")
    writer.write()

if __name__ == '__main__':
    processVM(sys.argv[1:])

