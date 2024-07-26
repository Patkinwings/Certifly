import os
import requests
from django.core.files.storage import Storage
from django.conf import settings
import magic
import mimetypes

class VercelBlobStorage(Storage):
    def __init__(self):
        self.base_url = "https://blob.vercel-storage.com"
        self.token = settings.BLOB_READ_WRITE_TOKEN

    def _open(self, name, mode='rb'):
        url = f"{self.base_url}/{name}"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.token}"})
        response.raise_for_status()
        return response.content

    def _save(self, name, content):
        url = f"{self.base_url}/{name}"

        # Read the first 1024 bytes for magic number detection
        content_start = content.read(1024)
        content.seek(0)  # Reset file pointer to the beginning

        # Try to determine content type using python-magic
        mime = magic.Magic(mime=True)
        content_type = mime.from_buffer(content_start)

        # If content type is not determined or is generic, try mimetypes
        if not content_type or content_type == 'application/octet-stream':
            content_type = mimetypes.guess_type(name)[0] or 'application/octet-stream'

        response = requests.put(
            url,
            data=content,
            headers={
                "Content-Type": content_type,
                "Authorization": f"Bearer {self.token}"
            }
        )
        response.raise_for_status()
        return name

    def delete(self, name):
        url = f"{self.base_url}/{name}"
        response = requests.delete(url, headers={"Authorization": f"Bearer {self.token}"})
        response.raise_for_status()

    def exists(self, name):
        url = f"{self.base_url}/{name}"
        response = requests.head(url, headers={"Authorization": f"Bearer {self.token}"})
        return response.status_code == 200

    def url(self, name):
        return f"{self.base_url}/{name}?token={self.token}"

    def size(self, name):
        url = f"{self.base_url}/{name}"
        response = requests.head(url, headers={"Authorization": f"Bearer {self.token}"})
        response.raise_for_status()
        return int(response.headers.get('Content-Length', 0))

    def get_accessed_time(self, name):
        return None

    def get_created_time(self, name):
        return None

    def get_modified_time(self, name):
        return None