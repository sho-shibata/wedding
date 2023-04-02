from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from dotenv import load_dotenv
import os
import datetime

from log import logger

class MailService:
    # ロガー
    log = logger.logger()

    # 環境ファイルの読み込み
    load_dotenv('setting/.env')
    # ROOT
    ROOT_BACK = os.environ['ROOT']
    # ROOT_FRONT
    ROOT_FRONT = os.environ['ROOT_FRONT']
    # INFO_EMAIL
    INFO_EMAIL = os.environ['INFO_EMAIL']
    # INFO_PASS
    INFO_PASS = os.environ['INFO_PASS']
    # ベースとなる絶対パス取得
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    # メール本文のパス
    MAIL_BODY_PATH = '../setting/mail_text/'  

    # Email確認メール用メッセージ作成
    def createEmailConfirmMail(self, db_data):
        # messageを取得
        text = self.__createContents(db_data)
        # MIMETextを作成
        msg = MIMEText(text, "plain", "utf-8")
        msg['Subject'] = '挙式・披露宴の出欠について'
        msg['From'] = self.INFO_EMAIL
        msg['To'] = db_data.email
        msg['Date'] = formatdate()
        return msg

    # メッセージ送信
    def sendMail(self, msg):
        smtp_obj = SMTP('smtp.gmail.com', 587)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(self.INFO_EMAIL, self.INFO_PASS)
        smtp_obj.send_message(msg)
        smtp_obj.quit()

    # メール本文を取り込む（本文の内容作成）
    # mode（0: 本登録 1: 会員登録 2: パスワード変更　3: 出品完了 4: オファー完了）
    def __createContents(self, db_data):
        format_content = ''
        # 取り込む本文のファイル名を取得
        text_name = ''
        text_name = 'confirm_wedding_invitation.txt'
        # メール本文のパス設定
        body_path = os.path.normpath(os.path.join(self.BASE_PATH, self.MAIL_BODY_PATH, text_name))
        # 本文の内容取得
        with open(body_path, 'r', encoding='utf-8') as f:
            format_content = f.read()
        # 本文に必要な情報をセット
        if format_content:
            full_content = self.__createConfirmInvitationContents(format_content, db_data)
            
        return full_content

    # 招待状回答確認本文作成
    def __createConfirmInvitationContents(self, format_content, db_data):
        full_content = ''
        # 確認用URL
        invitation_url = self.ROOT_BACK + '/' + 'top'
        # 本文の内容をセット
        full_content = format_content.format(
                                name = f'{db_data.last_name} {db_data.first_name}',
                                attendance = '出席' if db_data.attendance == '1' else '欠席',
                                invitation_side = '新郎ゲスト' if db_data.invitation_side == '1' else '新婦ゲスト',
                                relationship = '友人' if db_data.relationship == '2' else '親族',
                                namekana = f'{db_data.last_name_kana} {db_data.first_name_kana}',
                                gender = '男性' if db_data.gender == '1' else '女性' if db_data.gender == '2' else 'その他',
                                address = f'〒{db_data.zip_code} {db_data.address}',
                                mail = db_data.email,
                                allergy = db_data.allergy,
                                message = db_data.message,
                                invitation_url = invitation_url,
                                datetime = db_data.created_at.strftime("%Y/%m/%d %H:%M:%S")
                            )
        return full_content
