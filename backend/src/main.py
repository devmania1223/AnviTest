import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps import auth_app, dashboard_app
from utils import constants

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(    
    CORSMiddleware,
    allow_origins=origins,    
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def on_startup():
    with open(constants.SCHEMA_FILE, 'r') as fp:
        conn = sqlite3.connect(constants.DB_FILE)
        conn.executescript(fp.read())
    conn.close()


app.mount('/auth', auth_app.app)
app.mount('/dashboard', dashboard_app.app)
