# Dillon Yeh
#
# Reader.py defines a class that opens a file handle on a file defined on
# construction. It's only function, next, will return the next VM instruction
# found in the file. It also has fields associated with line number and 
# instruction counter.

import sys
import re
class VMReader:
    def __init__(self, filename):
        self.name = filename
        self.fileHandle = open(filename, "r")
        self.lno = 0
        self.IC = 0
        self.labelCount
    
    # Returns: lst, an array containing the next vm instruction in the file
    #               split by whitespace
    def next(self):
        line = self.fileHandle.readline()
        if not line:
            return "**EOF**"
        line = re.sub(r'\/\/.*','',line)
        self.lno = self.lno + 1
        regex = re.compile(r'^\s+$')
        while regex.match(line):
            line = self.fileHandle.readline()
            line = re.sub(r'\/\/.*','',line)
            self.lno = self.lno + 1
        self.IC = self.IC + 1
        lst = line.split()
        return lst
