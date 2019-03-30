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

try:
    import PySimpleGUI_Custom as sg
except:
    import PySimpleGUI as sg
import time
import multiprocessing
import sys
import pathlib
import random
import io
from PIL import Image
import base64
import multiprocessing


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


def hash_chunk(file_, multifile, out_num, out_rem, size=48000000):
    event = True
    for i in range(0, out_num):
        data = open(file_, 'rb').read(size)
        if not event:
            sys.exit()
        else:
            if not data:
                data = open(file_, 'rb').read(out_rem)
        yield data


def shav(file_, input_, home_, out_file_, out_num, out_rem, mode, buffer=48000000, multifile=False):
    hasher = hashlib.sha256()
    current = 0
    if multifile:
        data = open(f"{input_}{file_}", 'rb').read(buffer)
        hasher.update(data)
        yield hasher.hexdigest()
    else:
        hashes_ = json.load(open("{}{}".format(home_, out_file_), 'r'))
        if out_rem > 0:
            out_num += 1
        for piece in hash_chunk(multifile=multifile, size=buffer, out_num=out_num, out_rem=out_rem, file_=f"{input_}{file_}"):
            hasher.update(piece)
            yield current, hasher.hexdigest()
            current += 1
        if mode == "verify":
            pass
        elif mode == "generate":
            hashes_[file_] = hasher.hexdigest()
            json.dump(hashes_, open("{}{}".format(home_, out_file_), 'w'), indent=3, sort_keys=True)
        else:
            pass


