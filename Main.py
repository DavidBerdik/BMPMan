#!/usr/bin/env python2.7

from __future__ import print_function
import binascii
import gc
import os
import re

version = "1.1.0"

Output1 = 'Output_Images/'
Output2 = 'Output_Data/'
Input = 'Input_Images/'
Input2 = 'Input_Data/'

def wipe():
    os.system('cls' if os.name == 'nt' else 'clear')



def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort_n(l):
    l.sort(key=alphanum_key)


def generic_upd2():
    lim = 48000000
    ext = ".bmp"
    files = os.listdir(Input2)
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer = ''
    name_dig = 0
    print("Digesting Data...\n")
    for name in files:
        filename = name
        with open(Input2 + str(filename), 'rb') as byter:
            content = byter.read()
            byter.close()
        print("Building Buffer...\n")
        for letter in content:
            buffer += str(letter)
            if len(buffer) == lim:
                file = str(filename) + "-" + str(name_dig) + str(ext)
                with open(Output1 + str(file), 'wb') as byteman:
                    byteman.write(base)
                    byteman.write('0' * 32)
                    byteman.write(buffer)
                    byteman.close()
                print("Buffer Flushed To " + str(file) + "\n")
                name_dig += 1
                buffer = ''
                gc.collect()
        file = str(filename) + '-' + str(name_dig) + str(ext)
        with open(Output1 + str(file), 'wb') as byteman:
            byteman.write(base)
            byteman.write('0' * 32)
            byteman.write(buffer)
            byteman.close()
        print("Buffer Flushed To " + str(file) + "\n")
        name_dig += 1
        buffer = ''
        gc.collect()
        name_dig = 0
        print("Process Complete!\n")


def rip_upd2():
    namefile = os.listdir(Input)
    sort_n(namefile)
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer = str('0' * 32)
    dig = 0
    for name in namefile:
        if namefile[dig] in name:
            filename = name
            with open(Input + str(filename), 'rb') as generic:
                content = generic.read()
            temp = ''
            data = ''
            print("Stripping Header...")
            for line in content:
                temp += line
                if len(temp) <= int(len(base) + len(buffer)):
                    print("", end='')
                    if len(temp) == int(len(base) + len(buffer)):
                        print("Header Removed!\n")
                        print("Building File Data From " + str(filename) + "...\n")
                else:
                    data += line
            print("Building File...\n")
            temp_name = namefile[dig].split('-')
            with open(Output2 + str(temp_name[0]), 'ab') as out:
                out.write(data)
            gc.collect()
            #wipe()
        else:
            print("", end='')
        dig += 1
    print("Process Complete!\n")


def gen():
    for i in range(10):
        sen = ''
        for i in range(10000000):
            sen += '0'
        with open("dummy", 'a') as dummy:
            dummy.write(str(sen))
            dummy.close()


def initiate():
    if not os.path.exists(Output1):
        os.makedirs(Output1)
    if not os.path.exists(Output2):
        os.makedirs(Output2)
    if not os.path.exists(Input):
        os.makedirs(Input)
    if not os.path.exists(Input2):
        os.makedirs(Input2)
    print("Created Directories!\n")


initiate()
print("||Version||\n" + str(version) + "\n")
print("|Possible Commands|\n")
print(">> make | Makes BMP files 'Output_Images' out of data in 'Input_Data'")
print(">> unpack | Unpacks data from BMP 'Input_Images' into the original file 'Output_Data\n")
user_choice = raw_input("Command: ")
if user_choice == str("make"):
    wipe()
    generic_upd2()
elif user_choice == str("unpack"):
    wipe()
    rip_upd2()
elif user_choice == str("gen"):
    wipe()
    gen()
else:
    print("Error")
