from pydrive.auth import GoogleAuth,ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, UploadFile
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload


app = FastAPI()

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
     "http://localhost",
     "http://localhost:3000",
     "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_file(file: UploadFile):
    file_path = os.path.join(r"C:\Users\Administrator\Desktop\fastapi fileuploadgoogle drive", file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

#     WITH PYDRIVE LIBRARY

#     gauth = GoogleAuth()  
#     drive = GoogleDrive(gauth)  
#     upload_file = file.filename
#     gfile = drive.CreateFile({'title':file.filename})
#     # gfile = drive.CreateFile({'parents': [{'id': '1AGLFX0gOdejhqy-8vBBQ8zOLaKJkrgoa'}]})
#     # Read file and set it as the content of this instance.
#     gfile.SetContentFile(upload_file)

#     gfile.Upload() # Upload the file.
#     gauth.flow.redirect_uri = 'http://localhost:3000'
#     return {"filename": file.filename}


#   METHOD 2
    # Set up the OAuth 2.0 flow
    SCOPES = ['https://www.googleapis.com/auth/drive']
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)

    # Start the OAuth 2.0 authorization flow
    credentials = flow.run_local_server()

    # Build the Google Drive service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Upload a file to Google Drive
    file_metadata = {'name':file.filename}
    media = MediaFileUpload(file_path)
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media).execute()

    # Print the file ID of the uploaded file
    print('File ID:', uploaded_file)
    return {"filename": file.filename}