def generic_upd3(files, input_, output_, home_, font_, data, icon):
    t1 = time.time()
    settings = json.load(open("{}settings.txt".format(home_), 'r'))
    security = True if settings["SECURITY"] == "True" else False
    cpu_ = settings["THREADS"]
    pool = ThreadPool(processes=int(cpu_))
    lim = 48000000
    base = codecs.decode(
        '424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000',
        "hex")
    name_dig = 0
    current = 0
    blob = codecs.decode('3030303030303030303030303030303030303030303030303030303030303030', 'hex')
    keys = []
    name_ = "{}{}".format(input_, str(files[0]))
    data_val = (int(os.path.getsize(str(name_))))
    out_num = int(data_val // lim)
    out_rem = int(data_val % lim)
    if out_rem > 0:
        out_num += 1
    keys.append(out_num)
    num_total = sum(keys, 0)
    file_x = open(name_, 'rb')
    async_result = pool.apply_async(chunk, (file_x, name_))
    payload = async_result.get()
    holder = 0
    b1 = 0
    b2 = 0
    b3 = 0
    main_data = [[sg.Text("HASHING INPUT...",
                          font=font_,
                          text_color='red',
                          background_color='black',
                          justification='center',
                          key="H",
                          size=(30, 2))],
                 [sg.Text("HASH IN",
                          font=font_,
                          text_color='red',
                          background_color='black',
                          justification='left',
                          size=(14, 1),
                          key="In"),
                  sg.ProgressBar(max_value=out_num,
                                 orientation='h',
                                 bar_color=("red", "black"),
                                 size=(30, 10),
                                 border_width=0,
                                 relief="flat",
                                 key="DataHI"),
                  sg.Text("0%",
                          font=font_,
                          text_color='red',
                          background_color='black',
                          justification='center',
                          key="PercentHI")],
                 [sg.Text("IMAGES",
                          font=font_,
                          text_color='orange',
                          background_color='black',
                          justification='left',
                          size=(14, 1),
                          key="Mod"),
                  sg.ProgressBar(max_value=out_num,
                                 orientation='h',
                                 bar_color=("orange", "black"),
                                 size=(30, 10),
                                 border_width=0,
                                 relief="flat",
                                 key="Data"),
                  sg.Text("0%",
                          font=font_,
                          text_color='orange',
                          background_color='black',
                          justification='center',
                          key="Percent")],
                 [sg.Text("HASH OUT",
                          font=font_,
                          text_color='yellow',
                          background_color='black',
                          justification='left',
                          size=(14, 1),
                          key="Out"),
                  sg.ProgressBar(max_value=out_num,
                                 orientation='h',
                                 bar_color=("yellow", "black"),
                                 size=(30, 10),
                                 border_width=0,
                                 relief="flat",
                                 key="DataHO"),
                  sg.Text("0%",
                          font=font_,
                          text_color='yellow',
                          background_color='black',
                          justification='center',
                          key="PercentHO")],
                 [sg.Button(button_text="cancel",
                            font=font_,
                            border_width=0,
                            button_color=('red', 'black'),
                            image_data=image_file_to_bytes(data[0], (160, 70)),
                            key='Button'),
                  sg.Text("TOTAL TIME: ",
                          font=font_,
                          background_color='black',
                          text_color='yellow',
                          justification='right',
                          key="Total"),
                  sg.Text(f"{holder} SECONDS",
                          font=font_,
                          background_color='black',
                          text_color='yellow',
                          key='Timed',
                          justification='right')]
                 ]
    main_window = sg.Window('BMPMAN PROCESS',
                            background_color='black',
                            grab_anywhere=True,
                            alpha_channel=0.8,
                            icon=icon).Layout(main_data)
    timer = main_window.FindElement("Timed")
    progress_bar = main_window.FindElement('Data')
    progress_percent = main_window.FindElement('Percent')
    hash_bar = main_window.FindElement('DataHI')
    hash_percent = main_window.FindElement('PercentHI')
    hash_bar_2 = main_window.FindElement('DataHO')
    hash_percent_2 = main_window.FindElement('PercentHO')
    button_change = main_window.FindElement('Button')
    header_change = main_window.FindElement('H')
    in_text = main_window.FindElement('In')
    mid_text = main_window.FindElement('Mod')
    out_text = main_window.FindElement('Out')
    total = main_window.FindElement("Total")
    if security:
        async_hash = pool.apply_async(shav,
                                      (str(files[0]),
                                       input_,
                                       home_,
                                       'Input_Data_Hash.txt',
                                       out_num,
                                       out_rem,
                                       "generate",
                                       lim,
                                       False
                                       ))
        hash_count = async_hash.get()
        for i, hash_ in hash_count:
            event, values = main_window.Read(timeout=0)
            hash_bar.UpdateBar(i)
            hash_percent.Update(f"{(int(i) * 100 // out_num)}%")
            if event == "Button":
                header_change.Update("CANCELED",
                                     text_color='white')
                button_change.Update("close",
                                     button_color=('white', 'black'),
                                     image_data=image_file_to_bytes(data[4], (160, 70)))
                hash_bar.UpdateBar(current_count=0)
                hash_bar_2.UpdateBar(current_count=0)
                progress_bar.UpdateBar(current_count=0)
                in_text.Update(text_color='white')
                mid_text.Update(text_color='white')
                out_text.Update(text_color='white')
                hash_percent.Update(text_color="white")
                hash_percent_2.Update(text_color="white")
                progress_percent.Update(text_color="white")
                total.Update(text_color="white")
                timer.Update(text_color="white")
                event, values = main_window.Read()
                if event == "Button":
                    sys.exit()
                else:
                    sys.exit()
            else:
                pass
        header_change.Update("PROCESSING DATA...",
                             text_color='orange')
        button_change.Update(button_color=('orange', 'black'),
                             image_data=image_file_to_bytes(data[1], (160, 70)))
    else:
        event, values = main_window.Read(timeout=0)
        header_change.Update("PROCESSING DATA...",
                             text_color='orange')
        in_text.Update("DISABLED", text_color='white')
        hash_percent.Update(text_color='white')
        out_text.Update("DISABLED", text_color='white')
        hash_percent_2.Update(text_color='white')
        button_change.Update(button_color=('orange', 'black'),
                             image_data=image_file_to_bytes(data[1], (160, 70)))
        pass
    for piece in payload:
        event, values = main_window.Read(timeout=0)
        filename = files[current]
        if name_dig is num_total or event == "Button":
            header_change.Update("CANCELED",
                                 text_color='white')
            button_change.Update("close",
                                 button_color=('white', 'black'),
                                 image_data=image_file_to_bytes(data[4], (160, 70)))
            hash_bar.UpdateBar(current_count=0)
            hash_bar_2.UpdateBar(current_count=0)
            progress_bar.UpdateBar(current_count=0)
            in_text.Update(text_color='white')
            mid_text.Update(text_color='white')
            out_text.Update(text_color='white')
            hash_percent.Update(text_color="white")
            hash_percent_2.Update(text_color="white")
            progress_percent.Update(text_color="white")
            total.Update(text_color="white")
            timer.Update(text_color="white")
            break
        else:
            pass
        file_ = "{}{}-{}.bmp".format(str(output_), str(filename), str(name_dig))
        name_dig += 1
        open(file_, 'ab').write(base)
        open(file_, 'ab').write(blob)
        open(file_, 'ab').write(piece)
        progress_bar.UpdateBar(name_dig)
        progress_percent.Update(f"{(name_dig * 100 // out_num)}%")
    progress_percent.Update("100%")
    if name_dig >= num_total:
        if security:
            header_change.Update("HASHING OUTPUT...",
                                 text_color='yellow')
            button_change.Update(button_color=('yellow', 'black'),
                                 image_data=image_file_to_bytes(data[2], (160, 70)))
            out_len_ = os.listdir(output_)
            hashes_ = json.load(open("{}{}".format(home_, "Output_Image_Hash.txt"), 'r'))
            for i in range(len(out_len_)):
                event, values = main_window.Read(timeout=0)
                if event == "Button":
                    header_change.Update("CANCELED",
                                         text_color='white')
                    button_change.Update("close",
                                         button_color=('white', 'black'),
                                         image_data=image_file_to_bytes(data[4], (160, 70)))
                    hash_bar.UpdateBar(current_count=0)
                    hash_bar_2.UpdateBar(current_count=0)
                    progress_bar.UpdateBar(current_count=0)
                    in_text.Update(text_color='white')
                    mid_text.Update(text_color='white')
                    out_text.Update(text_color='white')
                    hash_percent.Update(text_color="white")
                    hash_percent_2.Update(text_color="white")
                    progress_percent.Update(text_color="white")
                    total.Update(text_color="white")
                    timer.Update(text_color="white")
                    event, values = main_window.Read()
                    if event == "Button":
                        sys.exit()
                    else:
                        pass
                im_async_hash = pool.apply_async(shav,
                                                 (out_len_[i],
                                                  output_,
                                                  home_,
                                                  "Output_Image_Hash.txt",
                                                  len(out_len_),
                                                  0,
                                                  "generate",
                                                  48000096,
                                                  True))
                hashes_[out_len_[i]] = ''.join(im_async_hash.get())
                hash_bar_2.UpdateBar(i)
                hash_percent_2.Update(f"{(i * 100 // len(out_len_))}%")
            json.dump(hashes_, open("{}{}".format(home_, "Output_Image_Hash.txt"), 'w'), indent=3)
            hash_bar_2.Update(len(out_len_))
            hash_percent_2.Update("100%")
            button_change.Update("close",
                                 image_data=image_file_to_bytes(data[4], (160, 70)),
                                 button_color=('white', 'black'))
            end_time = int(time.time() - t1)
            timer.Update(f"{end_time} SECONDS",
                         text_color='white')
            total.Update(text_color='white')
            header_change.Update("PROCESS COMPLETE",
                                 text_color='white')
            event, values = main_window.Read()
            if event == "Button":
                sys.exit()
            else:
                pass
        else:
            header_change.Update("COMPLETE",
                                 text_color='white')
            button_change.Update("close",
                                 button_color=('white', 'black'),
                                 image_data=image_file_to_bytes(data[4], (160, 70)))
            end_time = int(time.time() - t1)
            total.Update(text_color='white')
            timer.Update(f"{end_time} SECONDS",
                         text_color='white')
            event, values = main_window.Read()
            if event == "Button":
                sys.exit()
            else:
                sys.exit()
    else:
        header_change.Update("CANCELED",
                             text_color='white')
        button_change.Update("close",
                             button_color=('white', 'black'),
                             image_data=image_file_to_bytes(data[4], (160, 70)))
        progress_bar.UpdateBar(current_count=0)
        mid_text.Update(text_color='white')
        total.Update(text_color="white")
        timer.Update(text_color="white")
        delete(output_)
        event, values = main_window.Read()
        if event == "Button":
            sys.exit()
        else:
            sys.exit()


def rip_upd3(name, input_, output_, home_, font_, data, icon):
    t1 = time.time()
    settings = json.load(open("{}settings.txt".format(home_), 'r'))
    security = True if settings["SECURITY"] == "True" else False
    cpu_ = int(settings["THREADS"])
    pool = ThreadPool(processes=int(cpu_))
    comp_hash_other_2 = json.load(open('{}{}'.format(home_, "Input_Data_Hash.txt"), 'r'))
    comp_hash_other_ = json.load(open('{}{}'.format(home_, "Output_Image_Hash.txt"), 'r'))
    sort_n(name)
    dig = 0
    file_lim = len(name) - 1
    file_len = len(name)
    check = 0
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    main_data = [[sg.Text("PURGING...",
                          font=font_,
                          text_color='red',
                          background_color='black',
                          justification='center',
                          key="H",
                          size=(30, 2))],
                 [sg.Text("PURGE",
                          font=font_,
                          text_color='red',
                          background_color='black',
                          justification='left',
                          size=(14, 1),
                          key="Purge"),
                  sg.ProgressBar(max_value=file_len,
                                 orientation='h',
                                 bar_color=("red", "black"),
                                 size=(30, 10),
                                 border_width=0,
                                 relief='flat',
                                 key="PurgeB"),
                  sg.Text("0%",
                          font=font_,
                          text_color='red',
                          background_color='black',
                          justification='center',
                          key="PurgeP")],
                 [sg.Text("HASH IN",
                          font=font_,
                          text_color='orange',
                          background_color='black',
                          justification='left',
                          size=(14, 1),
                          key="In"),
                  sg.ProgressBar(max_value=file_len,
                                 orientation='h',
                                 bar_color=("orange", "black"),
                                 size=(30, 10),
                                 border_width=0,
                                 relief="flat",
                                 key="DataHI"),
                  sg.Text("0%",
                          font=font_,
                          text_color='orange',
                          background_color='black',
                          justification='center',
                          key="PercentHI")],
                 [sg.Text("DATA",
                          font=font_,
                          text_color='yellow',
                          background_color='black',
                          justification='left',
                          size=(14, 1),
                          key="Mod"),
                  sg.ProgressBar(max_value=file_len,
                                 orientation='h',
                                 bar_color=("yellow", "black"),
                                 size=(30, 10),
                                 border_width=0,
                                 relief="flat",
                                 key="Data"),
                  sg.Text("0%",
                          font=font_,
                          text_color='yellow',
                          background_color='black',
                          justification='center',
                          key="Percent")],
                 [sg.Text("HASH OUT",
                          font=font_,
                          text_color='white',
                          background_color='black',
                          justification='left',
                          size=(14, 1),
                          key="Out"),
                  sg.ProgressBar(max_value=file_len,
                                 orientation='h',
                                 bar_color=("white", "black"),
                                 size=(30, 10),
                                 border_width=0,
                                 relief="flat",
                                 key="DataHO"),
                  sg.Text("0%",
                          font=font_,
                          text_color='white',
                          background_color='black',
                          justification='center',
                          key="PercentHO")],
                 [sg.Button(button_text="cancel",
                            font=font_,
                            border_width=0,
                            button_color=('red', 'black'),
                            image_data=image_file_to_bytes(data[0], (160, 70)),
                            key='Button'),
                  sg.Button(button_text="proceed",
                            font=font_,
                            border_width=0,
                            button_color=('red', 'black'),
                            image_data=image_file_to_bytes(data[5], (160, 70)),
                            key='Danger',
                            visible=False),
                  sg.Text("TOTAL TIME: ",
                          font=font_,
                          background_color='black',
                          text_color='yellow',
                          justification='right',
                          key="Total"),
                  sg.Text(f"{check} SECONDS",
                          font=font_,
                          background_color='black',
                          text_color='yellow',
                          key='Timed',
                          justification='right')]
                 ]
    main_window = sg.Window('BMPMAN PROCESS',
                            background_color='black',
                            grab_anywhere=True,
                            alpha_channel=0.8,
                            icon=icon).Layout(main_data)
    timer = main_window.FindElement("Timed")
    text_purge = main_window.FindElement("Purge")
    purge_bar = main_window.FindElement("PurgeB")
    purge_percent = main_window.FindElement("PurgeP")
    progress_bar = main_window.FindElement('Data')
    progress_percent = main_window.FindElement('Percent')
    hash_bar = main_window.FindElement('DataHI')
    hash_percent = main_window.FindElement('PercentHI')
    hash_bar_2 = main_window.FindElement('DataHO')
    hash_percent_2 = main_window.FindElement('PercentHO')
    button_change = main_window.FindElement('Button')
    header_change = main_window.FindElement('H')
    in_text = main_window.FindElement('In')
    mid_text = main_window.FindElement('Mod')
    out_text = main_window.FindElement('Out')
    total = main_window.FindElement("Total")
    continue_ = main_window.FindElement("Danger")
    for i in range(0, file_len):
        event, values = main_window.Read(timeout=0)
        b1 = i
        purge_bar.UpdateBar(i)
        purge_percent.Update(f"{i * 100 // file_len}%")
        if ".bmp" not in name[i]:
            del name[i]
        else:
            pass
    files_ = name
    new_len = len(files_)
    out_num = len(files_)
    out_rem = 0
    purge_bar.UpdateBar(file_len)
    purge_percent.Update("100%")
    hash_bar.UpdateBar(current_count=0, max=new_len)
    event, values = main_window.Read(timeout=0)
    if security:
        header_change.Update("HASHING INPUT",
                             text_color='orange')
        for i in range(0, len(files_)):
            event, values = main_window.Read(timeout=0)
            if event == "Button":
                header_change.Update("CANCELED",
                                     text_color='white')
                button_change.Update("close",
                                     button_color=('white', 'black'),
                                     image_data=image_file_to_bytes(data[4], (160, 70)))
                hash_bar.UpdateBar(current_count=0)
                hash_bar_2.UpdateBar(current_count=0)
                progress_bar.UpdateBar(current_count=0)
                purge_bar.UpdateBar(current_count=0)
                in_text.Update(text_color='white')
                mid_text.Update(text_color='white')
                out_text.Update(text_color='white')
                text_purge.Update(text_color='white')
                hash_percent.Update(text_color="white")
                hash_percent_2.Update(text_color="white")
                progress_percent.Update(text_color="white")
                purge_percent.Update(text_color='white')
                total.Update(text_color="white")
                timer.Update(text_color="white")
                if event == "Button":
                    sys.exit()
                else:
                    sys.exit()
            else:
                pass
            temp_name__ = files_[i]
            async_result = pool.apply_async(shav, (temp_name__,
                                                   input_,
                                                   home_,
                                                   'Output_Image_Hash.txt',
                                                   out_num,
                                                   out_rem,
                                                   "verify",
                                                   48000096,
                                                   True))
            payload = async_result.get()
            comp_hash_ = ''.join(payload)
            try:
                if comp_hash_ == comp_hash_other_[temp_name__]:
                    check += 1
                else:
                    pass
            except:
                pass
            b2 = i
            hash_bar.UpdateBar(current_count=i)
            hash_percent.Update(f"{i * 100 // len(files_)}%")
        hash_bar.UpdateBar(current_count=1, max=1)
        hash_percent.Update("100%")
        if check == len(files_):
            hash_percent.Update("100%")
            pass
        else:
            header_change.Update("HASH MISMATCH",
                                 text_color='white')
            button_change.Update("close",
                                 button_color=('white', 'black'),
                                 image_data=image_file_to_bytes(data[4], (160, 70)))
            hash_bar.UpdateBar(current_count=0)
            hash_bar_2.UpdateBar(current_count=0)
            progress_bar.UpdateBar(current_count=0)
            purge_bar.UpdateBar(current_count=0)
            in_text.Update(text_color='white')
            mid_text.Update(text_color='white')
            out_text.Update(text_color='white')
            text_purge.Update(text_color='white')
            hash_percent.Update("100%", text_color='white')
            hash_percent_2.Update(text_color='white')
            progress_percent.Update(text_color='white')
            purge_percent.Update(text_color='white')
            total.Update(text_color="white")
            timer.Update(text_color="white")
            continue_.Update(visible=True)
            event, values = main_window.Read()
            if event == "Danger":
                header_change.Update("PROCESSING",
                                     text_color='yellow')
                button_change.Update("cancel",
                                     button_color=('yellow', 'black'),
                                     image_data=image_file_to_bytes(data[2], (160, 70)))
                hash_bar.UpdateBar(current_count=b2, max=b2)
                hash_bar_2.UpdateBar(current_count=b4)
                progress_bar.UpdateBar(current_count=b3)
                purge_bar.UpdateBar(current_count=b1)
                in_text.Update(text_color='orange')
                mid_text.Update(text_color='yellow')
                out_text.Update(text_color='white')
                text_purge.Update(text_color='red')
                hash_percent.Update("100%")
                hash_percent_2.Update(f"{b4}%")
                progress_percent.Update(f"{b3}%")
                purge_percent.Update("100%")
                total.Update(text_color="yellow")
                timer.Update(text_color="yellow")
                continue_.Update(visible=False)
                pass
            else:
                sys.exit()
    else:
        event, values = main_window.Read(timeout=0)
        in_text.Update("DISABLED", text_color='white')
        hash_percent.Update(text_color='white')
        out_text.Update("DISABLED", text_color='white')
        hash_percent_2.Update(text_color='white')
        button_change.Update(button_color=('orange', 'black'),
                             image_data=image_file_to_bytes(data[1], (160, 70)))
        pass
    header_change.Update("PROCESSING...",
                         text_color='yellow')
    for i in range(0, new_len):
        event, values = main_window.Read(timeout=0)
        if dig is file_len or event == "Button":
            break
        content = open("{}{}".format(input_, str(name[dig])), 'rb').read()
        temp_name = str(name[dig]).split("-{}.bmp".format(dig))
        file_ = "{}{}".format(output_, str(temp_name[0]))
        open(file_, 'ab').write(content[96:])
        dig += 1
        progress_bar.UpdateBar(i)
        progress_percent.Update(f"{i * 100 // new_len}%")
    progress_bar.UpdateBar(current_count=1, max=1)
    progress_percent.Update("100%")
    check_value = dig / new_len
    if check_value >= 1:
        if security:
            header_change.Update("HASHING OUT",
                                 text_color='white')
            files_ = os.listdir(output_)
            nn_ = str(files_[0])
            size = os.path.getsize(f"{output_}/{nn_}")
            out_num = size // 48000000
            out_rem = size % 48000000
            if out_rem > 0:
                out_num += 1
            else:
                pass
            async_result_2 = pool.apply_async(shav,
                                              (nn_,
                                               output_,
                                               home_,
                                               'Input_Data_Hash.txt',
                                               out_num,
                                               out_rem,
                                               "verify",
                                               48000000,
                                               False))
            payload_2 = async_result_2.get()
            hash_ = ''
            for i, hash_ in payload_2:
                hash_ = hash_
                event, values = main_window.Read(timeout=0)
                hash_bar_2.UpdateBar(i)
                hash_percent_2.Update(f"{int(i) * 100 // out_num}%")
                if event == "Button":
                    header_change.Update("CANCELED",
                                         text_color='white')
                    button_change.Update("close",
                                         button_color=('white', 'black'),
                                         image_data=image_file_to_bytes(data[4], (160, 70)))
                    hash_bar.UpdateBar(current_count=0)
                    hash_bar_2.UpdateBar(current_count=0)
                    progress_bar.UpdateBar(current_count=0)
                    purge_bar.UpdateBar(current_count=0)
                    in_text.Update(text_color='white')
                    mid_text.Update(text_color='white')
                    out_text.Update(text_color='white')
                    text_purge.Update(text_color='white')
                    hash_percent.Update(text_color="white")
                    hash_percent_2.Update(text_color="white")
                    progress_percent.Update(text_color="white")
                    purge_percent.Update(text_color='white')
                    total.Update(text_color="white")
                    timer.Update(text_color="white")
                    if event == "Button":
                        sys.exit()
                    else:
                        sys.exit()
            if hash_ == comp_hash_other_2[nn_]:
                button_change.Update("close",
                                     image_data=image_file_to_bytes(data[4], (160, 70)),
                                     button_color=('white', 'black'))
                end_time = int(time.time() - t1)
                timer.Update(f"{end_time} SECONDS",
                             text_color='white')
                total.Update(text_color='white')
                header_change.Update("PROCESS COMPLETE",
                                     text_color='white')
                event, values = main_window.Read()
                if event == "Button":
                    sys.exit()
                else:
                    pass
            else:
                header_change.Update("HASH MISMATCH",
                                     text_color='white')
                button_change.Update("close",
                                     button_color=('white', 'black'),
                                     image_data=image_file_to_bytes(data[4], (160, 70)))
                hash_bar.UpdateBar(current_count=0)
                hash_bar_2.UpdateBar(current_count=0)
                progress_bar.UpdateBar(current_count=0)
                purge_bar.UpdateBar(current_count=0)
                in_text.Update(text_color='white')
                mid_text.Update(text_color='white')
                out_text.Update(text_color='white')
                text_purge.Update(text_color='white')
                hash_percent.Update("100%", text_color='white')
                hash_percent_2.Update(text_color='white')
                progress_percent.Update(text_color='white')
                purge_percent.Update(text_color='white')
                total.Update(text_color="white")
                timer.Update(text_color="white")
                continue_.Update(visible=True)
                event, values = main_window.Read()
                if event == "Danger":
                    header_change.Update("COMPLETE",
                                         text_color='white')
                    button_change.Update("close",
                                         button_color=('yellow', 'black'),
                                         image_data=image_file_to_bytes(data[4], (160, 70)))
                    hash_bar.UpdateBar(current_count=b2, max=b2)
                    hash_bar_2.UpdateBar(current_count=b4)
                    progress_bar.UpdateBar(current_count=b3)
                    purge_bar.UpdateBar(current_count=b1)
                    in_text.Update(text_color='red')
                    mid_text.Update(text_color='orange')
                    out_text.Update(text_color='yellow')
                    text_purge.Update(text_color='red')
                    hash_percent.Update("100%")
                    hash_percent_2.Update("100%")
                    progress_percent.Update("100%")
                    purge_percent.Update("100%")
                    total.Update(text_color="yellow")
                    timer.Update(text_color="yellow")
                    continue_.Update(visible=False)
                    pass
                else:
                    sys.exit()
                event, values = main_window.Read()
                if event == "Danger":
                    sys.exit()
                else:
                    sys.exit()
        else:
            button_change.Update("close",
                                 image_data=image_file_to_bytes(data[4], (160, 70)),
                                 button_color=('white', 'black'))
            end_time = int(time.time() - t1)
            timer.Update(f"{end_time} SECONDS",
                         text_color='white')
            total.Update(text_color='white')
            header_change.Update("PROCESS COMPLETE",
                                 text_color='white')
            event, values = main_window.Read()
            if event == "Button":
                sys.exit()
            else:
                pass
    else:
        delete(output_)
        header_change.Update("CANCELED",
                             text_color='white')
        button_change.Update("close",
                             button_color=('white', 'black'),
                             image_data=image_file_to_bytes(data[4], (160, 70)))
        hash_bar.UpdateBar(current_count=0)
        hash_bar_2.UpdateBar(current_count=0)
        progress_bar.UpdateBar(current_count=0)
        purge_bar.UpdateBar(current_count=0)
        in_text.Update(text_color='white')
        mid_text.Update(text_color='white')
        out_text.Update(text_color='white')
        text_purge.Update(text_color='white')
        hash_percent.Update(text_color="white")
        hash_percent_2.Update(text_color="white")
        progress_percent.Update(text_color="white")
        purge_percent.Update(text_color='white')
        total.Update(text_color="white")
        timer.Update(text_color="white")
        if event == "Button":
            sys.exit()
        else:
            sys.exit()


def gen():
    values = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12345667890!@#$%^&*()_+-="
    for i in range(0, 100):
        sen = [random.choice(values) for i in range(1000000)]
        open("dummy", 'a').write(''.join(sen))


def lazy_proc():
    _1 = multiprocessing.Process(target=gen)
    _2 = multiprocessing.Process(target=gen)
    _3 = multiprocessing.Process(target=gen)
    _4 = multiprocessing.Process(target=gen)
    _5 = multiprocessing.Process(target=gen)
    _6 = multiprocessing.Process(target=gen)
    _7 = multiprocessing.Process(target=gen)
    _8 = multiprocessing.Process(target=gen)
    _9 = multiprocessing.Process(target=gen)
    _0 = multiprocessing.Process(target=gen)
    _1.start()
    _2.start()
    _3.start()
    _4.start()
    _5.start()
    _6.start()
    _7.start()
    _8.start()
    _9.start()
    _0.start()


def initiate():
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
        os.makedirs("{}/BMPMan/".format(home))
        open("{}/BMPMan/settings.txt".format(str(home)), 'w').write("{\n   \"Agree\": \"No\",\n   \"SECURITY\": \"True\",\n   \"THREADS\": \"1\"\n}")
        open("{}/BMPMan/Output_Image_Hash.txt".format(home), 'w').write("{\n}")
        open("{}/BMPMan/Input_Data_Hash.txt".format(home), 'w').write("{\n}")


def agree():
    home_true = str("{}/BMPMan/".format(pathlib.Path.home()))
    agreement = json.load(open("{}settings.txt".format(home_true), 'r'))
    if agreement["Agree"] == "No":
        try:
            license = open("LICENSE", 'r').read()
        except:
            license = ("LICENSE NOT FOUND: User is using software in violation of license\n\n"
                       "By Clicking Accept You Still Agree To The LGPLv3\n\n"
                       "By Not Having The License File, Should You Click Accept, You Forfeit Your Rights To Complain "
                       "About License Violations And Your Rights To The Source Code Of This Software.\n\n"
                       "User: DavidBerdik Has Complete Access To The Source, Regardless\n\n"
                       "Permissions Given by: 78Alpha")

        layout = [[sg.Multiline(license,
                                size=(60, 20))],
                  [sg.Button("Accept",
                             button_color=('white', 'green')),
                   sg.Button("Decline",
                             button_color=('white', 'red'))]]

        window = sg.Window("GNU LESSER GENERAL PUBLIC LICENSE").Layout(layout)

        event = window.Read()

        if str(event[0]) != "Accept":
            sys.exit()
        else:
            agreement["Agree"] = "Yes"
            json.dump(agreement, open("{}settings.txt".format(home_true), 'w'), indent=3)
            yield str(home_true)

            window.Close()
    else:
        yield home_true


def BMPBrowse(button_text='MyBrowse',
              target=(sg.ThisRow, -1),
              file_types=(("ALL Files", "*.*"),),
              initial_folder=None,
              size=(None, None),
              button_color=None,
              change_submits=False,
              font=None,
              disabled=False,
              image_data=None):
    return sg.Button(button_text=button_text,
                     button_type=sg.BUTTON_TYPE_BROWSE_FILE,
                     target=target,
                     file_types=file_types,
                     initial_folder=initial_folder,
                     size=size,
                     change_submits=change_submits,
                     disabled=disabled,
                     button_color=button_color,
                     font=font,
                     image_data=image_data,
                     border_width=0)


def settings(font, home_, data=None):
    settings_file = "{}settings.txt".format(home_)
    settings = json.load(open(settings_file, 'r'))
    if settings["SECURITY"] == "True":
        security = True
    else:
        security = False
    settings_screen = [[sg.Text("BMPMAN SETTINGS",
                                font=font,
                                size=(25, 2),
                                text_color='yellow',
                                background_color='black',
                                justification='center')],
                       [sg.Checkbox(text="SECURITY",
                                    default=security,
                                    background_color='black',
                                    tooltip='ENABLE/DISBALE HASHING',
                                    font=font,
                                    text_color='yellow')],
                       [sg.Spin([i for i in range(1, 1000)],
                                background_color='black',
                                text_color='yellow',
                                initial_value=int(settings["THREADS"])),
                        sg.Text(font=font,
                                text="THREADS",
                                text_color='yellow',
                                background_color='black',
                                justification='right',
                                tooltip="CHANGE THREAD COUNT")],
                       [sg.Button(button_text="CLOSE",
                                  font=font,
                                  border_width=0,
                                  button_color=('yellow', 'black'),
                                  image_data=image_file_to_bytes(data[2], (160, 70)))]]

    set_window = sg.Window("SETTINGS",
                           font=font,
                           background_color='Black',
                           grab_anywhere=True, alpha_channel=0.8).Layout(settings_screen)
    event, values = set_window.Read()
    settings["SECURITY"] = str(values[0])
    settings["THREADS"] = values[1]
    json.dump(settings, open(settings_file, 'w'), indent=3)
    set_window.Close()
    core()

def core():
    result = str(''.join(agree()))

    version = "2.0.2"

    out_images = 'Output_Images/'
    out_data = 'Output_Data/'
    in_images = 'Input_Images/'
    in_data = 'Input_Data/'

    font = 'Arial'
    try:
        font = "BMPMan"
    except:
        pass

    red_box = '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'
    orange_box = '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'
    yellow_box = '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'
    yellow_browse = 'iVBORw0KGgoAAAANSUhEUgAAAOQAAABOCAYAAAAw0LoFAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAH8SURBVHic7dchbmJRGIbh/05GFYmmCoccR+pnUV1APXvoImYDbIAgMVSScW1CMGfkKCAk0PNBnic56l7xmTc5Z2itWj2ej2Go594juJ3WaltVk947ru1H7wHAf4KEID97D7jE4VC1Wp3/b7+vp6r6dfNBdPP1VU+jUe8V1zfc0xtys6maTnuvIMF2WzV5uBekKytEESQEOfmGXK+rlsvvmnLebtd7ASne36vG494rLjefV81mJ35ordqxs1hUq3Ic51pnsTjeW2vVXFkhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhyNBatWMf1+uq5fI755y221W9vvZeQYK3t6rxuPeKy83nVbPZ8e8ng0yz2VRNp71XkGC7rZpMeq+4PldWCCJICHJXV9bDoWq1Ov/ffl9/X17q9+0X0cvnZ/0ZjeoOX5Gn3VWQF/gYhnruPYLbaa22VfVwr0hXVggiSAjyD4XjRPXZ0K+/AAAAAElFTkSuQmCC'
    white_box = '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'
    danger = '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'
    sg.FileBrowse = BMPBrowse
    data = [red_box, orange_box, yellow_box, yellow_browse, white_box, danger]
    icon_ = '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'
    icon = image_file_to_bytes((icon_), (256, 256))
    layout = [[sg.Text('BMPMAN DEBUG {}'.format(version),
                       font=font, text_color='yellow',
                       background_color='black',
                       justification='center',
                       size=(25, 2))],
              [sg.Text('INPUT',
                       font=font,
                       justification='right',
                       background_color='black',
                       text_color='yellow'),
               sg.InputText('USE_DEFAULT',
                            font=font,
                            text_color='#909090'),
               sg.FolderBrowse(image_data=image_file_to_bytes((yellow_browse), (330, 40)),
                               button_text="BROWSE",
                               border_width=0,
                               button_color=('yellow', 'black'),
                               font=font)],
              [sg.Text('OUTPUT',
                       font=font,
                       justification='right',
                       background_color='black',
                       text_color='yellow'),
               sg.InputText('USE_DEFAULT',
                            font=font,
                            text_color='#909090'),
               sg.FolderBrowse(image_data=image_file_to_bytes((yellow_browse), (330, 40)),
                               button_text="BROWSE",
                               border_width=0,
                               button_color=('yellow', 'black'),
                               font=font)],
              [sg.Button('make',
                         font=font,
                         border_width=0,
                         image_data=image_file_to_bytes((red_box), (160, 70)),
                         button_color=('red', 'black')),
               sg.Button('unpack',
                         font=font,
                         border_width=0,
                         image_data=image_file_to_bytes((orange_box),(160, 70)),
                         button_color=('orange', 'black')),
               sg.Button('options',
                         font=font,
                         border_width=0,
                         image_data=image_file_to_bytes((yellow_box), (160, 70)),
                         button_color=('yellow', 'black')),
               sg.Button('exit',
                         font=font,
                         border_width=0,
                         image_data=image_file_to_bytes((white_box), (160, 70)),
                         button_color=('white', 'black'))]]

    window = sg.Window(title='BMPMan V.{}'.format(version), keep_on_top=False, no_titlebar=False,
                       background_color='Black', grab_anywhere=True, alpha_channel=0.8, icon=icon).Layout(
        layout)

    event, values = window.Read()
    if str(event) == "make":
        if str(values[0]) != "USE_DEFAULT" and str(values[1]) != "USE_DEFAULT":
            in_data = "{}/".format(str(values[0]).replace('\\', '/'))
            out_images = "{}/".format(str(values[1]).replace('\\', '/'))
            files = os.listdir(in_data)
            name_list = [str(name) for name in files]
            window.Close()
            generic_upd3(name_list, input_=in_data, output_=out_images, home_=result, font_=font, data=data, icon=icon)
        elif str(values[0]) == "USE_DEFAULT" and str(values[1]) == "USE_DEFAULT":
            files = os.listdir(in_data)
            name_list = [str(name) for name in files]
            window.Close()
            generic_upd3(name_list, input_=in_data, output_=out_images, home_=result, font_=font, data=data, icon=icon)
    elif str(event) == "unpack":
        if str(values[0]) != "USE_DEFAULT" and str(values[1]) != "USE_DEFAULT":
            in_images = "{}/".format(str(values[0]).replace('\\', '/'))
            out_data = "{}/".format(str(values[1]).replace('\\', '/'))
            files = os.listdir(in_images)
            name_list = [str(name) for name in files]
            window.Close()
            rip_upd3(name_list, input_=in_images, output_=out_data, home_=result, font_=font, data=data, icon=icon)
        elif str(values[0]) == "USE_DEFAULT" and str(values[1]) == "USE_DEFAULT":
            files = os.listdir(in_images)
            name_list = [str(name) for name in files]
            window.Close()
            rip_upd3(name_list, input_=in_images, output_=out_data, home_=result, font_=font, data=data, icon=icon)
    elif str(event) == "options":
        window.Close()
        settings(font=font, home_=result, data=data)
    else:
        sys.exit()


initiate()
core()
