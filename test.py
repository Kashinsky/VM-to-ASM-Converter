#!/usr/bin/python
import re
lno = 1
#comment_regex = re.compile('\/\/.*')
fh = open("tests/BasicTest.vm", "r")
print "-----------------------------"
for line in fh:
    line = re.sub(r'\/\/.*','',line)
    if line == "\n" or re.match(r'^\s+$',line):
        continue;
    print str(lno),line,
    lno = lno+1

print "----------------------------"
