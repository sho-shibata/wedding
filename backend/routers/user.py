from fastapi import APIRouter, Depends, HTTPException, Cookie, Request, Response
from typing import Union, Optional
from datetime import datetime, date, time
from zoneinfo import ZoneInfo
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import os

from schemas import user as userSchema
from sqlalchemy.orm import Session
from typing import List

from service.user import UserService
import database

from log import logger

router = APIRouter()

# ユーザサービス
userService = UserService()
# ロガー
log = logger.logger()

"""
参加情報提出API
"""
@router.post("/register")
def login(userSchema : userSchema.User, db: Session = Depends(database.get_db)):
    log.info('register start')
    returnSet = {}
    try:
        returnSet = userService.submitInvitation(db, userSchema)
    except Exception as e:
        db.rollback()
        log.exception(e)
    log.info('register end')
    return returnSet

    