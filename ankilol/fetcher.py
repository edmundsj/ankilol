# TODO: this should be able to read both local files and files sourced from google drive.
from abc import ABC, abstractmethod
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.oauth2.service_account import Credentials
import io
from ankilol import base_dir
import configparser


class TransferManager(ABC):

    @abstractmethod
    def download_file(self, filename: str | Path):
        pass

    @abstractmethod
    def upload_file(self, filename: str | Path, file_id: str | Path):
        pass


class LocalTransferManager(TransferManager):
    def download_file(self, filename: str | Path):
        with open(self.filename, 'r') as file:
            return file.read()

    def upload_file(self, filename, file_id):
        with open(filename, 'r') as read_file:
            with open(file_id, 'w') as write_file:
                write_file.write(read_file.read())


class GoogleDriveTransferManager(TransferManager):
    SERVICE_ACCOUNT_FILE = base_dir / 'service_account.json'

    def _initialize_service(self):
        creds = Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE)
        drive_service = build('drive', 'v3', credentials=creds)
        return drive_service

    def download_file(self, file_id: str):
        drive_service = self._initialize_service()
        request = drive_service.files().export_media(fileId=file_id, mimeType='text/html')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        return fh.getvalue()

    def upload_file(self, filename: str | Path, file_id: str):
        drive_service = self._initialize_service()

        # Specify the file type as HTML and the conversion to Google Docs format
        media = MediaFileUpload(filename, mimetype='text/html')
        request = drive_service.files().update(fileId=file_id, media_body=media)

        # Execute the request
        updated_file = request.execute()

