#!c:\\python\\python.exe

'''
todo:
    - expand mutate with flag to toggle between smart, full and random.
    - make sizers fuzzable
    - add dependencies (conditionals)
    - expand parameter types from white board
    - address TODOs
    - text sizers? ie: content-length from http
'''

from sulley import *

import base64

s_initialize("packet 1")

s_qword(0xdeadbeefdeadbeef)
s_static(">>>")
s_dword(0xdeadbeef, endian=BIG_ENDIAN)
s_static(">>>")
s_short(0xdead, name="i'm a short")
s_static(">>>")
s_byte(0xde)
s_static(">>>")

s_sizer("header")
s_static(">>>")
if s_block_start("header", base64.b64encode):
    s_static("pedram amini")
    s_static(" is the coolest")
    s_short(0xdead)
    s_byte(0xde)
    s_string("pedram")
    s_block_end()

s_static(">>>")
s_sizer("body")
s_static(">>>")
s_checksum("body")
s_static(">>>")
if s_block_start("body"):
    s_static(" weeee")
    s_static(">>>")
    s_qword(0xdeadbeefdeadbeef, name="changeme", endian=BIG_ENDIAN)
    s_static(">>>")
    s_dword(0xdeadbeef)
    s_static(">>>")
    s_short(0xdead)
    s_static(">>>")
    s_block_end()
    if s_block_start("embedded"):
        s_delim("@")
        s_static(">>>")
        s_random("random", 10, 40)
        s_static(">>>")
        s_string("pedram")
        s_static(">>>")
        s_block_end()

s_static(">>>")
s_checksum("body")
s_static(">>>")
s_static(" footer")    
s_static(">>>")
s_static(" final.")
s_static(">>>")

import md5
digests = {}

while 1:
    print "[%d of %d]\r" % (blocks.CURRENT.mutant_index, blocks.CURRENT.num_mutations()),
    data   = s_render()
    digest = md5.md5(data).digest()
    
    if digests.has_key(digest):
        print "DUP ALERT"
    
    digests[digest] = 1
    
    if not s_mutate():
        print
        break

print len(digests.keys())

#s_update("changeme", 0xaaaaaaaaaaaaaa)
#print s_render()
#s_mutate()
#print "." * 80
#print s_render()
