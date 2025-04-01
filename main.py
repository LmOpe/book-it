import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Book It", version="1.0.0")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Music Booking API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7001, reload=True)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("uvicorn.error")
    logger.info("Starting server...")
    logger.info("Server started successfully.")
