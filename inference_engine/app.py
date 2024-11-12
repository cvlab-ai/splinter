import logging

from fastapi import FastAPI, Request

from src.routes import router

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.include_router(router)


@app.middleware('http')
async def request_middleware(request: Request, call_next):
    # Read the request body as bytes
    body_bytes = await request.body()

    # Decode the bytes to a string for logging
    body_str = body_bytes.decode('utf-8')
    logging.info(f'--- New request approach: {request.method} {body_str}')

    # Create a new stream for the request body to make it available downstream
    async def receive():
        return {'type': 'http.request', 'body': body_bytes}

    # Replace the request's receive method with the new one
    request._receive = receive

    # Proceed with the request
    response = await call_next(request)
    return response
