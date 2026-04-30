# app/db/init_db.py
from app.db.base import Base

# 👇 import ALL models so they register with Base.metadata
from app.models.request_log import RequestLog  # add others here if any