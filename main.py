from starlette.responses import StreamingResponse
from typing import List
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
import requests
import json
from fastapi.middleware.cors import CORSMiddleware
import multiprocessing
import time
import os


from subprocess import PIPE, run

def cmd(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout, result.stderr


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Runs(BaseModel):
    student_id: str
    file_name: str
    code_src: str


@app.post('/runs')
async def runs(item: Runs):
    print("student_id", item.student_id, "file_name", item.file_name, "code_src", item.code_src)
    if not os.path.exists(f'{item.student_id}/'):
        os.mkdir(f'{item.student_id}/')
    with open(f'{item.student_id}/{item.file_name}', 'w', encoding='utf-8') as f:
        f.write(item.code_src)
    stdout, stderr = cmd(f"python {item.student_id}/{item.file_name}")
    return {"code": 0, "stdout": stdout, "stderr": stderr}


if __name__ == '__main__':
    port = None
    gpu = None
    pics_dic = {}
    try:
        port = sys.argv[1]
        print("port:", port)
    except Exception:
        print("use default port 7001")
        port = 7001

    uvicorn.run(app, host='0.0.0.0', port=int(port))
