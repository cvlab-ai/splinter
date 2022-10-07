import logging

from fastapi import FastAPI, Request

from src.routes import router

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.include_router(router)


@app.middleware('http')
def request_middleware(request: Request, call_next):
    logging.info(f'--- New request approach: {request.method} {request.json}')
    return call_next(request)
