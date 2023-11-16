from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import jwt
from app.dbVideo import saveToPostgres
from pydantic import BaseModel
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()
jwt_key = os.getenv("JWT_KEY")

class Video(BaseModel):
    title: str
    desc: str

class UserData(BaseModel):
   token: str
   video: Video

def my_schema():
   openapi_schema = get_openapi(
       title="video converter",
       version="1.0",
       description="microservice for converting user videos to .webm",
       routes=app.routes,
   )
   app.openapi_schema = openapi_schema
   return app.openapi_schema

app.openapi = my_schema

def checkToken(token):
    try:
        jwt.decode(token, jwt_key, algorithms=['HS256'])
    except Exception as e:
        print(e)
        return False
    return True

@app.post("/api/video/load")
def loadVideo(data:UserData):
    """
    This endpoint returns status of user video loading.
    """
    if not checkToken(data.token):
        return JSONResponse(content={"message": "Пользовательские данные не совпадают"}, status_code=403)
    saveResponse = saveToPostgres(data.video)
    if saveResponse[0] == False:
        return JSONResponse(content={"message": saveResponse[1]}, status_code=500)
    return JSONResponse(content={"message": "Видео загружено"}, status_code=201)

@app.get("/docs")
def read_docs():
    """
    Swagger page
    """
    return get_swagger_ui_html(openapi_url="/openapi.json")
