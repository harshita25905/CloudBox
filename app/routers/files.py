import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File
from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.crud.file import create_File, get_user_files, get_file_by_id
from app.schemas.file import FileResponse

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):

    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    db_file = create_File(
    db,

    filename=file.filename,

    stored_filename=unique_filename,

    file_path=file_path,

    file_size=file_size,

    content_type=file.content_type,

    owner_id=current_user.id
)
    return db_file


@router.get(
    "/",
    response_model=list[FileResponse]
)
def get_files(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    files = get_user_files(
        db,
        current_user.id
    )

    return files


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_file=get_file_by_id(db,file_id)

    if db_file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    if db_file.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorised to access this file"
        )

    return FastAPIFileResponse(
        path= db_file.file_path,
        filename=db_file.filename
    )