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
import PySimpleGUI_Custom as sg
from PySimpleGUI_Custom import EasyPrint as Print
import time
import multiprocessing
import sys
import pathlib
import random
import io
from PIL import Image
import base64


def image_file_to_bytes(image64, size):
    image_file = io.BytesIO(base64.b64decode(image64))
    img = Image.open(image_file)
    img.thumbnail(size)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    imgbytes = bio.getvalue()
    return imgbytes


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
    if file_lim == 0:
        file_lim = 1
    else:
        pass
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

    version = "1.5.7"

    out_images = 'Output_Images/'
    out_data = 'Output_Data/'
    in_images = 'Input_Images/'
    in_data = 'Input_Data/'

    font = 'Arial'
    Print("DEBUG: Attempting To Load Custom Font...")
    try:
        font = "BMPMan"
    except:
        pass

    red_box = 'iVBORw0KGgoAAAANSUhEUgAAAXEAAABLCAYAAACGEbfbAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAWqSURBVHic7Z3Lj2VVGUfX7W4RQlBnaAI0A1vaCS04cOIENYbu5u0LHwiKCqKJb0hQtBEDiQo4FJ9DfEDQRBCB9MD/QSeiTFAHgFEE7G66+8fglohF33PP7rtr1z66VrIGVXVy987OV6tObp1UzZClBG4BvrLZ+xARWce+bZu9g94JfAP48mbvQ0RkHTfP5soiAl8HbtrsfYiIrOObM7gBYMtm76RXDLiIdMot/w44gHfixyBwM/DVzd6HiMg6vjWD61/6Ce/E1xHYhwEXkf54WcDBiP8XawH/2mbvQ0RkHbceK+Dg2ykvknm89y277hng7vn1IiLHxS7gLeMvv20GN27YZv4XCFwfyDKfhZw377eq6nH5ZsjfWN6bNb+NDBMDrqqNPBcDXpXAl8YcpgFX1VU9F/IUowN+OzJMCgL+tg4GQFWnqwGvTAy4qjbSgFcm8MUxh2nAVXVVz6Eo4Hcgw6Qg4G/vYABUdboa8MoEvjDmMJ/DgKvqahYG/E5kmBQE/B0dDICqTtc3QZ7EgFcj8Pkxh2nAVXVVDXhlMjLgByB7OxgAVZ2uhQH/TvyzJ8MEPjfmMA24qq5qYcC/GwM+TAy4qjZyF0UBvysGfJjAZ8cc5kHIBR0MgKpO112QJzDg1YgBV9VGFgb8ezHgw6Qg4Bd2MACqOl3PxoBXJfCZwNFlh2nAVXVVDXhlAtfEgKtqA98I+SujA/79+C8whwl8IiMDflEHA6Cq03UnBrwqMeCq2sjCgP8gBnyYwMdjwFW1gQa8MikI+MUdDICqTtedkL8wOuA/jAEfJgZcVRt5Fga8KoGPBY4sO8yDkEs6GABVna4GvDIZGfBDGHBVXc3CgP8oBnyYwNUx4KrawLMgf8aAVyMGXFUb+QaKAv7jGPBhUhDwSzsYAFWdrga8MoGPZkTAD0Mu72AAVHW6Fgb87sBWZDEx4KrayB0Y8KqkIODv72AAVHW67oA8jgGvRuAjMeCq2sDCgP8ksA1ZTAoC/oEOBkBVp6sBr0zgqhhwVW1gYcB/GgM+TAoC/sEOBkBVp+vrMeBVCVweOLzsMA24qq7qmZDHMODVSEHAP9TBAKjqdN1OUcB/FgM+TOB9geeXHaYBV9VV3Y4Br0oMuKo2cjtFAf95DPgwgfdmZMCv6GAAVHW6bof8CQNejRhwVW3kGRjwqqQg4B/uYABUdboWBvyewCuQxQTekxEBP4IBV9XVNOCVSUHAr+xgAFR1up4B+SOjA35vDPgwgXfHgKtqAw14ZTIy4Ech13QwAKo6XU/HgFclBlxVG3k65FFGB/xXgVciiwm8K3Bo2WEehVzbwQCo6nQtDPj9MeDDxICraiMNeGViwFW1kadRFPAHYsCHCVyWkQH/ZAcDoKrT9TTIHzDg1YgBV9VGGvDKpCDg13UwAKo6XV8L+T2jA/7rwInIYgJ7AweWHaYBV9VVNeCVCeyJAVfVBp6KAa9KCgL+qQ4GQFWn66mQ32HAqxHYHQOuqg0sDPiDMeDDpCDgn+5gAFR1uhrwcmZDXwxcANwLnLDshe4B7qq0KYAjwNMVX2+IfwBHG6zzHHCwwTrPA880WEekJq8D9gM7x13+IHDpDA5s4JYmwcKIB/YyD7jPW8pC/s78FmqjeRY41GCdQ2trbTRhfnYt+CdwuME6B5nfqBwv5wE7xl36G+ASAz7nmBE34CLSKQ8BFxvw//CyiAfOB+7D95pEpC8eZh7wf232Rnpiy0s/COwBfoEBF5G+MOALePFOPLCb+R24b6GISE88AlxkwI/NDCDwTuCXeAcuIn3xW2DPrM3vmyfJlrX3wA24iPTGfmC3AR9mFngrdQL+KmBrhddZxkm0+YGzDTilwToAr2HJM/uVOJkRz/xX4IS1tTaaGfOza8EpzGdiozmR+YxvNFuZf8+24NWs+/3bCPYDF85We2rx/4IXAICNKMDAcsK5AAAAAElFTkSuQmCC'
    orange_box = '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'
    yellow_box = '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'
    browse = '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'

    layout = [[sg.Text('BMPMAN DEBUG {}'.format(version), font=font, text_color='yellow', background_color='black', justification='center', size=(25, 2))],
              [sg.Text('INPUT', font=font, justification='right', background_color='black', text_color='yellow'), sg.InputText('USE_DEFAULT', font=font, text_color='#909090'),
               sg.FolderBrowse(image_data=image_file_to_bytes((browse), (200, 30)), button_text="", border_width=0, button_color=('yellow', 'black'), font=font)],
              [sg.Text('OUTPUT', font=font, justification='right', background_color='black', text_color='yellow'), sg.InputText('USE_DEFAULT', font=font,text_color='#909090'),
               sg.FolderBrowse(image_data=image_file_to_bytes((browse), (200, 30)), button_text="", border_width=0, button_color=('yellow', 'black'), font=font)],
              [sg.Button('make', font=font,border_width=0, image_data=image_file_to_bytes((red_box), (160,70)), button_color=('red', 'black')), sg.Button('unpack', font=font,border_width=0,  image_data=image_file_to_bytes((orange_box), (160,70)), button_color=('orange', 'black')),
               sg.Button('exit', font=font, border_width=0, image_data=image_file_to_bytes((yellow_box), (160,70)), button_color=('yellow', 'black'))]]

    window = sg.Window(title='BMPMan V.{}'.format(version), keep_on_top=False, no_titlebar=False, background_color='Black', grab_anywhere=True, alpha_channel=0.8).Layout(layout)  # Add this after | , alpha_channel=0.8

    event, values = window.Read()
    Print("DEBUG: Event | {}".format(event))
    Print("DEBUG: Values | {}".format(values))
    try:
        if str(event) == "make":
            if str(values[0]) != "USE_DEFAULT" and str(values[1]) != "USE_DEFAULT":
                in_data = "{}/".format(str(values[0]).replace('\\', '/'))
                out_images = "{}/".format(str(values[1]).replace('\\', '/'))
                files = os.listdir(in_data)
                Print("DEBUG: List | {} ".format(str(files)))
                name_list = [str(name) for name in files]
                Print("DEBUG: List | {}".format(str(name_list)))
                Print("DEBUG: Length Of List | {}".format(len(name_list)))
                window.Close()
                generic_upd3(name_list, input_=in_data, output_=out_images, home_=result)
            elif str(values[0]) == "USE_DEFAULT" and str(values[1]) == "USE_DEFAULT":
                files = os.listdir(in_data)
                Print("DEBUG: List | {}".format(str(files)))
                name_list = [str(name) for name in files]
                Print("DEBUG: List | {}".format(str(name_list)))
                Print("DEBUG: Length Of List | ".format(str(len(name_list))))
                window.Close()
                generic_upd3(name_list, input_=in_data, output_=out_images, home_=result)
        elif str(event) == "unpack":
            if str(values[0]) != "USE_DEFAULT" and str(values[1]) != "USE_DEFAULT":
                in_images = "{}/".format(str(values[0]).replace('\\', '/'))
                out_data = "{}/".format(str(values[1]).replace('\\', '/'))
                files = os.listdir(in_images)
                Print("DEBUG: Files | {}".format(str(files)))
                name_list = [str(name) for name in files]
                Print("DEBUG: List | {}".format(str(name_list)))
                Print("DEBUG: Length Of List | {}".format(str(len(name_list))))
                window.Close()
                rip_upd3(name_list, input_=in_images, output_=out_data, home_=result)
            elif str(values[0]) == "USE_DEFAULT" and str(values[1]) == "USE_DEFAULT":
                files = os.listdir(in_images)
                Print("DEBUG: Files | {}".format(str(files)))
                name_list = [str(name) for name in files]
                Print("DEBUG: List | {}".format(str(name_list)))
                Print("DEBUG: Length Of List | {}".format(str(len(name_list))))
                window.Close()
                rip_upd3(name_list, input_=in_images, output_=out_data, home_=result)
        else:
            sys.exit()
    except:
        pass

#
initiate()
core()
