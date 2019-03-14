
from __future__ import print_function
import binascii
import os
import re
import sys
import hashlib
import json
import codecs
try:
    import PySimpleGUI27 as sg
except:
    import PySimpleGUI as sg
import time
import sys
try:
    from Tkinter import *
    import UserList
    import commands
    import UserString

except:
    pass
import _tkinter
import tkinter as tk


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


def chunk(file_, name_, chunk_size=48000000):
    name_ = "{}".format(str(name_))
    data_val = (int(os.path.getsize(name_)))
    out_num = int(data_val // chunk_size)
    out_rem = int(data_val % chunk_size)
    if out_rem > 0:
        out_num += 1
    for i in range(0, out_num):
        data = file_.read(chunk_size)
        if not data:
            data = file_.read(out_rem)
        yield data

def hash_chunk(file_, size=48000000):
    data_val = (int(os.path.getsize(file_)))
    out_num = int(data_val // size)
    out_rem = int(data_val % size)
    if out_rem > 0:
        out_num += 1
    for i in range(0, out_num):
        data = open(file_, 'rb').read(size)
        if not data:
            data = open(file_, 'rb').read(out_rem)
        yield data

def shav(file_, input_):
    hasher = hashlib.sha256()
    for piece in hash_chunk(file_="{}{}".format(input_, file_)):
        hasher.update(piece)
    yield hasher.hexdigest()


def hashing(mode=None, list_=None, location_=None, total=None, run=None):
    print("DEBUG: Mode = " + str(mode))
    print("DEBUG: List_ = " + str(list_))
    print("DEBUG: Total = " + str(total))
    print("DEBUG: Run = " + str(run))
    current = 0
    event_ = True
    if mode is "make":
        if total is 0:
            total = 1
        if run == 0:
            read_data = json.load(open("Input_Data_Hash", 'r'))
            while event_:
                print("DEBUG: Current = " + str(current))
                if current is total:
                    event_ = False
                else:
                    event_ = sg.OneLineProgressMeter("Hash Core Files", current, total, "key")
                    file_ = list_[current]
                    sha = hashlib.sha256()
                    #hash_ = open("{}{}".format(location_, file_), 'r').read()
                    hash_ = open("{}{}".format(location_, file_), 'r').read()
                    read_data[file_] = shav(file_=file_, input_=location_)#hashlib.sha256(hash_).hexdigest()
                    print("DEBUG: Hash " + str(file_) + " = " + str(read_data[file_]))
                    current += 1
                    json.dump(read_data, open("Input_Data_Hash", 'w'), indent=3, sort_keys=True)
                    print("DEBUG: Hash Run 0 Written!")
        elif run == 1:
            current = 0
            event_ = True
            read_data = json.load(open("Output_Image_Hash", 'r'))
            for i in range(0, total):
                if current is total or not event_:
                    event_ = False
                else:
                    print("DEBUG: Current = " + str(current))
                    print("DEBUG: " + str(len(list_)))
                    event_ = sg.OneLineProgressMeter("Hash Core Files", current, total, "key")
                    file_ = list_[i]
                    #read_data[file_] = hashlib.sha256(file_).hexdigest()
                    read_data[file_] = shav(file_=file_, input_=location_)#hashlib.sha256(hash_).hexdigest()
                    print("DEBUG: Hash " + str(file_) + " = " + str(read_data[file_]))
                    json.dump(read_data, open("Output_Image_Hash", 'w'), indent=3, sort_keys=True)
                    print("DEBUG: Hash Run 0 Written!")
                    current += 1
        else:
            pass
    elif mode is "unpack":
        match = 0
        if total is 0:
            total = 1
        if run == 0:
            read_data = json.load(open("Output_Image_Hash", 'r'))
            while event_:
                print("DEBUG: Current = " + str(current))
                if current is total:
                    event_ = False
                else:
                    event_ = sg.OneLineProgressMeter("Hash Core Files", current, total, "key")
                    file_ = list_[current]
                    file_hash = shav(file_=file_, input_=location_)#hashlib.sha256(hash_).hexdigest()
                    print("DEBUG: Hash = " + str(file_hash))
                    print("DEBUG: Original_Hash = " + str(read_data[file_]))
                    if str(read_data[file_]) == str(file_hash):
                        print("DEBUG: File Hash Of " + str(file_) + " Matches!")
                        match += 1
                    else:
                        print("DEBUG: Hash Of File " + str(file_) + " Does Not Match!")
                    #print("DEBUG: Hash " + str(file_) + " = " + str(read_data[file_]))
                    current += 1
                    #json.dump(read_data, open("Input_Data_Hash", 'w'), indent=3, sort_keys=True)
                    #print("DEBUG: Hash Run 0 Written!")
            sg.Popup("Images Hashed", " Matches: {}/{}".format(match, total))
            if match != total:
                print("DEBUG: Process Halted!")
                value = sg.PopupYesNo("Hash Mismatch!", "The hashes of the images you were using do not match the originals!", "Action Taken: Halt Process", "Continue?")
                sys.exit()
            else:
                pass
            current = 0
            event_ = True
        elif run == 1:
            total_lim = total - 1
            read_data = json.load(open("Output_Image_Hash", 'r'))
            while event_:
                if current is total_lim:
                    event_ = False
                else:
                    print("DEBUG: Current = " + str(current))
                    file_ = list_[current]
                    event_ = sg.OneLineProgressMeter("Hash Core Files", current, total, "key")
                    file_ = list_[current]
                    read_data[file_] = hashlib.sha256(file_).hexdigest()
                    print("DEBUG: Hash " + str(file_) + " = " + str(read_data[file_]))
                    current += 1
                    json.dump(read_data, open("Output_Images_Hash", 'w'), indent=3, sort_keys=True)
                    print("DEBUG: Hash Run 0 Written!")
        else:
            pass
        pass
    else:
        pass

def test_hash(file_):
    m = hashlib.sha256()
    with open(file_, 'rb') as f:
        for piece in iter(f.read(1024)):
            m.update(piece)
    print(m.hexdigest())

def generic_upd3(files, input_, output_):
    print("DEBUG: Process Start!")
    lim = 48000000
    #base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    base = codecs.decode('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000', "hex")
    print("DEBUG: Base = " + str(base))
    buffer_ = ''
    name_dig = 0
    current = 0
    event = True
    file_lim = len(files) - 1
    #blob = str("00000000000000000000000000000000")
    blob = codecs.decode('3030303030303030303030303030303030303030303030303030303030303030', 'hex')
    keys = []
    name_ = "{}{}".format(input_, str(files[0]))
    open("test.txt", 'w').write(str(''.join(shav(files[0], input_))))
    time.sleep(10)
    data_val = (int(os.path.getsize(str(name_))))
    out_num = int(data_val // lim)
    print("DEBUG: Out_Num_Start = " + str(out_num))
    out_rem = int(data_val % lim)
    #hashing(mode="make", list_=files, location_=input_, total=file_lim, run=0)
    if out_rem > 0:
        out_num += 1
    print("DEBUG: Out_Rem = " + str(out_rem) + " Bytes")
    print("DEBUG: Out_Num_End = " + str(out_num))
    keys.append(out_num)
    num_total = sum(keys, 0)
    file_x = open(name_, 'rb')
    payload = chunk(file_x, name_=name_)
    for piece in payload: #chunk(file_):
        #print("DEBUG: Piece = " + str(piece.hex()))
        event = sg.OneLineProgressMeter('Build Progress', name_dig, out_num, 'key')
        print("DEBUG: Current = " + str(current))
        filename = files[current]
        print("DEBUG: Working With File | " + str(filename))
        print("DEBUG: Expected Output Files = " + str(num_total))
        print("DEBUG: Progress Bar Started!")
        if name_dig is num_total or not event:
            event = False
            print("DEBUG: Process Should Be Stopped!")
            break
        else:
            pass
        file_ = "{}{}-{}.bmp".format(str(output_), str(filename), str(name_dig))
        print("DEBUG: Name Dig = " + str(name_dig))
        print("DEBUG: Buffer Flushed to " + str(file_) + "!")
        print("DEBUG: Buffer Size = " + str(len(piece)))
        print("DEBUG: File Name = " + str(filename))
        name_dig += 1
        open(file_, 'ab').write(base)
        open(file_, 'ab').write(blob)
        open(file_, 'ab').write(piece)
    if name_dig is num_total:
        sg.Popup("Complete!", "Images Output: " + str(name_dig), "Output Location: " + str(output_))
        print("DEBUG: Process Should Halt!")
        #hashing(mode="make", list_=file_lib_, total=len(file_lib_), run=1)
    else:
        print("DEBUG: Deleting Files!")
        delete(str(output_))
        print("DEBUG: Files Deleted!")
        sg.Popup("Cancled!", "The process has been stopped, partially written data has automatically been deleted")


def rip_upd3(name, input_, output_):
    print("DEBUG: Initializing...")
    print("DEBUG: Stripping Non-BMP Files")
    for i in range(0, len(name)):
        if ".bmp" not in name[i]:
            print("DEBUG: File " + str(name[i]) + " Removed From List!")
            del name[i]
    sort_n(name)
    print("DEBUG: List Sorted")
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer_ = str('00000000000000000000000000000000')
    print("DEBUG: Base = " + str(base))
    dig = 0
    event = True
    file_lim = len(name) - 1
    file_len = len(name)
    print("DEBUG: Clearing Output Folder...")
    if len(output_) is not 0:
        delete(output_)
    else:
        pass
    print("DEBUG: Output Ready!")
    print("DEBUG: File_Lim = " + str(file_lim))
    print("DEBUG: File_Len = " + str(file_len))
    temp_name = ''
    for i in range(0, file_len):
        event = sg.OneLineProgressMeter('Build Progress', dig, len(name), 'key')
        if dig is file_len or not event:
            print("DEBUG: Process Should Stop")
            break
        content = open("{}{}".format(input_, str(name[dig])), 'rb').read()
        print("DEBUG: Reading File " + str(name[dig]))
        temp_name = str(name[dig]).strip("-{}.bmp".format(dig))
        print("DEBUG: SPlit Name | " + str(temp_name.split("-")))
        file_ = "{}{}".format(output_, str(temp_name))
        print("DEBUG: File " + str(temp_name) + " Processing")
        open(file_, 'ab').write(content[96:])
        print("DEBUG: Dig = " + str(dig))
        dig += 1
        print("DEBUG: Payload Dumped")
    check_value = dig / file_lim
    print("DEBUG: Check Value = " + str(check_value))
    if check_value >= 1:
        sg.Popup("Complete!", "Data Output: " + str(len(os.listdir(output_))), "Output Location: " + str(output_))
        print("DEBUG: Process Should Stop!")
        open("test2.txt", 'w').write(str(''.join(shav(temp_name, output_))))
    else:
        print("DEBUG: Deleting Output...")
        delete(str(output_))
        print("DEBUG: Output Deleted!")
        sg.Popup("Cancled!", "The process has been stopped partially written data has automatically been deleted")


def gen():
    for i in range(0, 10):
        sen = []
        for u in range(0, 10000000):
            sen.append("0")
        open("dummy", 'a').write(''.join(sen))

def initiate():
    output_images = 'Output_Images/'
    output_data = 'Output_Data/'
    input_images = 'Input_Images/'
    input_data = 'Input_Data/'
    if not os.path.exists(input_data):
        os.makedirs(input_data)
    if not os.path.exists(input_images):
        os.makedirs(input_images)
    if not os.path.exists(output_data):
        os.makedirs(output_data)
    if not os.path.exists(output_images):
        os.makedirs(output_images)
    if not os.path.exists("Input_Data_Hash"):
        open("Input_Data_Hash", 'w').write("{\n}")
    if not os.path.exists("Output_Image_Hash"):
        open("Output_Image_Hash", 'w').write("{\n}")
    if not os.path.exists("settings.txt"):
        open("settings.txt", 'w').write("{\n   \"Agree\": \"No\"\n}")


def agree():
    agreement = json.load(open("settings.txt", 'r'))
    if agreement["Agree"] == "No":
        try:
            license = open("LICENSE", 'r').read()
        except:
            license = "LICENSE NOT FOUND: User is using software in violation of license\n\nBy Clicking Accept You Still Agree To The LGPLv3\n\nBy Not Having The License File, Should You Click Accept, You Forfeit Your Rights To Complain About License Violations And Your Rights To The Source Code Of This Software.\n\nUser: DavidBerdik Has Complete Access To The Source, Regardless\n\nPermissions Given by: 78Alpha"

        layout = [[sg.Multiline(license, size=(60, 20))],
                  [sg.Button("Accept", button_color=('white', 'green')), sg.Button("Decline", button_color=('white', 'red'))]]

        window = sg.Window("GNU LESSER GENERAL PUBLIC LICENSE").Layout(layout)

        event = window.Read()

        if str(event[0]) != "Accept":
            print("DEBUG: License Rejected")
            sys.exit()
        else:
            agreement["Agree"] = "Yes"
            json.dump(agreement, open("settings.txt", 'w'), indent=3)
            window.Close()
    else:
        pass


def core():
    version = "1.4.6"

    out_images = 'Output_Images/'
    out_data = 'Output_Data/'
    in_images = 'Input_Images/'
    in_data = 'Input_Data/'

    layout = [[sg.Text('Input', justification='right'), sg.InputText('Use_Default'),
               sg.FolderBrowse()],
              [sg.Text('Output', justification='right'), sg.InputText('Use_Default'),
               sg.FolderBrowse()],
              [sg.Button('Make', button_color=('white', 'red')), sg.Button('Unpack', button_color=('white', 'green')),
               sg.Cancel()]]

    window = sg.Window('BMPMan V.{}'.format(version)).Layout(layout)

    event, values = window.Read()

    if str(event) == "Make":
        if str(values[0]) != "Use_Default" and str(values[1]) != "Use_Default":
            in_data = "{}/".format(str(values[0]).replace('\\', '/'))
            out_images = "{}/".format(str(values[1]).replace('\\', '/'))
            files = os.listdir(in_data)
            print("DEBUG: List = " + str(files))
            name_list = [str(name) for name in files]
            print("DEBUG: List = " + str(name_list))
            print("DEBUG: Length Of List = " + str(len(name_list)))
            time.sleep(3)
            window.Close()
            generic_upd3(name_list, input_=in_data, output_=out_images)
        elif str(values[0]) == "Use_Default" and str(values[1]) == "Use_Default":
            files = os.listdir(in_data)
            print("DEBUG: List = " + str(files))
            name_list = [str(name) for name in files]
            print("DEBUG: List = " + str(name_list))
            print("DEBUG: Length Of List = " + str(len(name_list)))
            time.sleep(3)
            window.Close()
            generic_upd3(name_list, input_=in_data, output_=out_images)
    elif str(event) == "Unpack":
        if str(values[0]) != "Use_Default" and str(values[1]) != "Use_Default":
            in_images = "{}/".format(str(values[0]).replace('\\', '/'))
            out_data = "{}/".format(str(values[1]).replace('\\', '/'))
            files = os.listdir(in_images)
            print("DEBUG: Files = " + str(files))
            name_list = [str(name) for name in files]
            print("DEBUG: List = " + str(name_list))
            print("DEBUG: Length Of List = " + str(len(name_list)))
            window.Close()
            rip_upd3(name_list, input_=in_images, output_=out_data)
        elif str(values[0]) == "Use_Default" and str(values[1]) == "Use_Default":
            files = os.listdir(in_images)
            print("DEBUG: Files = " + str(files))
            name_list = [str(name) for name in files]
            print("DEBUG: List = " + str(name_list))
            print("DEBUG: Length Of List = " + str(len(name_list)))
            window.Close()
            rip_upd3(name_list, input_=in_images, output_=out_data)
    else:
        sys.exit()

initiate()
agree()
core()
