#!/usr/bin/env python2.7

from __future__ import print_function
import binascii
import gc
import os
import re
import sys
import hashlib
import json
import PySimpleGUI27 as sg
import time
from multiprocessing.dummy import Pool
from multiprocessing import *

version = "1.2.0"

Output1 = r'Output_Images/'
Output2 = r'Output_Data/'
Input = r'Input_Images/'
Input2 = r'Input_Data/'


#def hash_check_image():




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


def generic_upd2(files):
    lim = 48000000
    ext = ".bmp"
    #files = os.listdir(Input2)
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer = ''
    name_dig = 0
    current = 0
    #mylist = []
    #mylist.append(files)
    print("Digesting Data...\n")
    for i in range(len(files)):#name in files:
        sg.OneLineProgressMeter('Progress', current, len(files), 'key')
        filename = files[i]
        with open("file_hashes", 'r') as hashes:
            crypt = json.load(hashes)
            hashes.close()
        with open(Input2 + str(filename), 'r') as data:
            bytes_ = data.read()
            crypt[name] = str(hashlib.sha256(str(bytes_)).hexdigest())
            data.close()
        with open("file_hashes", 'w') as hashes2:
            json.dump(crypt, hashes2, indent=3)
            hashes2.close()
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
        file = str(filename) + '-' + str(name_dig) + str(ext)
        with open(Output1 + str(file), 'wb') as byteman:
            byteman.write(base)
            byteman.write('0' * 32)
            byteman.write(buffer)
            byteman.close()
        with open(Output1 + str(file), 'r') as main_hash:
            hash_data = main_hash.read()
            main_hash.close()
        #with open("image_hashes", 'r') as init1:
        print("Buffer Flushed To " + str(file) + "\n")
        name_dig += 1
        buffer = ''
        name_dig = 0
        current += 1
        print("Process Complete!\n")

    sg.Popup("Complete!\n", "Images Output: " + str(current), "Output Location: " + str(Output1))


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
        print("Created Directory %s" % Output1)
    if not os.path.exists(Output2):
        os.makedirs(Output2)
        print("Created Directory %s" % Output2)
    if not os.path.exists(Input):
        os.makedirs(Input)
        print("Created Directory %s" % Input)
    if not os.path.exists(Input2):
        os.makedirs(Input2)
        print("Created Directory %s" % Input2)


initiate()
#gen()


#if len(sys.argv) == 0:

if len(sys.argv) > 1:
    command = str(sys.argv[1])
    if command == "make":
        wipe()
        files = os.listdir(Input2)
        for name in files:
            Process(generic_upd2(name)).start()
    elif command == "unpack":
        wipe()
        rip_upd2()
    else:
        print("Incorrect Arguments Given!\n")
else:
    layout = [[sg.Text('Source Folder', justification='right'), sg.InputText('Input'),
               sg.FolderBrowse()],
              [sg.Text('Destination Folder', justification='right'), sg.InputText('Output'),
               sg.FolderBrowse()],
              [sg.Button('Make', button_color=('white', 'red')), sg.Button('Unpack', button_color=('white', 'green')), sg.Cancel()]]
    window = sg.Window('Test').Layout(layout)
    event, values = window.Read()
    if str(event) == "Make":
        if str(values[0]) != "Input" and str(values[1]) != "Output":
            Input2 = str(values[0]).replace('\\', '/') + "/"
            Output1 = str(values[1]).replace('\\', '/') + "/"
            files = os.listdir(Input2)
            print(files)

            name_list = []
            for name in files:
                name_list.append(str(name))
            window.Close()
            Process(generic_upd2(name_list)).start()
            #print(name_list)
            #time.sleep(10)
            #for i in range(len(name_list)):
            #    print(name_list[i])
            #    temp = str(name_list[i])
            #    Process(generic_upd2(temp)).start()
            #generic_upd2(files)
        elif str(values[0]) == "Input" and str(values[1]) == "Output":
            files = os.listdir(Input2)
            print(files)

            name_list = []
            for name in files:
                name_list.append(str(name))
            window.Close()
            Process(generic_upd2(name_list)).start()
            #print(name_list)
            #time.sleep(10)
            #for i in range(len(name_list)):
            #    print(name_list[i])
            #    temp = str(name_list[i])
            #    Process(generic_upd2(name_list)).start()
    elif str(event) == "Unpack":
        if str(values[0]) is not "Input" and str(values[1]) is not "Output":
            Input = str(values[0])
            Output2 = str(values[1])
