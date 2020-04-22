import os
import shutil
import eyed3
import sys
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
    try:
        songs=os.listdir(direc)
    except:
        enablePrint()
        direc=input("Please give a valid directory path.:")
        sort_music_dir(direc)
        return
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
    org_directory=input("Give full path of the Directory you want to sort:")
    sort_music_dir(org_directory)
    input("Operation Complete.\nPress enter to exit.")

if __name__=='__main__':
    main()
