import os
# import shutil (for local storage)
import uuid

from fastapi import APIRouter, UploadFile, File
from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.crud.file import create_File, get_user_files, get_file_by_id, delete_file_record
from app.schemas.file import FileResponse
from app.services.s3 import upload_file as upload_to_s3, generate_download_url, delete_from_s3
from app.core.constants import MAX_FILE_SIZE, ALLOWED_FILE_TYPES
from app.core.logger import logger

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

# UPLOAD_DIR = "uploads"

# os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload",
    summary="Upload a file",
    description="Uploads a file to AWS S3 and stores its metadata in PostgreSQL.",
    response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):

    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    # file_path = os.path.join(
    #     UPLOAD_DIR,
    #     unique_filename
    # )

    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    file.file.seek(0, 2)      # Move to end
    file_size = file.file.tell()
    file.file.seek(0)         # Move back to beginning

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 10 MB."
        )

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="File type is not allowed."
        )
    

    try:
        upload_to_s3(
            file.file,
            unique_filename
        )
        logger.info(
            f"User {current_user.email} uploaded {file.filename}"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to upload file to cloud storage."
        )


    # file_size = os.path.getsize(file_path)

    db_file = create_File(
    db,

    filename=file.filename,

    stored_filename=unique_filename,

    file_path=unique_filename,

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

    # return FastAPIFileResponse(
    #     path= db_file.file_path,
    #     filename=db_file.filename
    # )

    download_url = generate_download_url(
        db_file.file_path
    )

    logger.info(
        f"User {current_user.email} download {db_file.filename}"
    )

    return {
        "download_url":download_url
    }

@router.delete("/{file_id}/delete")
def delete_uploaded_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_file = get_file_by_id(db,file_id)

    if db_file is None:
        raise HTTPException(
                    status_code=404,
                    detail="File not found"
                )

    if db_file.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not authorised to delete this file"
            )

    # if os.path.exists(db_file.file_path):
    #     os.remove(db_file.file_path)

    delete_from_s3(
         db_file.file_path
    )

    logger.info(
        f"User {current_user.email} deleted {db_file.filename}"
    )

    delete_file_record(db, db_file)

    return{
        "message":"File deleted successfully"
    }