from pydantic import BaseModel, ConfigDict

class FileResponse(BaseModel):
    id:int
    filename: str
    stored_filename:str
    file_size: int
    content_type: str

    model_config = ConfigDict(from_attributes=True)