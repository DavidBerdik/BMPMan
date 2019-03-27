# BMPMan

A utility made to wrap data in a bitmap file. BMPMan files will function as images wherever placed and are limited only to the media with which they are distributed. The core design of this application is centered around Google Photos and to be compliant with its core limitations. This application can not currently interact with any online media, it is strictly an offline app until modified thusly.

Updated to use Python3! So long 2.7!

## How To Use

First, you have to execute as your OS supports, you will be greeted with a GUI window that displays the version and options.

![alt text](https://raw.githubusercontent.com/78Alpha/BMPMan/master/Images/MainMenu.png)

BMPMan creates images and unpacks them from directories, you can use whatever directories you like, but if you don't mind too much, it generates default folders:

``Input_Data
 Input_Images
 Output_Data
 Output_Images``
 
The **Make** command takes data from *Input_Data* or your own input folder and output it to *Output_Images* or your own output folder. Each image will be of a size maxed out at ~50 MB.
 
![alt text](https://raw.githubusercontent.com/78Alpha/BMPMan/master/Images/makehash.png)
![alt text](https://raw.githubusercontent.com/78Alpha/BMPMan/master/Images/makebuild.png)
![alt text](https://raw.githubusercontent.com/78Alpha/BMPMan/master/Images/MakeHashImages.png)
 
The **Unpack** command takes data from *Input_Images* or your own input folder and output it to *Output_Data* or your own output folder.
 
![alt text](https://raw.githubusercontent.com/78Alpha/BMPMan/master/Images/unpackimageshash.png)
![alt text](https://raw.githubusercontent.com/78Alpha/BMPMan/master/Images/unpackmakeog.png)
![alt text](https://raw.githubusercontent.com/78Alpha/BMPMan/master/Images/hashoutunpack.png)

The **Cancel** button functions like a normal cancel button, and should halt the application.

Each progress bar loads based on image interaction rather than number of files being worked with. The progress bar can alse be canceled, stopping the entire program and **Deleting All Files In The Output Directory**. Make sure the folders you are using are empty as data loss may occur.

## License

This software is licensed under the LGPLv-3, and will be compliant to the GPL licenses included in the imported packages. Packages imported and used by this project that are not in the standard library are:

[PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) | [License](https://github.com/PySimpleGUI/PySimpleGUI/blob/master/license.txt)

Users with permission to act out of bounds of license are:

*DavidBerdik*

## Notice

If you want the theme I use to be an exact replica of the binary versions, use my fork of PySimpleGUI. It's altered specifically to make the theme look like a theme, without cookie cutter boxes...

https://github.com/78Alpha/PySimpleGUI/blob/master/PySimpleGUI.py
