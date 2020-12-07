#YouTube API
from google.cloud import bigquery
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
#Get the last file in the folder
import glob
import os
#Add delay in code
import time


CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) #Start Youtube API

mp4_files = glob.glob("*.mp4")  #consider only files with .mp4 extension
try:
    newest_file = max(mp4_files, key = os.path.getctime)    #get the last file
except:
    print("No videos to upload.")  
    time.sleep(60)
    os.system("python upload_video.py")
    print("restarting the script...")  #if there aren't any files, the script restarts
    exit()

file_title = os.path.splitext(newest_file)[0]   #get the title of file

while newest_file != '': 

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

    #Upload last file 
    mediaFile = MediaFileUpload(newest_file)
    print('upload in progress...')

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    print("await the upload of the video...")
    time.sleep(5) #5 seconds delay
    #Remove the last file uploaded
    print("removing the last .mp4 file...")
    
    newest_file = 1 #Set the value of var in int
    os.close(newest_file)   #Close process
    newest_file = max(mp4_files, key = os.path.getctime)    #Get the last video uploaded
    os.remove(newest_file)  #Remove the last video
    print("last video removed")
