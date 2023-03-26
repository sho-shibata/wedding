from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

# ユーザスキーマ
class User(BaseModel):
    last_name: str
    first_name: str
    last_name_kana: str
    first_name_kana: str
    gender: str
    zip_code: str
    address: str
    email: str
    allergy: str
    message: str
    invitation_side: str
    attendance: str
    relationship: str
    # class Config:
    #     orm_mode = True
