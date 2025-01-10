from server_api import API
import os
import json
import chardet
from fastapi import FastAPI, UploadFile, Form, File as FastFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
a = API()
os.makedirs(r"./assets", exist_ok=True)
app.mount("/assets", StaticFiles(directory=r"./assets"), "ui")


@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse(r"./index.html")


@app.get("/favicon.ico")
def favicon():
    return FileResponse(r"./favicon.ico")


@app.post("/api/login")
def api_login(account: str = Form(...), token: str = Form(...)):
    return a.api_login(account, token)


@app.post("/api/login_byid")
def api_login_byid(userid: str = Form(...), token: str = Form(...)):
    return a.api_login_byid(userid, token)


@app.get("/api/get_user")
def api_getuser_byid(userid: str):
    return a.api_getuser_byid(userid)


@app.post("/api/check_user")
def check_user(userid: str = Form(...), token: str = Form(...)):
    user=a.api_login_byid(userid, token)
    return {"isuser": user["id"] == userid,"username":user["username"] }


@app.get("/api/has_account")
def api_has_account(account: str):
    return a.api_has_account(account)


@app.post("/api/signup")
def api_signup(account: str = Form(...), token: str = Form(...)):
    return a.api_signup(account, token)


@app.post("/api/upload_file")
async def api_upload_file(knowledgeid: str, file: UploadFile = FastFile(...)):
    content = await file.read()
    detected_encoding = chardet.detect(content)["encoding"]
    return a.api_upload_file(knowledgeid, content.decode(detected_encoding))


@app.get("/api/add_knowledges")
def get_api_addknowledges(userid: str, knowledgename: str, ispublic: bool):
    return a.get_api_addknowledges(userid, knowledgename, ispublic)


@app.get("/api/knowledges")
def get_api_knowledges(userid: str, containspublic: bool):
    return a.get_api_knowledges(userid, containspublic)


@app.get("/api/publish_knowledge")
def get_publish_knowledge(knowledgeid: str):
    return a.get_publish_knowledge(knowledgeid)


@app.post("/api/updateknowledge")
def post_api_updateknowledge(knowledgeid: str, knowledge: str = Form(...)):
    return a.post_api_updateknowledge(knowledgeid, json.loads(knowledge))


@app.get("/api/qas")
def get_api_qas(knowledgeid: str, start: int = 0, count: int = 30):
    data = a.get_api_qas(knowledgeid)
    return data[start : start + count]


@app.post("/api/qa")
def post_api_qa(knowledgeid: str, method: str, qas: str = Form(...)):
    return a.post_api_qa(knowledgeid, method, qas)


@app.get("/api/sessions")
def api_sessions(userid: str):
    return a.api_sessions(userid)


@app.get("/api/add_session")
def api_add_sessions(userid: str, knowledgeid: str):
    return a.api_add_sessions(userid, knowledgeid)


@app.get("/api/del_session")
def api_del_sessions(sessionid: str):
    return a.disable_session(sessionid)


@app.get("/api/history")
def api_history(sessionid: str):
    return a.api_history(sessionid)


@app.post("/api/chat")
async def api_chat(sessionid: str, history: str = Form(...), question: str = Form(...)):
    return a.api_chat(sessionid=sessionid, history=history, question=question)


@app.exception_handler(404)
async def redirect_404(request, exec):
    return RedirectResponse("/")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1234)
