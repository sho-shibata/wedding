import json
from datetime import datetime, date, time
from zoneinfo import ZoneInfo
import webbrowser
import hashlib
import traceback
from dotenv import load_dotenv
import os

from service.mail import MailService
from cruds import user as userCrud
from log import logger

# 本登録済
EMAIL_CHECKED = '1'
# 未本登録
EMAIL_NOT_CHECKED = '2'

# ログインサービスクラス
class UserService:

    # メールサービス
    mailService = MailService()
    # 環境ファイルの読み込み
    load_dotenv('setting/.env')

    # 送信ボタン押下時
    def submitInvitation(self, db, inputData):
        result = {}
        messages = []
        # エラーチェック
        messages = self.invitationCheck(inputData)
        if len(messages) > 0:
            # エラーが存在する場合
            result['result'] = 'error'
            result['data'] = {'messages': messages}
            return result
        # 登録処理
        regData = userCrud.create_user(db, inputData)
        # 次画面用データ
        if regData:
            # 登録したデータが存在する場合
            result['result'] = 'success'
            # メール送信
            self.sendMail(regData)
            return result
        return result

    # 入力チェック
    def invitationCheck(self, inputData):
        messages = []
        # 必須チェック
        messages.extend(self.inputExistCheck(inputData))
        # 文字数チェック
        messages.extend(self.inputCountCheck(inputData))
        return messages
    
    # 入力チェック
    def inputExistCheck(self, inputData):
        messages = []
        # 出席可否
        if self.isNoneOrEmpty(inputData.attendance):
            messages.append('出席可否を選択してください')
        # 招待側
        if self.isNoneOrEmpty(inputData.invitation_side):
            pass
        # 関係
        if self.isNoneOrEmpty(inputData.relationship):
            messages.append('ご関係を選択してください')
        # 姓
        if self.isNoneOrEmpty(inputData.last_name):
            messages.append('お名前の姓を入力してください')
        # 名
        if self.isNoneOrEmpty(inputData.first_name):
            messages.append('お名前の名を入力してください')
        # 姓カナ
        if self.isNoneOrEmpty(inputData.last_name_kana):
            messages.append('お名前の姓カナを入力してください')
        # 名カナ
        if self.isNoneOrEmpty(inputData.first_name_kana):
            messages.append('お名前の名カナを入力してください')
        # 性別
        if self.isNoneOrEmpty(inputData.gender):
            messages.append('性別を選択してください')
        # 郵便番号
        if self.isNoneOrEmpty(inputData.zip_code):
            messages.append('郵便番号を入力してください')
        # 住所
        if self.isNoneOrEmpty(inputData.address):
            messages.append('住所を入力してください')
        # メールアドレス
        if self.isNoneOrEmpty(inputData.email):
            messages.append('メールアドレスを入力してください')
        # アレルギー
        if self.isNoneOrEmpty(inputData.allergy):
            pass
        # メッセージ
        if self.isNoneOrEmpty(inputData.message):
            pass
        
        return messages

    # 入力値の文字数チェック
    def inputCountCheck(self, inputData):
        messages = []
        # 姓
        if self.countCheck(inputData.last_name, 100):
            messages.append('お名前の名字は100文字以内です')
        # 名
        if self.countCheck(inputData.first_name, 100):
            messages.append('お名前の名前は100文字以内です')
        # 姓カナ
        if self.countCheck(inputData.last_name_kana, 100):
            messages.append('お名前の名字カナは100文字以内です')
        # 名カナ
        if self.countCheck(inputData.first_name_kana, 100):
            messages.append('お名前の名前カナは100文字以内です')
        # 性別
        if self.countCheck(inputData.gender, 1):
            pass
        # 郵便番号
        if self.countCheck(inputData.zip_code, 20):
            messages.append('郵便番号は20文字以内です')
        # 住所
        if self.countCheck(inputData.address, 100):
            messages.append('住所は100文字以内です')
        # メールアドレス
        if self.countCheck(inputData.email, 100):
            messages.append('メールアドレスは100文字以内です')
        # アレルギー
        if self.countCheck(inputData.allergy, 1000):
            messages.append('アレルギーは1000文字以内です')
        # メッセージ
        if self.countCheck(inputData.message, 10000):
            messages.append('メッセージは10000文字以内です')
        # 招待側
        if self.countCheck(inputData.invitation_side, 1):
            pass
        # 出席可否
        if self.countCheck(inputData.attendance, 1):
            pass
        # 関係
        if self.countCheck(inputData.relationship, 1):
            pass
        return messages

    # メール送信
    def sendMail(self, db_data):
        content = self.mailService.createEmailConfirmMail(db_data)
        self.mailService.sendMail(content)
        return True

    # 文字数チェック
    def countCheck(self, words, cnt):
        result = False
        if len(words) > cnt:
            result = True
        return result

    # Noneと空チェック
    def isNoneOrEmpty(self, word):
        if not word:
            return True
        return False

