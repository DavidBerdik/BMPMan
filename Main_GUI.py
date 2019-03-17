import binascii
import os
import re
import sys
import hashlib
import json
import codecs
import threading
import datetime
from multiprocessing.pool import ThreadPool
import PySimpleGUI as sg
from PySimpleGUI import EasyPrint as Print
import time
import multiprocessing
import sys
import pathlib
import random
import base64


def delete(directory):
    try:
        os.system("rm -r {}*".format(directory))
    except:
        os.system("del /S {}*".format(directory))


def tryint(s):
    Print("DEBUG: Splitting Over Integers...")
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort_n(l):
    Print("DEBUG: Sorting Called...")
    l.sort(key=alphanum_key)
    Print("DEBUG: Data Sorted!")


def chunk(file_, name_, chunk_size=48000000):
    Print("DEBUG: Chunk Called On File | {}".format(file_))
    name_ = "{}".format(str(name_))
    Print("DEBUG: Name Of Used File | {}".format(name_))
    data_val = (int(os.path.getsize(name_)))
    Print("DEBUG: Size Of File | {}".format(data_val))
    out_num = int(data_val // chunk_size)
    Print("DEBUG: Out Num | {}".format(out_num))
    out_rem = int(data_val % chunk_size)
    Print("DEBUG: Out Rem | {}".format(out_rem))
    if out_rem > 0:
        Print("DEBUG: Out Rem Greater Than Zero!")
        out_num += 1
        Print("DEBUG: Out Num Extended!")
    Print("DEBUG: Processing File By Chunks...")
    for i in range(0, out_num):
        data = file_.read(chunk_size)
        if not data:
            Print("DEBUG: Data Smaller Than Allowed | Reading Remaining Data...")
            data = file_.read(out_rem)
            Print("DEBUG: Read Successful!")
        Print("DEBUG: Data Yielded To Parent Function!")
        yield data


def hash_chunk(file_, multifile, size=48000000):
    Print("DEBUG: Chunk Function Called...")
    data_val = (int(os.path.getsize(file_)))
    Print("DEBUG: File Size | {}".format(data_val))
    out_num = int(data_val // size)
    Print("DEBUG: Out Num | {}".format(out_num))
    out_rem = int(data_val % size)
    Print("DEBUG: Out Rem | {}".format(out_rem))
    if out_rem > 0:
        Print("DEBUG: Remainder Greater Than Zero!")
        out_num += 1
        Print("DEBUG: Out Num Extended!")
    Print("DEBUG: Reading | {}".format(file_))
    event = True
    for i in range(0, out_num):
        if not multifile:
            event = sg.OneLineProgressMeter("Hashing File...", i, out_num, "stat")
        else:
            pass
        data = open(file_, 'rb').read(size)
        if not event:
            Print("DEBUG: Hashing Stopped!")
            sys.exit()
        else:
            if not data:
                Print("DEBUG: Remaining Data Smaller Than Chunk!")
                data = open(file_, 'rb').read(out_rem)
                Print("DEBUG: Processed Remaining Data!")
            Print("DEBUG: Data Yielded To Parent Function!")
        yield data


def shav(file_, input_, home_, out_file_, multifile=False):
    Print("DEBUG: Start Hash Function...")
    try:
        Print("DEBUG: Loading Hashes File...")
        hashes_ = json.load(open("{}{}".format(home_, out_file_), 'r'))
    except:
        Print("DEBUG: Failed To Load Hashes File!")
        pass
    Print("DEBUG: Hashing Choice Set...")
    hasher = hashlib.sha256()
    Print("DEBUG: Breaking File Into Chunks...")
    for piece in hash_chunk(multifile=multifile, file_="{}{}".format(input_, file_)):
        Print("DEBUG: Chunk Update...")
        hasher.update(piece)
    try:
        Print("DEBUG: Outputting Hash...")
        hashes_[file_] = hasher.hexdigest()
        json.dump(hashes_, open("{}{}".format(home_, out_file_), 'w'), indent=3, sort_keys=True)
        Print("DEBUG: Hash Data Dumped!")
    except:
        Print("DEBUG: Failed To Dump Hash Data!")
        pass
    Print("DEBUG: Data Yielded To Parent Function!")
    yield hasher.hexdigest()


def generic_upd3(files, input_, output_, home_):
    start = datetime.datetime.now()
    Print("DEBUG: Current Time | {}".format(str(start)))
    cpu_ = multiprocessing.cpu_count()
    Print("DEBUG: Thread Count Set | {}".format(cpu_))
    pool = ThreadPool(processes=int(cpu_))
    Print("DEBUG: Process Start!")
    lim = 48000000
    base = codecs.decode(
        '424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000',
        "hex")
    Print("DEBUG: Base = {}".format(str(base)))
    name_dig = 0
    current = 0
    blob = codecs.decode('3030303030303030303030303030303030303030303030303030303030303030', 'hex')
    keys = []
    Print("DEBUG: Keys | {}".format(keys))
    name_ = "{}{}".format(input_, str(files[0]))
    Print("DEBUG: Hashing Start...")
    open("test.txt", 'w').write(
        str(''.join(shav(files[0], input_, multifile=False, home_=home_, out_file_="Input_Data_Hash.txt"))))
    Print("DEBUG: Hashing End!")
    data_val = (int(os.path.getsize(str(name_))))
    Print("DEBUG: File Size | {}".format(data_val))
    out_num = int(data_val // lim)
    Print("DEBUG: Out_Num_Start = {}".format(str(out_num)))
    out_rem = int(data_val % lim)
    Print("DEBUG: Out Remainder | {}".format(out_rem))
    if out_rem > 0:
        out_num += 1
    Print("DEBUG: Out_Rem | {}" + str(out_rem) + " Bytes")
    Print("DEBUG: Out_Num_End | {}".format(str(out_num)))
    keys.append(out_num)
    num_total = sum(keys, 0)
    Print("DEBUG: Out Number | {}".format(num_total))
    file_x = open(name_, 'rb')
    Print("DEBUG: File In Use | {}".format(file_x))
    async_result = pool.apply_async(chunk, (file_x, name_))
    payload = async_result.get()
    # payload = chunk(file_=file_x, name_=name_)
    for piece in payload:  # chunk(file_):
        event = sg.OneLineProgressMeter('Build Progress', name_dig, out_num, 'key')
        Print("DEBUG: Current | {}".format(str(current)))
        filename = files[current]
        Print("DEBUG: Working With File | {}".format(str(filename)))
        Print("DEBUG: Expected Output Files | {}".format(str(num_total)))
        Print("DEBUG: Progress Bar Started!")
        if name_dig is num_total or not event:
            Print("DEBUG: Process Should Be Stopped!")
            break
        else:
            Print("DEBUG: Name Dig Not At Limit | No User Cancellation")
            pass
        file_ = "{}{}-{}.bmp".format(str(output_), str(filename), str(name_dig))
        Print("DEBUG: Name Dig | {}".format(str(name_dig)))
        Print("DEBUG: Buffer Flushed to {}!".format(str(file_)))
        Print("DEBUG: Buffer Size | {}".format(str(len(piece))))
        Print("DEBUG: File Name | {}".format(str(filename)))
        name_dig += 1
        open(file_, 'ab').write(base)
        Print("DEBUG: Header Bytes Written!")
        open(file_, 'ab').write(blob)
        Print("DEBUG: Buffer Bytes Written!")
        open(file_, 'ab').write(piece)
        Print("DEBUG: File Data Written!")
    Print("DEBUG: Name Dig | {}".format(str(name_dig)))
    if name_dig >= num_total:
        Print("DEBUG: Loading Completion Popup...")
        Print("DEBUG: End Time | {}".format(str(datetime.datetime.now() - start)))
        Print("DEBUG: Process Should Halt!")
        out_len_ = os.listdir(output_)
        Print("DEBUG: Files In Out Len | {}".format(str(out_len_)))
        Print("DEBUG: Hashing Images...")
        name_in_use = 0
        for name in out_len_:
            try:
                sg.OneLineProgressMeter("Hashing Images...", int(name_in_use), int(len(out_len_)), "key")
                name_in_use += 1
                Print("DEBUG: Name | {}".format(str(name)))
                open("Output_Image_Hash.txt", 'w').write(
                    str(''.join(shav(name, output_, multifile=True, home_=home_, out_file_="Output_Image_Hash.txt"))))
            except:
                sg.PopupError("An Unexpected Error Has Occurred!", "Failed to Hash Images")
                sys.exit()
        Print("DEBUG: Hash Complete!")
        sg.Popup("Complete!", "Images Output: " + str(name_dig), "Output Location: " + str(output_))
    else:
        Print("DEBUG: Deleting Files!")
        delete(output_)
        Print("DEBUG: Files Deleted!")
        Print("DEBUG: Loading Cancelation Popup...")
        sg.Popup("Cancled!", "The process has been stopped, partially written data has automatically been deleted")


def rip_upd3(name, input_, output_, home_):
    pool = ThreadPool(processes=int(multiprocessing.cpu_count()))
    Print("DEBUG: Thread Count Set | {}".format(pool))
    Print("DEBUG: Initializing...")
    Print("DEBUG: Stripping Non-BMP Files")
    for i in range(0, len(name)):
        if ".bmp" not in name[i]:
            del name[i]
            Print("DEBUG: File {} Removed From List!".format(str(name[i])))
        else:
            pass
    sort_n(name)
    Print("DEBUG: Name List Sorted")
    dig = 0
    file_lim = len(name) - 1
    file_len = len(name)
    Print("DEBUG: Clearing Output Folder...")
    Print("DEBUG: Output Ready!")
    Print("DEBUG: File Limit | {}".format(str(file_lim)))
    Print("DEBUG: File Length | {}".format(str(file_len)))
    files_ = os.listdir(input_)
    Print("DEBUG: Files In Input | {}".format(files_))
    check = 0
    if len(output_) > 0:
        delete(output_)
    else:
        pass
    for i in range(0, len(files_)):
        Print("DEBUG: Hashing Start!")
        event = sg.OneLineProgressMeter("Hashing Images", i, len(files_), 'key')
        if not event:
            Print("DEBUG: Hashing Should Stop...")
            break
        temp_name__ = files_[i]
        Print("DEBUG: Temp Name | {}".format(temp_name__))
        comp_hash_ = ''.join(shav(temp_name__, input_, multifile=True, home_=home_, out_file_=''))
        comp_hash_other_ = json.load(open('{}{}'.format(home_, "Output_Image_Hash.txt"), 'r'))
        Print("DEBUG: Hashes | {}".format(comp_hash_other_))
        try:
            if comp_hash_ == comp_hash_other_[temp_name__]:
                check += 1
                Print("DEBUG: Hash Match!")
                Print("DEBUG: Hashes | OG = {} | Current = {}".format(str(comp_hash_other_[temp_name__]),
                                                                      str(comp_hash_)))
            else:
                Print("DEBUG: Hash Mismatch!")
                Print("DEBUG: Hashes | OG = {} | Current = {}".format(str(comp_hash_other_[temp_name__]),
                                                                      str(comp_hash_)))
                pass
        except:
            pass
    if check == len(files_):
        Print("DEBUG: All Hashes Matched")
        pass
    else:
        sg.PopupError("Hashes Do Not Match! | Process Halted!")
        sys.exit()
    for i in range(0, file_len):
        Print("DEBUG: Progress Bar Start...")
        event = sg.OneLineProgressMeter('Build Progress', dig, len(name), 'key_b')
        if dig is file_len or not event:
            Print("DEBUG: Process Should Stop")
            break
        content = open("{}{}".format(input_, str(name[dig])), 'rb').read()
        Print("DEBUG: Reading File | {}".format(str(name[dig])))
        temp_name = str(name[dig]).strip("-{}.bmp".format(dig))
        Print("DEBUG: Split Name | {}".format(str(temp_name.split("-"))))
        file_ = "{}{}".format(output_, str(temp_name))
        Print("DEBUG: File {} Processing".format(str(temp_name)))
        open(file_, 'ab').write(content[96:])
        Print("DEBUG: Header Stripped!")
        Print("DEBUG: Dig | {}".format(str(dig)))
        dig += 1
        Print("DEBUG: Payload Dumped")
    check = 0
    check_value = dig / file_lim
    Print("DEBUG: Checking That All Files Have Been Processed...")
    Print("DEBUG: Check Value |  {}".format(str(check_value)))
    if check_value >= 1:
        Print("DEBUG: Opening Complete Popup Window...")
        sg.Popup("Complete!", "Data Output: {}".format(str(len(os.listdir(output_)))),
                 "Output Location: {}".format(str(output_)))
        Print("DEBUG: Hashing Output File!")
        files_ = os.listdir(output_)
        Print("DEBUG: Files In Output | {}".format(files_))
        for i in range(0, len(files_)):
            Print("DEBUG: Progress Bar Start...")
            sg.OneLineProgressMeter("Hashing Output", i, len(files_), "key")
            nn_ = files_[i]
            Print("DEBUG: Current Name | {}".format(nn_))
            comp_hash_ = ''.join(shav(nn_, output_, home_=home_, out_file_=''))
            comp_hash_other_ = json.load(open('{}{}'.format(home_, "Input_Data_Hash.txt"), 'r'))
            if comp_hash_ == comp_hash_other_[nn_]:
                check += 1
                Print("DEBUG: Hash Match!")
                Print("DEBUG: Hashes | OG = {} Current = {}".format(str(comp_hash_other_[nn_]), str(comp_hash_)))
            else:
                Print("DEBUG: Hash Mismatch!")
                Print("DEBUG: Hashes | OG = {} Current = {}".format(str(comp_hash_other_[nn_]), str(comp_hash_)))
                pass
        sg.PopupOK("Process Finished! | Clicking 'OK' Will close the debug Window!")
    else:
        Print("DEBUG: Output Deleted!")
        delete(output_)
        Print("DEBUG: Loading Cancel Popup")
        sg.Popup("Canceled!", "The process has been stopped partially written data has automatically been deleted")


def gen():
    Print("DEBUG: Generating Test File...")
    values = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12345667890!@#$%^&*()_+-="
    for i in range(0, 1000):
        sen = [random.choice(values) for i in range(1000000)]
        open("dummy", 'a').write(''.join(sen))
    Print("DEBUG: Test File Generated | dummy")


def initiate():
    Print("DEBUG: Creating Working Directories...")
    output_images = 'Output_Images/'
    output_data = 'Output_Data/'
    input_images = 'Input_Images/'
    input_data = 'Input_Data/'
    home = str(pathlib.Path.home())
    if not os.path.exists(input_data):
        os.makedirs(input_data)
    if not os.path.exists(input_images):
        os.makedirs(input_images)
    if not os.path.exists(output_data):
        os.makedirs(output_data)
    if not os.path.exists(output_images):
        os.makedirs(output_images)
    if not os.path.exists("{}/BMPMan/".format(home)):
        try:
            Print("DEBUG: Files Allowed Global User Access | BMPMan3 Can Now Be Added To PATH")
            os.makedirs("{}/BMPMan/".format(home))
            home_ = "{}/BMPMan/".format(home)
            Print("DEBUG: Data Directory | {}".format(str(home_)))
            open("{}/BMPMan/settings.txt".format(str(home)), 'w').write("{\n   \"Agree\": \"No\"\n}")
            if not os.path.exists("{}/BMPMan/Output_Image_Hash.txt"):
                open("{}/BMPMan/Output_Image_Hash.txt".format(home), 'w').write("{\n}")
            if not os.path.exists("{}/BMPMan/Input_Data_Hash.txt"):
                open("{}/BMPMan/Input_Data_Hash.txt".format(home), 'w').write("{\n}")
        except:
            Print("DEBUG: Files Not Allowed Global User Access | Permission Denied")
            if not os.path.exists("Output_Image_Hash"):
                open("Output_Image_Hash", 'w').write("{\n}")
            if not os.path.exists("Input_Data_Hash"):
                open("Input_Data_Hash", 'w').write("{\n}")
            open("settings.txt", 'w').write("{\n   \"Agree\": \"No\"\n}")


def agree():
    Print("DEBUG: Running Agree Function")
    home_true = str("{}/BMPMan/".format(pathlib.Path.home()))
    Print("DEBUG: Data Directory Agree | {}".format(str(home_true)))
    Print("DEBUG: Loading Agreement Form...")
    if home_true is not None:
        Print("DEBUG: Global Settings Loading...")
        agreement = json.load(open("{}settings.txt".format(home_true), 'r'))
        Print("DEBUG: Global Settings Loaded!")
    else:
        Print("DEBUG: Local Settings Loading...")
        agreement = json.load(open("settings.txt", 'r'))
        Print("DEBUG: Local Settings Loaded")
    if agreement["Agree"] == "No":
        Print("DEBUG: Agreement Not Yet Accepted!")
        try:
            Print("DEBUG: Reading License...")
            license = open("LICENSE", 'r').read()
        except:
            Print("DEBUG: License File Not Found In Current Directory")
            license = ("LICENSE NOT FOUND: User is using software in violation of license\n\n"
                       "By Clicking Accept You Still Agree To The LGPLv3\n\n"
                       "By Not Having The License File, Should You Click Accept, You Forfeit Your Rights To Complain "
                       "About License Violations And Your Rights To The Source Code Of This Software.\n\n"
                       "User: DavidBerdik Has Complete Access To The Source, Regardless\n\n"
                       "Permissions Given by: 78Alpha")

        layout = [[sg.Multiline(license, size=(60, 20))],
                  [sg.Button("Accept", button_color=('white', 'green')),
                   sg.Button("Decline", button_color=('white', 'red'))]]

        window = sg.Window("GNU LESSER GENERAL PUBLIC LICENSE").Layout(layout)

        Print("DEBUG: Opening Window...")

        event = window.Read()

        if str(event[0]) != "Accept":
            Print("DEBUG: License Rejected")
            sys.exit()
        else:
            agreement["Agree"] = "Yes"
            Print("DEBUG: License Accepted")
            if home_true is not None:
                json.dump(agreement, open("{}settings.txt".format(home_true), 'w'), indent=3)
                yield str(home_true)
            else:
                json.dump(agreement, open("settings.txt", 'w'), indent=3)
                home_true = './'
                yield home_true

            window.Close()
    else:
        yield home_true


def core():
    result = str(''.join(agree()))

    if result is not None:
        Print("DEBUG: Data Directory Core | {}".format(result))
    else:
        Print("DEBUG: Data Directory Core | NoneType")

    version = "1.5.6"

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
            Print("DEBUG: List | {} ".format(str(files)))
            name_list = [str(name) for name in files]
            Print("DEBUG: List | {}".format(str(name_list)))
            Print("DEBUG: Length Of List | {}".format(len(name_list)))
            window.Close()
            generic_upd3(name_list, input_=in_data, output_=out_images, home_=result)
        elif str(values[0]) == "Use_Default" and str(values[1]) == "Use_Default":
            files = os.listdir(in_data)
            Print("DEBUG: List | {}".format(str(files)))
            name_list = [str(name) for name in files]
            Print("DEBUG: List | {}".format(str(name_list)))
            Print("DEBUG: Length Of List | ".format(str(len(name_list))))
            window.Close()
            generic_upd3(name_list, input_=in_data, output_=out_images, home_=result)
    elif str(event) == "Unpack":
        if str(values[0]) != "Use_Default" and str(values[1]) != "Use_Default":
            in_images = "{}/".format(str(values[0]).replace('\\', '/'))
            out_data = "{}/".format(str(values[1]).replace('\\', '/'))
            files = os.listdir(in_images)
            Print("DEBUG: Files | {}".format(str(files)))
            name_list = [str(name) for name in files]
            Print("DEBUG: List | {}".format(str(name_list)))
            Print("DEBUG: Length Of List | {}".format(str(len(name_list))))
            window.Close()
            rip_upd3(name_list, input_=in_images, output_=out_data, home_=result)
        elif str(values[0]) == "Use_Default" and str(values[1]) == "Use_Default":
            files = os.listdir(in_images)
            Print("DEBUG: Files | {}".format(str(files)))
            name_list = [str(name) for name in files]
            Print("DEBUG: List | {}".format(str(name_list)))
            Print("DEBUG: Length Of List | {}".format(str(len(name_list))))
            window.Close()
            rip_upd3(name_list, input_=in_images, output_=out_data, home_=result)
    else:
        sys.exit()


#
initiate()
core()
