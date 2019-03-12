#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from __future__ import print_function
import binascii
import os
import re
import sys
import hashlib
import json
import PySimpleGUI27 as sg
import time
import sys
from Tkinter import *
import UserList
import commands
import UserString
import _tkinter
import tkinter as tk

version = "1.4.0"

Output1 = 'Output_Images/'
Output2 = 'Output_Data/'
Input = 'Input_Images/'
Input2 = 'Input_Data/'


#def hash_check_image():

def delete(directory):
    try:
        os.system("rm -r {}*".format(directory))
    except:
        os.system("del /S {}*".format(directory))


def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort_n(l):
    l.sort(key=alphanum_key)


def chunk(file_, chunk_size=48000000):
    keys = []
    name_ = "{}{}".format(Input2, str(files[0]))
    data_val = (int(os.path.getsize(name_)))
    out_num = int(data_val // chunk_size)
    out_rem = int(data_val % chunk_size)
    if out_rem > 0:
        out_num += 1
    for i in xrange(0, out_num, 1):
        data = file_.read(chunk_size)
        if not data:
            data = file_.read(out_rem)
        yield data


def generic_upd3(files):
    print("DEBUG: Process Start!")
    lim = 48000000
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer_ = ''
    name_dig = 0
    current = 0
    event = True
    file_lim = len(files) - 1
    blob = str("00000000000000000000000000000000")
    keys = []
    name_ = "{}{}".format(Input2, str(files[0]))
    data_val = (int(os.path.getsize(name_)))
    out_num = int(data_val // lim)
    print("DEBUG: Out_Num_Start = " + str(out_num))
    out_rem = int(data_val % lim)
    if out_rem > 0:
        out_num += 1
    print("DEBUG: Out_Rem = " + str(out_rem) + " Bytes")
    print("DEBUG: Out_Num_End = " + str(out_num))
    keys.append(out_num)
    num_total = sum(keys, 0)
    file_x = open(name_, 'rb')
    payload = chunk(file_x)
    for piece in payload: #chunk(file_):
        event = sg.OneLineProgressMeter('Build Progress', name_dig, out_num, 'key')
        print("DEBUG: Current = " + str(current))
        filename = files[current]
        print("DEBUG: Working With File | " + str(filename))
        data_blob = os.path.getsize("{}{}".format(Input2, str(filename)))
        print("DEBUG: Expected Output Files = " + str(num_total))
        print("DEBUG: Progress Bar Started!")
        if name_dig == num_total or not event:
            event = False
            print("DEBUG: Process Should Be Stopped!")
            break
        else:
            pass
        file_ = "{}{}-{}.bmp".format(str(Output1), str(filename), str(name_dig))
        name_dig += 1
        open(file_, 'wb').write("{}{}{}".format(base, blob, piece))
        print("DEBUG: Buffer Flushed to " + str(file_) + "!")
        print("DEBUG: Buffer Size = " + str(len(piece)))
        print("DEBUG: File Name = " + str(filename))
    if name_dig == num_total:
        sg.Popup("Complete!", "Images Output: " + str(name_dig), "Output Location: " + str(Output1))
    else:
        delete(str(Output1))
        sg.Popup("Cancled!", "The process has been stopped by a user, partially written data has automatically been deleted")


def rip_upd3(name):
    print("DEBUG: Initializing...")
    print("DEBUG: Stripping Non-BMP Files")
    for i in xrange(0, len(name), 1):
        if ".bmp" not in name[i]:
            print("DEBUG: File " + str(name[i]) + " Removed From List!")
            del name[i]
    sort_n(name)
    print("DEBUG: List Sorted")
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer_ = str('00000000000000000000000000000000')
    dig = 0
    event = True
    file_lim = len(name) - 1
    file_len = len(name)
    print("DEBUG: File_Lim = " + str(file_lim))
    print("DEBUG: File_Len = " + str(len(name)))
    file_len = len(name)
    for i in xrange(0, file_len, 1):
        event = sg.OneLineProgressMeter('Build Progress', dig, len(name), 'key')
        if dig == file_len or not event:
            print("DEBUG: Process Should Stop")
            break
        content = open("{}{}".format(Input, str(name[dig])), 'rb').read()
        print("DEBUG: Reading File " + str(name[dig]))
        temp_name = name[dig].split('-')
        file_ = "{}{}".format(Output2, str(temp_name[0]))
        print("DEBUG: File " + str(temp_name[0]) + " Processing")
        open(file_, 'ab').write(content[96:])
        print("DEBUG: Dig = " + str(dig))
        dig += 1
        print("DEBUG: Payload Dumped")
    check_value = dig / file_lim
    if check_value == 1:
        sg.Popup("Complete!", "Data Output: " + str(len(os.listdir(Output2))), "Output Location: " + str(Output2))
    else:
        delete(str(Output2))
        sg.Popup("Cancled!", "The process has been stopped by a user, partially written data has automatically been deleted")


def gen():
    for i in xrange(0, 10, 1):
        sen = []
        for u in xrange(0, 10000000, 1):
            sen.append("0")
        open("dummy", 'a').write(''.join(sen))


def initiate():
    if not os.path.exists(Output1):
        os.makedirs(Output1)
    if not os.path.exists(Output2):
        os.makedirs(Output2)
    if not os.path.exists(Input):
        os.makedirs(Input)
    if not os.path.exists(Input2):
        os.makedirs(Input2)


initiate()
layout = [[sg.Text('Input', justification='right'), sg.InputText('Use_Default'),
           sg.FolderBrowse()],
          [sg.Text('Output', justification='right'), sg.InputText('Use_Default'),
           sg.FolderBrowse()],
          [sg.Button('Make', button_color=('white', 'red')), sg.Button('Unpack', button_color=('white', 'green')), sg.Cancel()]]

window = sg.Window('BMPMan V.{}'.format(version)).Layout(layout)

event, values = window.Read()

if str(event) == "Make":
    if str(values[0]) != "Use_Default" and str(values[1]) != "Use_Default":
        Input2 = "{}/".format(str(values[0]).replace('\\', '/'))
        Output1 = "{}/".format(str(values[1]).replace('\\', '/'))
        files = os.listdir(Input2)
        name_list = [str(name) for name in files]
        window.Close()
        generic_upd3(name_list)
    elif str(values[0]) == "Use_Default" and str(values[1]) == "Use_Default":
        files = os.listdir(Input2)
        name_list = [str(name) for name in files]
        window.Close()
        generic_upd3(name_list)
elif str(event) == "Unpack":
    if str(values[0]) != "Use_Default" and str(values[1]) != "Use_Default":
        Input = "{}/".format(str(values[0]).replace('\\', '/'))
        Output2 = "{}/".format(str(values[1]).replace('\\', '/'))
        files = os.listdir(Input)
        name_list = [str(name) for name in files]
        window.Close()
        rip_upd3(name_list)
    elif str(values[0]) == "Use_Default" and str(values[1]) == "Use_Default":
        files = os.listdir(Input)
        name_list = [str(name) for name in files]
        window.Close()
        rip_upd3(name_list)
