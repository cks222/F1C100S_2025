from server_api import API
import os
import json
import chardet
from fastapi import FastAPI,UploadFile,Form,File as FastFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,HTMLResponse,RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

origins =[
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
a=API()
os.makedirs(r"./assets",exist_ok=True)
app.mount("/assets",StaticFiles(directory=r"./assets"),"ui")
@app.get('/',response_class=HTMLResponse)
def home():
    return FileResponse(r'./index.html')

@app.post('/api/login')
def api_login(username:str=Form(...),token:str=Form(...)):
    return a.api_login(username,token)

@app.get('/api/hasuser')
def api_hasuser(username:str):
    return  a.api_hasuser(username)

@app.post('/api/signup')
def api_signup(username:str=Form(...),token:str=Form(...)):
    return  a.api_signup(username,token)

@app.post("/api/upload_file")
async def api_upload_file(knowledgeid:str,file: UploadFile = FastFile(...)):
    content = await file.read() 
    detected_encoding = chardet.detect(content)['encoding']
    return a.api_upload_file(knowledgeid,content.decode(detected_encoding) )

@app.get('/api/add_knowledges')
def get_api_addknowledges(username:str,knowledgename:str,ispublic:bool): 
    return a.get_api_addknowledges(username,knowledgename,ispublic)

@app.get('/api/knowledges')
def get_api_knowledges(username:str,containspublic:bool):
    return a.get_api_knowledges(username,containspublic)

@app.get('/api/publish_knowledge')
def get_publish_knowledge(knowledgeid:str):
    return a.get_publish_knowledge(knowledgeid)

@app.post('/api/updateknowledge')
def post_api_updateknowledge(knowledgeid:str,knowledge:str=Form(...)):
    return a.post_api_updateknowledge(knowledgeid,json.loads(knowledge))

@app.get('/api/qas')
def get_api_qas(knowledgeid:str,start:int=0,count:int=30):
    data = a.get_api_qas(knowledgeid)
    return data[start:start+count]

@app.post('/api/qa')
def post_api_qa(knowledgeid:str,method:str,qas:str=Form(...)):
    return a.post_api_qa(knowledgeid,method,qas)

@app.get('/api/sessions')
def api_sessions(username:str):
    return a.api_sessions(username)

@app.get('/api/add_session')
def api_add_sessions(username:str,knowledgeid:str):
    return a.api_add_sessions(username,knowledgeid)

@app.get('/api/history')
def api_history(sessionid:str):
    return a.api_history(sessionid)

@app.post('/api/chat')
async def api_chat(sessionid:str,history:str=Form(...),question:str=Form(...)):
   return a.api_chat(sessionid=sessionid,history=history,question=question)

@app.exception_handler(404)
async def redirect_404(request,exec):
    return RedirectResponse("/")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=1234)
