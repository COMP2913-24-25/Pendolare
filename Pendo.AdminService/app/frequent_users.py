from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import status
from models import Journey
from typing import List, Dict

class FrequentUsersCommand:
    def __init__(self, db_session: Session, response):
        self.db_session = db_session
        self.response = response

    def execute(self):