#Delete Last File
import os
import glob
#Delay
import time
import sys


def deletelastvideo():
    #Remove the last file uploaded
    print("Removing the last .mp4 file...")
    try:
        mp4_files = glob.glob(
            "*.mp4")  #consider only files with .mp4 extension
        newest_file = max(mp4_files,
                          key=os.path.getctime)  #Get the last video uploaded
        os.remove(newest_file)  #Remove last video
        print("Last video: " + newest_file + " removed")
    except:
        print("Remove Failed: script is using the file: " + newest_file)
        time.sleep(5)
        return deletelastvideo()


deletelastvideo()
os.system("python upload_video.py")
sys.exit()
