import uuid, os
from fastapi import UploadFile
from fastapi.responses import FileResponse

STATIC_DIR = os.path.join(os.getcwd(), "static")

def save_upload(file: UploadFile) -> str:
    """
    Сохраняет файл в static/ и возвращает относительный путь (/static/filename.ext)
    """
    ext = os.path.splitext(file.filename)[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(STATIC_DIR, fname)

    with open(dest_path, "wb") as f:
        f.write(file.file.read())

    return f"/static/{fname}"

def get_file_response(path: str) -> FileResponse:
    """Отдать файл браузеру (если нужно)"""
    abs_path = os.path.join(STATIC_DIR, os.path.basename(path))
    return FileResponse(abs_path)
