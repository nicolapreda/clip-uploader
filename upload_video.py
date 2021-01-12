#YouTube API
from google.cloud import bigquery
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
#Get the last file in the folder
import glob
import os
#Check if file is corrupted
import integv
#Add delay in code
import time
#Delete last file
import sys
import subprocess
#Limit bandwidth
import asyncio
import aiohttp
import aiothrottle

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,
                         SCOPES)  #Start Youtube API

mp4_files = glob.glob("*.mp4")  #consider only files with .mp4 extension
try:

    newest_file = max(mp4_files, key=os.path.getctime)  #get the last file
except:
    print("No videos to upload.")
    time.sleep(60)
    os.system("python upload_video.py")
    print("Restarting the script..."
          )  #if there aren't any files, the script restarts
    exit()


def filevalidator():
    with open(newest_file, "rb") as f:
        filevalidator = f.read()
    # verify using the file and file_type
    integv.verify(filevalidator, file_type="mp4")  # True

    # a corrupted file (in this case, shortened by one byte) will not pass the verification
    integv.verify(filevalidator[:-1], file_type="mp4")  # False

    # if the file path contains a proper filename extension, the file_type is not needed.
    verified_latest_file = integv.verify(newest_file)  # True

    if verified_latest_file == False:
        print("File corrupted\nRestarting Script in 60 seconds...")
        time.sleep(60)
        os.system("python upload_video.py")
        exit()


filevalidator()

file_title = os.path.splitext(newest_file)[0]  #get the title of file

request_body = {
    'snippet': {
        'categoryI': 19,
        'title': file_title,
        'description': file_title + " (video loaded by python script)"
    },
    'status': {
        'privacyStatus': 'private',
        'selfDeclaredMadeForKids': False,
    },
    'notifySubscribers': False
}
try:
    #Set bandwith limit (YT Queries limits set to 10.000)
    aiothrottle.limit_rate(200 * 1024)
    print("Set Bandwidth limit to 200kb/s")
    
    #Upload last file
    mediaFile = MediaFileUpload(newest_file)
    print('Upload in progress...')

    response_upload = service.videos().insert(
        part='snippet,status', body=request_body,
        media_body=mediaFile).execute()  #Upload Video On Youtube
except:
    print("Error in the Youtube API")
    time.sleep(5)
    os.system("python upload_video.py")
    print("Restarting the script..."
          )  #if there aren't any files, the script restarts
    exit()

print(file_title + " uploaded successfully")
time.sleep(5)  #5 seconds delay


def spawn_program_and_die(exit_code=0):

    # Start deletelastvideo.py
    subprocess.Popen("python deletelastvideo.py")
    # We have started the program, and can suspend this interpreter
    sys.exit(exit_code)


spawn_program_and_die()
