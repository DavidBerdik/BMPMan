#!/usr/bin/env python2.7

from __future__ import print_function
import binascii
import gc

def generic_upd():
    lim = 48000000
    ext = ".bmp"
    filename = raw_input("Filename: ")
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer = ''
    name_dig = 0
    print("Digesting Data...\n")
    with open(filename, 'rb') as byter:
        content = byter.read()
        byter.close()
    print("Building Buffer...\n")
    for letter in content:
        buffer += str(letter)
        if len(buffer) == lim:
            file = str(filename) + str(name_dig) + str(ext)
            with open(file, 'wb') as byteman:
                byteman.write(base)
                byteman.write('0' * 32)
                byteman.write(buffer)
                byteman.close()
            print("Buffer Flushed To " + str(file) + "\n")
            name_dig += 1
            buffer = ''
            gc.collect()
    file = str(filename) + str(name_dig) + str(ext)
    with open(file, 'wb') as byteman:
        byteman.write(base)
        byteman.write('0' * 32)
        byteman.write(buffer)
        byteman.close()
    print("Buffer Flushed To " + str(file) + "\n")
    name_dig += 1
    buffer = ''
    gc.collect()
    print("Process Complete!\n")

def rip_upd():
    name = raw_input("Parts (include 0): ")
    outname = raw_input("FileName: ")
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer = str('0' * 32)
    for i in range(int(name)):
        filename = str(outname) + str(i) + str(".bmp")
        with open(filename, 'rb') as generic:
            content = generic.read()
        temp = ''
        data = ''
        print("Processing File " + str(filename) + "\n")
        print("Stripping Header...")
        for line in content:
            temp += line
            if len(temp) <= int(len(base) + len(buffer)):
                print("", end='')
                if len(temp) == int(len(base) + len(buffer)):
                    print("Header Removed!\n")
                    print("Building File Data...\n")
            else:
                data += line
        print("Building File...\n")
        with open(outname, 'ab') as out:
            out.write(data)
        gc.collect()
    print("Process Complete!\n")

def gen():
    sen = ''
    for i in range(100000000):
        sen += '0'
    with open("dummy", 'w') as dummy:
        dummy.write(str(sen))
        dummy.close()

print("|Possible Commands|\n")
print(">> make | Makes BMP files out of data")
print(">> unpack | Unpacks data from BMP into the original file\n")
user_choice = raw_input("Command: ")
if user_choice ==  str("make"):
    generic_upd()
elif user_choice == str("unpack"):
    rip_upd()
elif user_choice == str("gen"):
    gen()
else:
    print("Error")
