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

class DispUser(BaseModel):
    name: str
    attendance: str
    invitation_side: str
    relationship: str
    namekana: str
    gender: str
    address: str
    mail: str
    allergy: str
    message: str
    datetime: str