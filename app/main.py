from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.user import User
from app.routers import auth, files, users

#Base.metadata.create_all(bind=engine) #Look at every class that inherits
#from Base,and if its table doesn't exist, create it

app = FastAPI(
    title="CloudBox API",
    description="Secure File Sharing Platform built with FastAPI & AWS",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {
        "message":"Welcome to CloudBox"
    }