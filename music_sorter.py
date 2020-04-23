import os
import shutil
import eyed3
import sys
import tkinter as tk
from tkinter import filedialog
#block and enable print because we dont want the eyed3 to print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

#Windows illegal directory names,used to create a valid Artist and/or Album directory
def check_illegal_name(s):
    illegals="/\:*<>|."
    for i in illegals:
        if i in s:
            return True
    return False

def strip_illegals(s):
    new_s=""
    illegals="/\:*<>|."
    for i in s:
        if i not in illegals:
            new_s+=i
    return new_s
    
    
def sort_music_dir(direc):
    blockPrint()
    songs=os.listdir(direc)
    for i in songs:
        try:
            song=eyed3.load(direc+'/'+i)
            artist=song.tag.album_artist
            album=song.tag.album
        except:
            continue
        if not artist:
            artist="Various Artists"
        if not album:
            album=""
        if check_illegal_name(artist):
            artist=strip_illegals(artist)
        if check_illegal_name(album):
            album=strip_illegals(album)
        if not os.path.exists(direc+'/'+artist):
            os.mkdir(direc+'/'+artist)
        if not os.path.exists(direc+'/'+artist+'/'+album):
            os.mkdir(direc+'/'+artist+'/'+album)
        shutil.move(direc+'/'+i,direc+'/'+artist+'/'+album)
    enablePrint()
    return
def main():
    tk.Tk().withdraw()
    org_directory=tk.filedialog.askdirectory()
    sort_music_dir(org_directory)
    print("",end="\r")
    input("Operation Complete.\nPress enter to exit.")

if __name__=='__main__':
    main()