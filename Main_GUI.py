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

version = "1.3.2"

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


def generic_upd2(files):
    lim = 48000000
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer_ = []
    name_dig = 0
    current = 0
    event = True
    file_lim = len(files) - 1
    blob = str("0" * 32)
    while event:
        event = sg.OneLineProgressMeter('Progress', current, len(files), 'key')
        filename = files[current]
        if current == file_lim:
            event = False
        content = open("{}{}".format(Input2, str(filename)), 'rb').read()
        for letter in content:
            buffer_.append(str(letter))
            if len(buffer_) == lim:
                file_ = "{}{}-{}.bmp".format(str(Output1), str(filename), str(current))
                open(file_, 'wb').write("{}{}{}".format(base, blob, ''.join(buffer_)))
                name_dig += 1
                buffer_ = []
        file_ = "{}{}-{}.bmp".format(str(Output1), str(filename), str(current))
        open(file_, 'wb').write("{}{}{}".format(base, blob, ''.join(buffer_)))
        name_dig += 1
        buffer_ = []
        current += 1
    check_value = current / len(files)
    if check_value == 1:
        sg.Popup("Complete!", "Images Output: " + str(current), "Output Location: " + str(Output1))
    else:
        delete(str(Output1))
        sg.Popup("Cancled!", "The process has been stopped by a user, partially written data has automatically been deleted")



def rip_upd2(name):
    sort_n(name)
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer_ = str('0' * 32)
    dig = 0
    event = True
    file_lim = len(name) - 1
    while event:
        event = sg.OneLineProgressMeter('Build Progress', dig, len(name), 'key')
        if dig == file_lim:
            event = False
        if name[dig] in name:
            content = open("{}{}".format(Input, str(name[dig])), 'rb').read()
            temp = []
            data = []
            base_buf = int(len(base) + len(buffer_))
            for line in content:
                temp.append("0")
                if len(temp) <= base_buf:
                    print("", end='')
                else:
                    data.append(line)
            temp_name = name[dig].split('-')
            file_ = "{}{}".format(Output2, str(temp_name[0]))
            output_data = ''.join(data)
            open(file_, 'ab').write(output_data)
        else:
            print("", end='')
        dig += 1
    check_value = dig / len(files)
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
layout = [[sg.Text('Source Folder', justification='right'), sg.InputText('Input'),
           sg.FolderBrowse()],
          [sg.Text('Destination Folder', justification='right'), sg.InputText('Output'),
           sg.FolderBrowse()],
          [sg.Button('Make', button_color=('white', 'red')), sg.Button('Unpack', button_color=('white', 'green')), sg.Cancel()]]

window = sg.Window('BMPMan V.{}'.format(version)).Layout(layout)

event, values = window.Read()

if str(event) == "Make":
    if str(values[0]) != "Input" and str(values[1]) != "Output":
        Input2 = "{}/".format(str(values[0]).replace('\\', '/'))
        Output1 = "{}/".format(str(values[1]).replace('\\', '/'))
        files = os.listdir(Input2)
        name_list = [str(name) for name in files]
        window.Close()
        generic_upd2(name_list)
    elif str(values[0]) == "Input" and str(values[1]) == "Output":
        files = os.listdir(Input2)
        name_list = [str(name) for name in files]
        window.Close()
        generic_upd2(name_list)
elif str(event) == "Unpack":
    if str(values[0]) != "Input" and str(values[1]) != "Output":
        Input = "{}/".format(str(values[0]).replace('\\', '/'))
        Output2 = "{}/".format(str(values[1]).replace('\\', '/'))
        files = os.listdir(Input)
        name_list = [str(name) for name in files]
        window.Close()
        rip_upd2(name_list)
    elif str(values[0]) == "Input" and str(values[1]) == "Output":
        files = os.listdir(Input)
        name_list = [str(name) for name in files]
        window.Close()
        rip_upd2(name_list)
