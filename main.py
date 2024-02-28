from fastapi import FastAPI
from utils.youtube2 import auth_user
from utils.youtube import youtube_authenticate

app = FastAPI()

@app.get("/")
def read_root():
    return {"response":youtube_authenticate()}
    