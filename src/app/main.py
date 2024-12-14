from fastapi import FastAPI
from app.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(router)