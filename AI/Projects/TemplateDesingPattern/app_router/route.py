from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import os
from constants import app_constants
from service.userservice import UserService

router = APIRouter()
user_service = UserService()


class Query(BaseModel):
    question: str
    sessionId: str


class Content(BaseModel):
    url: str


@router.get("/hello")
async def hello_endpoint():
    return {"response": "Har Har Mahadev"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_location = app_constants.UPLOAD_DIRECTORY
    if not os.path.exists(upload_location):
        os.mkdir(upload_location)
    else:
        location = os.path.join(upload_location, file.filename)
        with open(location, "wb") as buffer:
            buffer.write(await file.read())
            await user_service.load_document_from_file(location, file.filename.split(".")[1])

    return {"response": app_constants.SUCCESS_MESSAGE}


@router.post("/url")
async def web_url(content: Content):
    try:
        await user_service.load_document_from_web(content.url)
        return {"response": "Content uploaded"}
    except RuntimeError as r:
        return {"response": f"Error while getting content from url {r}"}


@router.post("/ask")
async def user_query(query: Query):
    return user_service.invoke_user_request(query.question, query.sessionId)
