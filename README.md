# BMPMan
Pronounced "Bump-Man"

Simply, this is a utility to make an image safe BMPthat contains up to 48 MB of data per image.

## Usage

The main usage of this program is through the use of 2 commands with their own internal arguments (this will be changed to sys.argv() soon)

First, you run the script...

./Main.py

You will get 2 options, "make" and "unpack"

Make | Takes raw data and inputs it into a predetermined BMP "container" or "containers". Should the data exceed 48 MB, it will just be put into more files.

Unpack | Takes the image data, strips the generic BMP header and buffer, and reassembles the original file, in a later version checksums will be used to make sure files are like the originals. You also have to input the number of files, but this may be automated in the future.

## Purpose

Building on the idea of UDS from stewartmcgown, this method creates BMP files that are Google Photos safe (currently, later versions may have 'default' options to work on seperate platforms). These Google Photo safe images can be backed up using the free storage option, allowing you to have "Unlimited Google Drive Storage" via images. By creating albums, you can have a full directory containing all the images, allowing for easy sharing, downloading and unpacking with friends.

## Future

If I get around to it adn learn enough about the Google API, It may be possible to upload photos directly with the script, create albums, and make the process more seamless. Also, adding sys.argv() functions, maybe some multithreading, general improvements and such.

### To Google

I am sorry for what you have just looked at, and the disgust you are probably feeling, but hey, at least it was fun.
