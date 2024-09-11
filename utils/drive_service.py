from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import mimetypes
from googleapiclient.http import MediaIoBaseUpload
from requests import HTTPError
from googleapiclient.errors import HttpError
import socket
import os
import sys
import io
import re

from  PIL import Image
import pillow_heif

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.config import Config
from utils.functions import get_abspath_relative_root, get_file_extension

pillow_heif.register_heif_opener()
pillow_heif.register_avif_opener()

class DriveService:
    def __init__(self, config: Config) -> None:
        self.cv_folder_id = config.get("RESUME_FOLDER_ID")
        self.photo_folder_id = config.get("PHOTO_FOLDER_ID")
        self.creds = self._get_credentials()
        self.service = self._get_service()

    def _get_credentials(self) -> Credentials:
        scopes = ["https://www.googleapis.com/auth/drive"]
        file = get_abspath_relative_root("credentials.json")
        return Credentials.from_service_account_file(file, scopes=scopes)
    
    def _get_service(self):
        self.available = True
        if not self._check_internet_connection():
            self.available = False
            return None
        try:
            return build('drive', 'v3', credentials=self.creds, static_discovery=False)
        except HTTPError as _:
            self.available = False

    def _check_internet_connection(self) -> bool:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            return False

    def restart_service(self) -> bool:
        if not self.available:
            self.service = self._get_service()
        return self.available

    def import_file(self, input_file_url, output_file_name, folder_id, overwrite = False) -> str:
        if input_file_url.strip() == "":
            return ""

        # Extraer el ID del archivo de la URL
        file_id = input_file_url.split('/')[-2]
        
        # Verificar la extensión del archivo mediante los metadatos sin descargarlo
        file_info = self.service.files().get(fileId=file_id, fields='mimeType, name').execute()
        file_name = file_info.get('name')
        mime_type = file_info.get('mimeType')

        query = f"'{folder_id}' in parents and name='{output_file_name}'"
        existing_files = self.service.files().list(q=query, fields='files(id)').execute().get('files', [])
        
        # Si ya existe un archivo con el mismo nombre, no hacer nada
        if existing_files and not overwrite:
            copied_file_id = existing_files[0]['id']
            copied_file_url = f'https://drive.google.com/file/d/{copied_file_id}/view'
            print(f'Archivo ya existe. URL del archivo: {copied_file_url}')
            return copied_file_url
        elif existing_files and overwrite:
            copied_file_id = existing_files[0]['id']
            self.service.files().delete(fileId=copied_file_id).execute()
            print(f"Eliminando archivo existente...")
        
        # Si es una imagen y no es JPG, procesar la conversión
        if mime_type.startswith('image/') and not file_name.lower().endswith('.jpg'):
            print("Convirtiendo imagen...")
            # Descargar el archivo
            request = self.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO(request.execute())

            # Convertir la imagen a JPG
            image = Image.open(file_content)
            converted_image_io = io.BytesIO()
            image.convert('RGB').save(converted_image_io, format='JPEG')
            converted_image_io.seek(0)

            # Subir la imagen convertida a la carpeta de destino
            media = MediaIoBaseUpload(converted_image_io, mimetype='image/jpeg', resumable=True)
            file_metadata = {
                'name': output_file_name,
                'parents': [folder_id]
            }
            copied_file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        else:
            # Definir los metadatos para la copia
            file_metadata = {
                'name': output_file_name,
                'parents': [folder_id]  # Carpeta destino
            }
            # Crear una copia del archivo
            copied_file = self.service.files().copy(fileId=file_id, body=file_metadata).execute()

        # Construir la URL del archivo copiado
        copied_file_id = copied_file.get('id')
        copied_file_url = f'https://drive.google.com/file/d/{copied_file_id}/view'
        
        return copied_file_url

    def import_local_file(self, input_file_path, output_file_name, folder_id, overwrite=False) -> str:
        if not os.path.exists(input_file_path):
            print("El archivo no existe.")
            return ""

        # Obtener el mime_type y nombre del archivo
        mime_type = mimetypes.guess_type(input_file_path)[0]
        file_name = os.path.basename(input_file_path)

        # Verificar si ya existe un archivo con el mismo nombre en la carpeta de Google Drive
        query = f"'{folder_id}' in parents and name='{output_file_name}'"
        existing_files = self.service.files().list(q=query, fields='files(id)').execute().get('files', [])

        # Si ya existe un archivo con el mismo nombre y no se debe sobrescribir, retornar la URL
        if existing_files and not overwrite:
            copied_file_id = existing_files[0]['id']
            copied_file_url = f'https://drive.google.com/file/d/{copied_file_id}/view'
            print(f'Archivo ya existe. URL del archivo: {copied_file_url}')
            return copied_file_url
        elif existing_files and overwrite:
            copied_file_id = existing_files[0]['id']
            self.service.files().delete(fileId=copied_file_id).execute()
            print(f"Eliminando archivo existente...")

        # Si es una imagen y no es JPG, procesar la conversión
        if mime_type and mime_type.startswith('image/') and not file_name.lower().endswith('.jpg'):
            print("Convirtiendo imagen a JPG...")
            # Abrir la imagen y convertirla
            with open(input_file_path, 'rb') as f:
                image = Image.open(f)
                converted_image_io = io.BytesIO()
                image.convert('RGB').save(converted_image_io, format='JPEG')
                converted_image_io.seek(0)

                # Subir la imagen convertida a Google Drive
                media = MediaIoBaseUpload(converted_image_io, mimetype='image/jpeg', resumable=True)
                file_metadata = {
                    'name': output_file_name,
                    'parents': [folder_id]
                }
                copied_file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        else:
            # Si no requiere conversión, subir el archivo directamente
            with open(input_file_path, 'rb') as f:
                media = MediaIoBaseUpload(f, mimetype=mime_type, resumable=True)
                file_metadata = {
                    'name': output_file_name,
                    'parents': [folder_id]
                }
                copied_file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Construir la URL del archivo copiado
        copied_file_id = copied_file.get('id')
        copied_file_url = f'https://drive.google.com/file/d/{copied_file_id}/view'

        return copied_file_url

    def get_file_extension(self, file_url):
        """Extrae la extensión del archivo dado su URL en Google Drive."""
        try:
            if file_url.strip() == "":
                return ""
            # Extraer el ID del archivo de la URL
            file_id = file_url.split('/')[-2]
            file_metadata = self.service.files().get(fileId=file_id, fields='name, mimeType').execute()
            file_name = file_metadata.get('name', '')
            mime_type = file_metadata.get('mimeType', '')
            mime_types = {
                'application/pdf': '.pdf',
                'image/jpeg': '.jpg',
                'image/png': '.png',
                'application/msword': '.doc',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            }
            file_extension = mime_types.get(mime_type, '')
            if not file_extension:
                file_extension = file_name.split('.')[-1] if '.' in file_name else ''
                file_extension = get_file_extension(file_name)
            return file_extension
        except HttpError as error:
            print(f'Error al obtener la extensión del archivo: {error}')
            return None
    
    def import_resume(self, input_file_url, output_file_name, overwrite = False) -> str:
        return self.import_file(input_file_url, output_file_name, self.cv_folder_id, overwrite)
    
    def import_photo(self, input_file_url, output_file_name, overwrite = False) -> str:
        return self.import_file(input_file_url, output_file_name, self.photo_folder_id, overwrite)
    
    def import_local_resume(self, input_file_path, output_file_name, overwrite = False) -> str:
        return self.import_local_file(input_file_path, output_file_name, self.cv_folder_id, overwrite)
    
    def import_local_photo(self, input_file_path, output_file_name, overwrite = False) -> str:
        return self.import_local_file(input_file_path, output_file_name, self.photo_folder_id, overwrite)

    def delete_file(self, file_url: str) -> bool:
        file_id = self._extract_file_id(file_url)
        if not file_id:
            print(f"No se pudo extraer el ID del archivo de la URL: {file_url}")
            return False
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"Archivo con ID {file_id} eliminado exitosamente.")
            return True
        except HttpError as error:
            print(f"Error al intentar eliminar el archivo: {error}")
            return False

    def _extract_file_id(self, file_url: str) -> str:
        # Usa una expresión regular para extraer el ID del archivo de la URL
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', file_url)
        if match:
            return match.group(1)
        return None
