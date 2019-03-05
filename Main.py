from __future__ import print_function
import binascii
import random
import gc


def test():
    with open("dummy.txt", 'rb') as f:
        content = f.read()

    print(binascii.unhexlify(content))

data1 = "424d564d0c0300000000360400002800"
data2 = "0000ee1b0000ee1b0000010008000000"
data3 = "000020490c0300000000000000000000"
data4 = "00000000000000000000000080008080"
data5 = "0000c0c0c000c0dcc000f0caa6000020"
lib = ["424d564d0c0300000000360400002800", "0000ee1b0000ee1b0000010008000000", "000020490c0300000000000000000000", "00000000000000000000000080008080", "0000c0c0c000c0dcc000f0caa6000020", "400000206000002080000020a0000020", "c0000020e00000400000004020000040"]

def base():
    with open("5.test", 'rb') as main:
        content = main.read()
        zip = ''
        text = binascii.unhexlify(content)
        temp = 0
        for line in content:
            if line != '00000000000000000000000000000000':
                print(line)
            else:
                while line != '00000000000000000000000000000000':
                    zip += line

def mod():
    file_name = raw_input("Name of file: ")
    output_name = raw_input("Name to output: ")
    local = ''
    with open(file_name, 'rb') as core:
        content = core.read()
    #for line in content:
    line2 = content.encode('hex')
        # print(binascii.unhexlify(line2))
    #    if line2 == '0':
    #        line2 = '00'
        #print(line2)
    #    local += line2
        #print(line2)
    #print(local)
    #print(content)
    #print(content.encode('hex'))
    #print(line2)
    x = 0
    y = 0
    temp = ''
    for line in line2:
        if x != 160:
            print("skipped " + str(x))
            x += 1
        elif x == 160:
            if len(temp) == 8:
                if '00000000' in temp:
                    exit()
                else:
                    temp = ''
            elif len(temp) < 8:
                local += line
                temp += line
            #print('', end='')
            else:
                print("Logic Error")
        #elif y != 2:
        #if '00' not in temp:
        #    local += str(line)
        #else:
        #    print(local)
        #    break
    loc_decode = local.decode('hex')
    dec_content = line2.decode('hex')
    if dec_content == content:
        print("Match")
    else:
        print("Undetermined")
    with open(output_name, 'wb') as byte_file:
        #for i in range(len(local)):
            #byte_file.write(local[i])
        byte_file.write(loc_decode)

def generic():  # Template, do not delete
    filename = raw_input("Filename: ")
    sequence = '1234567890ABCDEF'
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    #new = base.codecs.encode('hex')
    #print("\n")
    #print(base)
    #print("\n")
    with open(filename, 'rb') as byter:
        content = byter.read()
        byter.close()
    with open("Generic.bmp", 'wb') as byteman:
        byteman.write(base)
        byteman.write('0' * 32)
        byteman.write(content)
        byteman.close()
    #with open("generic.bmp", 'wb') as byter:
    #    byter.write(base)
    #    temp = ''
    #    for x in range(10):
    #        for i in range(12000000):
    #            temp += str(random.choice(sequence))
    #        #byter.write(secrets.choice(sequence))
    #        byter.write(binascii.unhexlify(temp))
    #        temp = ''
    #       gc.collect()

    #    byter.close()

def rip():  # Template, do not delete
    filename = raw_input("Filename: ")
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer = str('0' * 32)
    with open(filename, 'rb') as generic:
        content = generic.read()
    temp = ''
    data = ''
    for line in content:
        temp += line
        if len(temp) <= int(len(base) + len(buffer)):
            print("Omitting... ", end='')
        else:
            data += line
    with open("output.txt", 'wb') as out:
        out.write(data)

def generic_upd():
    lim = 48000000
    ext = ".bmp"
    filename = raw_input("Filename: ")
    base = binascii.unhexlify('424DD2E4DE02000000007A0000006C00000037130000BF0C0000010018000000000058E4DE02130B0000130B0000000000000000000042475273000000000000')
    buffer = ''
    name_dig = 0
    with open(filename, 'rb') as byter:
        content = byter.read()
        byter.close()
    for letter in content:
        buffer += letter
        if len(buffer) == lim:
            file = str(filename) + str(name_dig) + str(ext)
            with open(file, 'wb') as byteman:
                byteman.write(base)
                byteman.write('0' * 32)
                byteman.write(buffer)
                byteman.close()
            name_dig += 1
            buffer = ''
            gc.collect()
    file = str(filename) + str(name_dig) + str(ext)
    with open(file, 'wb') as byteman:
        byteman.write(base)
        byteman.write('0' * 32)
        byteman.write(buffer)
        byteman.close()
    name_dig += 1
    buffer = ''
    gc.collect()

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
        for line in content:
            temp += line
            if len(temp) <= int(len(base) + len(buffer)):
                print("Omitting... ", end='')
            else:
                data += line
        with open(outname, 'ab') as out:
            out.write(data)
        gc.collect()

def gen():
    sen = ''
    for i in range(100000000):
        sen += '0'
    with open("dummy", 'w') as dummy:
        dummy.write(str(sen))
        dummy.close()

#mod()
#generic()
#rip()

user_choice = raw_input("Make or unpack? ")
if user_choice ==  str("make"):
    generic_upd()
elif user_choice == str("unpack"):
    rip_upd()
elif user_choice == str("gen"):
    gen()
else:
    print("Error")