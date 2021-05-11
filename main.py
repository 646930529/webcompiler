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


from subprocess import PIPE, run

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout, result.stderr


app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Alarm(BaseModel):
    pc_id: str
    frame: str


@app.post('/alarm')
async def alarm(item: Alarm):
    t = str(time.time())
    print("pc_id", item.pc_id, "frame", item.frame)
    with open(f'student01/{t}', 'w', encoding='utf-8') as f:
        f.write(item.frame)
    stdout, stderr = out(f"python student01/{t}")
    return {"code": 0, "stdout": stdout, "stderr": stderr}


if __name__ == '__main__':
    port = None
    gpu = None
    pics_dic = {}
    try:
        port = sys.argv[1]
        gpu = sys.argv[2]
        print("port:", port)
        print("gpu:", gpu)
    except Exception:
        print("args port or gpu is None")
        port = 7001
        gpu = "0"
        if port is None or gpu is None:
            sys.exit()

    uvicorn.run(app, host='0.0.0.0', port=int(port))
