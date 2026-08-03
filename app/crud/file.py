from sqlalchemy.orm import Session

from app.models.file import File


def create_File(db:Session, **kwargs): #kwargs make function reusable

    db_file = File(**kwargs)

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file

def get_user_files(db:Session, user_id:int):

    return db.query(File).filter(
        File.owner_id ==user_id
    ).all()


def get_file_by_id(db:Session, file_id:int):
    return db.query(File).filter(
        File.id ==file_id
    ).first()