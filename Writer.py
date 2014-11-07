# Dillon Yeh

import sys
import re
class VMWriter:

    def __init__(self, filename):
        self.name = filename
        self.fileHandle = open(filename, "w")
        self.labelCount = 0
        self.errCount = 0
        self.outString = ";" + filename + "\n"

    def prepare(self, string):
        self.outString = self.outString + string + "\n"

    def write(self):
        if self.errCount > 0:
            sys.exit(1)
        self.fileHandle.write(self.outString)

    def genLabel(self, string):
        temp = string + "." + '{:0>4}'.format(self.labelCount)
        self.labelCount = self.labelCount + 1
        return temp
    
    def error(self, string):
        print(string)
        self.errCount = self.errCount + 1
