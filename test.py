#!/usr/bin/python
import re
import sys
lno = 1


src = open("tests/BasicTest.vm", "r")
for line in src:
    line = re.sub(r'\/\/.*','',line)
    if line == "\n" or re.match(r'^\s+$',line):
        continue;
    print str(lno),line,
    lno = lno+1


