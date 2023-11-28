import os

from dotenv import load_dotenv
import uvicorn

if os.path.isfile(".env"):
    print("Loading env file...")
    load_dotenv(".env")

DEBUG = os.environ.get("DEBUG", "false") == "true"

if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", reload=DEBUG, port=8000)
