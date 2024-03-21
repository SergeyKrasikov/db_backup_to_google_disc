from datetime import datetime, timedelta
import os
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import shutil


SERVICE_ACCOUNT_FILE =  #service account key file
DB_PATH = 
GOOGLE_FOLDER = 
NAME = 


def _creater_connection(service_account_file: str) -> object:
    credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=['https://www.googleapis.com/auth/drive'])
    return build('drive', 'v3', credentials=credentials)


def _lowder_to_google_drive(service: object, google_folder_id: str, file_name: str) -> None:
    name = file_name + '.zip'
    file_metadata = {
                'name': name,
                'parents': [google_folder_id]
            }
    media = MediaFileUpload(name, resumable=True)
    service.files().create(body=file_metadata, media_body=media).execute()


def _old_backups_remover(service: object) -> None:
    results = service.files().list(
        pageSize=10, 
        fields="nextPageToken, files(id)",
        q=f"createdTime < '{datetime.now().date() - timedelta(weeks=1)}' and name contains 'backup_base'").execute()
    for i in results['files']:
        service.files().delete(fileId=i.get('id')).execute()    


def creator_backups(name: str, path: str, service_account_file: str, google_folder: str) -> None:
    shutil.make_archive(name, 'zip', path)
    service = _creater_connection(service_account_file)
    _lowder_to_google_drive(service, google_folder, name)
    os.remove(name + '.zip')
    _old_backups_remover(service)

if __name__ == "__main__":
    creator_backups(NAME, DB_PATH, SERVICE_ACCOUNT_FILE, GOOGLE_FOLDER) 


