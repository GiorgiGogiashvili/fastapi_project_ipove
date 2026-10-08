import os


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-secret-key-change-later",
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60