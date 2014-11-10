# Dillon Yeh
#
# Writer.py defines a class that stores potential assembly code and prints the
# code to the specified filename only if there are no errors.

import sys
import re
class VMWriter:

    def __init__(self, filename):
        self.name = filename # the name of the file to be written to
        self.fileHandle = open(filename, "w")
        self.labelCount = 0 # the total number of labels (0 indexed)
        self.errCount = 0 # the number of errors found
        self.outString = "//" + filename + "\n" # the string containing all the
                                                # asm code

    # Param: string, the string to be appended to the output string
    def prepare(self, string):
        self.outString = self.outString + string + "\n"

    # Writes outstring to the file if there are no errors
    # the number of errors are printed if there are any
    def write(self):
        if self.errCount > 0:
            print("Number of errors: " + str(self.errCount))
            sys.exit(1)
        self.fileHandle.write(self.outString)

    # Param: string, the general label to be "uniquified"
    # Return: temp, the uniquified label
    def genLabel(self, string):
        temp = string + "." + '{:0>4}'.format(self.labelCount)
        self.labelCount = self.labelCount + 1
        return temp
    
    # Increments error counts and prints passed error message
    # Param: string, the error message
    def error(self, string):
        print(string)
        self.errCount = self.errCount + 1

    
