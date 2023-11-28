import os

ALLOWED_ORIGINS = os.environ.get(
    "BACKEND_ALLOWED_ORIGINS", "http://localhost:3000"
).split(",")

ALLOW_ALL_ORIGINS = os.environ.get(
    "BACKEND_ALLOW_ALL_ORIGINS", "false"
) == "true"
