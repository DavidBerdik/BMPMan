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


def generic_upd3(files, input_, output_, home_, font_, data):
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
                            alpha_channel=0.8).Layout(main_data)
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


def rip_upd3(name, input_, output_, home_, font_, data):
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
                            alpha_channel=0.8).Layout(main_data)
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

    version = "2.0.1"

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
    orange_box = 'iVBORw0KGgoAAAANSUhEUgAAAXEAAABLCAYAAACGEbfbAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAgSSURBVHic7d3fl1VlHcfx9zPQyDTAyFBLLJMhJbELMbvouhsGSvAXiBp69gGEtF8qRmu1Kods1UpDa7UqBzEOgUIiqJWVMczMMlrSf1Ctyla1qst+MGPz6zxd7DnmjMzsZ+999s/zeV3Cs85+mIv3fHnOPvsYJJCt8DCGL2S9DxGRWfoWZL2DvLNVvgIKuIjkzj5TY5/Jehd5Zj2+DHwx632IiMxgeMQc4nMAbVnvJa8UcBHJqYcbAQfQJH4Btso+LF/Keh8iIrM8amrsffMfKOKzWI8+4KGs9yEiMstbAg46TplBAReRnPrqhQIOmsTfYD0eAvqC1p2fgGOvgU1+SyJSUmuXwYfe6bjY8jVzmM/P9dcLm7SnQrMV9uIQ8NFJ2HQGhv6R/J5EpJw+uBxO9zouNuw3tbkD7i9pcbbCXgxfD1o3OgnXDyjgIhLddcthoBeWtTssNuw3h3gweFkLsx6fBR4JWqeAi0hc1y2H0+ug+yKn5Y+ZGntcFrbsG5thAr5RRygiEkNSAYcWncTDBnzw7ylsSkRKKcmAQwtG3FZ5EMujQesUcBGJ6wPd/hm4U8Atj5vDPBD2Gi11nBIm4JsUcBGJIY2AA7TMUwxthT3AN4LWvT7lB/yMAi4iEYUKOHwzasChRSZxW2EPRgEXkeRd2+3fB+4c8Br3x7le6c/ErccDwP6gdY2AD/wthU2JSCldOz2BL08p4FDySdw14GNTsGVIAReR6EIG/FvUoh+hvFlpJ3Fb5X4sjwWtG5uCW4bgpb+msSsRKaOQAe+nxj2mSY9gKmXEFXARScvabjjjGnDDAQ7x8WYFHEp4nGI97nMJ+HgdNg8r4CIS3dpuGFiXXcD9ly0R63Ef8HjQuvG6P4H/5C8pbEpESqkR8Hcsclr+JDV2NzvgUKJJPEzANyvgIhLDNcvyEXAoySRuPT6DH/B5/z2NgP9YAReRiK5Z5p+B5yHgUIJJ3FbZjQIuIim4ugtedp3ALQfpaf4Z+GyF/ti9rbALeAKHgG9RwEUkhjVdMLQeVnQ4LLYcZBW7TR/1pPdV2OMUW2EXxj3gP1LARSSiUAGHp+hhVxoBh4JG3HrcDfSjgItIwvIccCjgmXiYgN86rICLSHRrumDQPeDfTzvgULBJPGzAX/xzKtsSkRK6anoCv9Q94HenHXAo0CRuq+zE8U3MrcMKuIhEV5SAQ0EmcVtlJ5Z+An7pTExP4C8o4CISUaiAWw6xip1ZBRwKMInbCjsUcBFJw1VdMNhbnIBDzidxW2EHhgMo4CKSsPct9Sfwd73daXmNHnZkHXDI8SQeJuBbhxVwEYmuqAGHnE7i1mM78CQBAZ+ysO0VOP5aOvsSkfIJGfDjjLDNnGAq4W05y13EFXARScvqpTBc4IBDzo5TwgT8zl8q4CIS3eqCT+ANuYm4rVIlRMCP/TGdfYlI+TQC/m63gP+QHu7MY8AhJxG3VapYDuIQ8LsUcBGJIULAt5k+JhPeVmSZn4lbDw94CseAP6OAi0hEoQJueJaVfCzPAYeMnyceJuAVBVxEYrhy+k3MMgUcMpzErcdtwFECfpE0Av60Ai4iEfUs9ifwnsUOiwsUcMjoTDxMwL2zCriIRLcyTMDhRJECDhlE3FbZiuUIjgE/+oeUNiYipbNysX+E4hzwHu4oUsAh5eMUW2UrdY5iWDjfOgVcROIKFXDLc6zi9qIFHFKMuK1wK/C0S8CrZ+GIAi4iETWOUFaVPOCQUsQVcBFJy+WdMLyhNQIOKUQ8TMC3n4UfKOAiElGogMNJ2rndHGAi4W0lKtGIW48tWJ4JCnh9egJXwEUkqlYMOCR4d0qYgG//lQIuItFd3hniDBxOlSXgkNAnNm2VzViOuQb88O+T2IWItIJGwN+7xGn5Kdq5rSwBhwQmcVtlM/XggFvg3nMKuIhE954WDzg0OeJhAn7Pq9D/22ZeXURaSciAv8QS7ihbwKGJb2zaCrdgOAa8bd51wL2vwhMKuIhE1Aj4FW4B/ylLuNl8m7GEt5WJpkRcAReRtCjgM8WOuAIuImm5rNP/KL1TwA0/YzE3lTngwPxn10Gsx83gFvBPnFPARSS6yzphqFcBny3yJD4d8OM4Bvx7v4l6JRFpdY2AX7nUYXELBRwiRjxMwD95Dr6rgItIRCs6YHA9XN3ltPznwE2mxn+T3VV+hI64rfBRDCeBi+ZdhwIuIvEo4MFCRdx6fAQ4hQIuIgm7pMO/C0UBn5/zh33CBPxTCriIxHBJBwz2KuAunCZxexcbaON5HAP+HQVcRCJqBPz9Fzstfxm4sVUDDg6TeJiAf/rXCriIRKeAhzfvJG6rXI/lJNAe9ELP/Qn6f9esbcFUHf6d0lMO/jXhP1ExaaOTMDaV/HUmLJwv3RMipOwunX4Tc42OUEKZM+Kud6FIa/vnuP+/sKSNTMB4PfnrjNdhJIUv6rLW/9ml4T+TMJnCz25sCkZjDCkfXgGrXe4D1wQ+wwUjroCLSE79ArhBAf+/t0TceqwHngcWpb8dEZE5nWaEG8wJXs96I3ky443N6dsIX0ABF5F8UcDn8MYk7noXiohIqiwDjLJJAb+whQC2wjpM8Ad5RERS9gp1blTA59ZmPdZjeBEdoYhIvgzSzgZzhJGsN5JnC2njPLAx9ivVWQosiP06QSwdpPELx/+eULfvDonvYpr4VXlzsnTSFnzPfxOu0w50pnAdg/+zS55hCTGfv+9oEdCRwnUWAG439MXXRfjv8x2knY3mAKNJbKhM/gfdZQnjLSo0yQAAAABJRU5ErkJggg=='
    yellow_box = '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'
    yellow_browse = 'iVBORw0KGgoAAAANSUhEUgAAAOQAAABOCAYAAAAw0LoFAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAH8SURBVHic7dchbmJRGIbh/05GFYmmCoccR+pnUV1APXvoImYDbIAgMVSScW1CMGfkKCAk0PNBnic56l7xmTc5Z2itWj2ej2Go594juJ3WaltVk947ru1H7wHAf4KEID97D7jE4VC1Wp3/b7+vp6r6dfNBdPP1VU+jUe8V1zfc0xtys6maTnuvIMF2WzV5uBekKytEESQEOfmGXK+rlsvvmnLebtd7ASne36vG494rLjefV81mJ35ordqxs1hUq3Ic51pnsTjeW2vVXFkhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhiCAhyNBatWMf1+uq5fI755y221W9vvZeQYK3t6rxuPeKy83nVbPZ8e8ng0yz2VRNp71XkGC7rZpMeq+4PldWCCJICHJXV9bDoWq1Ov/ffl9/X17q9+0X0cvnZ/0ZjeoOX5Gn3VWQF/gYhnruPYLbaa22VfVwr0hXVggiSAjyD4XjRPXZ0K+/AAAAAElFTkSuQmCC'
    white_box = 'iVBORw0KGgoAAAANSUhEUgAAAXEAAABLCAYAAACGEbfbAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAZYSURBVHic7Z3JbxTpHYbfAjKZKJokN4PkhQONmwsN5sAlFwOKAmadTBJ2JiurlH0iZRvIRImUdY5hsh3JwiiJlGUyM/Ih/wNc2C4sBxYZcHfcje03B5PJxIO76oOvqroyzyM9B9vl+j61fn5cqi7ZiSAV2y9J+lbZ+wAAmMfJJWXvoNex/T1J3yx7HwAA8ziVJMmppOxd9DK2vyvp22XvAwBgHj9MkuTrkrSo7J30KgQcAHqUl/4TcEniSvwR2D4l6Ttl7wMAYB4/SpLkhbd/givxedg+KQIOAL3HOwIuEfH/4WHAXyx7HwAA8/j+owIucTvlLWy/KOlk2nGTk5M6c+aMbOe/KQD4v6TRaGj9+vVZD/9BkiTfyHM/lcf2C85As9n06OioJSEiPpbr1q3znTt3siTHtn8s6A4BR8SiHBkZIeAxsf01Ao6IRTgyMuLbt29nDfhPBN0JCfiGDRtKHwBErK4EPDIEHBGLkoBHxvZXCTgiFuHatWtDAv5TQXdCAr5x48bSBwARqysBj4ztr2R5JVutFgFHxCcyMOA/E3QnJOCbNm0qfQAQsbquWbPGt27dIuCxsP1lAo6IRUjAI5M14FNTUx4bGyt9ABCxugYG/GXb/NmTbtj+EgFHxCIMDPjPCXgKBBwRi7LRaIQE/DQBT8H2F7O8ku1221u3bi19ABCxujYaDd+8eZOAx4KAI2JRBgb8FQKeQkjAt23bVvoAIGJ1Xb16NQGPie0v2J4l4IiYtwQ8MrYPE3BELMJVq1b5xo0bWQP+C9v8C8xu2P581oBv37699AFAxOpar9cJeEwIOCIWZWDAf0nAU7D9OQKOiEVIwCMTEvAdO3aUPgCIWF3r9bqvX7+eNeC/IuApEHBELMrh4WECHhPbn7U9kyXgO3fuLH0AELG6EvDIZA14p9Mh4Ij4RAYG/NcEPAXbnyHgiFiEw8PDvnbtGgGPBQFHxKJcuXJlSMB/Q8BTCAn4rl27Sh8ARKyuBDwytj+dJeDT09PevXt36QOAiNU1MOBnbC8WLAwBR8SirNVqBDwmIQHfs2dP6QOAiNW1Vqv56tWrBDwWtj9FwBGxCAMD/lvbSwQLExLwvXv3lj4AiFhdCXhkbD9PwBGxCAMD/jsCnkJIwPft21f6ACBidV2xYgUBj4nt3banCTgi5u3y5ct95coVAh6LkIDv37+/9AFAxOo6NDQUEvDfE/AUbH/S9gMCjoh5S8AjQ8ARsSgDA/4HAp6C7U9kDfiBAwdKHwBErK5DQ0O+fPkyAY8FAUfEohwcHCTgMQkJ+MGDB0sfAESsroEBP2v7PYKFsf3xLAGfmZkh4Ij4RBLwyIQE/NChQ6UPACJW18HBQV+6dClrwF8l4CnYfo6AI2IREvDIZA347OysDx8+XPoAIGJ1HRgYIOAxIeCIWJQDAwO+ePFi1oD/xfZ7BQtj+2O2O1kCfuTIkdIHABGra2DA/0rAUyDgiFiUBDwyBBwRi7K/vz8k4H8j4CnYfjZrwI8ePVr6ACBide3v7/eFCxcIeCwIOCIWJQGPTEjAjx07VvoAIGJ1Xbp0qc+fP5814H+3/bRgYWyP2Z4i4IiYtwQ8Mra3EHBELMK+vj4CHpOQgB8/frz0AUDE6trX1+dz584R8FjY3kzAEbEIAwP+GgFPISTgJ06cKH0AELG6EvBwkm5ftL1V0quSnko70dmzZ3X69OlY+9LMzIzu3bsX7XzduHv3rmZnZ3Nfp9Vqqd1u577OgwcPNDk5mfs6ADFZtmyZxsfHVa/Xsxz+mqRdSZJM5bytnmfBiNse01zAed4SFmRiYkK2c1+n2Wyq0+nkvk6n01Gz2cx9HduamJjIfR1Jun//vqanp3Nfp91uq9VqPfb3j46OqlarZTn0H5J2EvA5HhlxAg4APcrrknYQ8P/yjojb/qikP0p6199rAoCe4g3NBfxfZW+kl1j09g9sb5H0JxFwAOgtCPgCvHUlbnuz5q7AuYUCAL3Em5K2E/BHk0iS7Y9I+rO4AgeA3uKfkrYkSZL/u80VZdHDe+AEHAB6jXFJmwl4dxLbH1acgH9A0uII50njfSrmF84SSc8UsI4kfUgpz+xH4v3K8Mx/BJ56uFbeJJp77YrgGc3NRN48rbkZz5vFmvuZLYIPat77bxkYl7QtSZLHf2bxXcK/AU/T9EKvebZiAAAAAElFTkSuQmCC'
    danger = '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'
    sg.FileBrowse = BMPBrowse
    data = [red_box, orange_box, yellow_box, yellow_browse, white_box, danger]

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
                       background_color='Black', grab_anywhere=True, alpha_channel=0.8).Layout(
        layout)

    event, values = window.Read()
    if str(event) == "make":
        if str(values[0]) != "USE_DEFAULT" and str(values[1]) != "USE_DEFAULT":
            in_data = "{}/".format(str(values[0]).replace('\\', '/'))
            out_images = "{}/".format(str(values[1]).replace('\\', '/'))
            files = os.listdir(in_data)
            name_list = [str(name) for name in files]
            window.Close()
            generic_upd3(name_list, input_=in_data, output_=out_images, home_=result, font_=font, data=data)
        elif str(values[0]) == "USE_DEFAULT" and str(values[1]) == "USE_DEFAULT":
            files = os.listdir(in_data)
            name_list = [str(name) for name in files]
            window.Close()
            generic_upd3(name_list, input_=in_data, output_=out_images, home_=result, font_=font, data=data)
    elif str(event) == "unpack":
        if str(values[0]) != "USE_DEFAULT" and str(values[1]) != "USE_DEFAULT":
            in_images = "{}/".format(str(values[0]).replace('\\', '/'))
            out_data = "{}/".format(str(values[1]).replace('\\', '/'))
            files = os.listdir(in_images)
            name_list = [str(name) for name in files]
            window.Close()
            rip_upd3(name_list, input_=in_images, output_=out_data, home_=result, font_=font, data=data)
        elif str(values[0]) == "USE_DEFAULT" and str(values[1]) == "USE_DEFAULT":
            files = os.listdir(in_images)
            name_list = [str(name) for name in files]
            window.Close()
            rip_upd3(name_list, input_=in_images, output_=out_data, home_=result, font_=font, data=data)
    elif str(event) == "options":
        window.Close()
        settings(font=font, home_=result, data=data)
    else:
        sys.exit()


initiate()
core()
