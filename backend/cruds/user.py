from sqlalchemy.orm import Session
from models import user as userModels
from schemas import user as userSchemas

"""ユーザ情報"""

# ユーザ情報取得（条件:id)
def get_user(db: Session, user_id: int):
    db_user = db.query(account.User).filter(account.User.id == user_id, 
                                            account.User.is_deleted == '0').first()
    return db_user

# 複数ユーザ情報取得（条件:デフォルト100件取得）
def get_users(db: Session, skip: int = 0, limit: int = 100):
    db_user = db.query(account.User).fileter(account.User.is_deleted == '0').offset(skip).limit(limit).all()
    return db_user

# ユーザ情報作成
def create_user(db: Session, user: userSchemas.User):
    db_user = userModels.User(
        last_name = user.last_name,
        first_name = user.first_name,
        last_name_kana = user.last_name_kana,
        first_name_kana = user.first_name_kana,
        gender = user.gender,
        zip_code = user.zip_code,
        address = user.address,
        email = user.email,
        allergy = user.allergy,
        message = user.message,
        invitation_side = user.invitation_side,
        attendance = user.attendance,
        relationship = user.relationship
    )
    db.add(db_user)
    db.flush()
    return db_user

# メール確認完了の更新
def update_email_check(db: Session, user_id):
    db_user = db.query(account.User).filter(account.User.id == user_id).first()
    db_user.email_check = "1"
    db.flush()

# パスワード更新
def update_password(db: Session, user_id, new_password):
    db_user = db.query(account.User).filter(account.User.id == user_id).first()
    db_user.password = new_password
    db.flush()

"""トークン情報"""

# トークン情報取得（条件:user_id, token）
def get_user_token_by_user_id_and_token(db: Session, user_id, token):
    db_token = db.query(account.UserToken)\
                .filter(account.UserToken.user_id == user_id, 
                        account.UserToken.user_token == token)
    return db_token

# トークン情報作成
def create_user_token(db: Session, user_id, user_token, expiration):
    # 既に登録されている場合は更新、登録されていない場合は登録
    db_user_token = db.query(account.UserToken).filter(account.UserToken.user_id == user_id).first()
    if db_user_token:
        # 既に登録されている場合
        db_user_token.user_token = user_token
        db_user_token.token_expiration = expiration
    else:
        # 登録されていない場合
        db_user_token = account.UserToken(
                            user_id=user_id, 
                            user_token=user_token, 
                            token_expiration=expiration)
        db.add(db_user_token)
    db.flush()
    return db_user_token

"""ユーザ情報&トークン情報"""

def get_user_and_token(db: Session, user_id, token):
    db_user_token = db.query(account.User, account.UserToken.user_token, account.UserToken.token_expiration)\
                    .join(account.UserToken, account.UserToken.user_id == account.User.id)\
                    .filter(account.User.id == user_id).first()
    return db_user_token

""" Email確認 """

# Email確認URLを取得
def get_confirm_url(db: Session, confirm_url):
    db_url = db.query(account.EmailConfirm).filter(account.EmailConfirm.confirm_url == confirm_url).first()
    return db_url

# Email確認URLを削除
def delete_confirm_url(db: Session, confirm_url):
    db.query(account.EmailConfirm).filter(account.EmailConfirm.confirm_url == confirm_url).delete()

# Email確認URLを登録・更新
def insert_update_confirm_url(db: Session, user_id, confirm_url, expiration):
    db_url = db.query(account.EmailConfirm).filter(account.EmailConfirm.user_id == user_id).first()
    if db_url:
        # 既にデータが存在する場合
        db_url.confirm_url = confirm_url
        db_url.url_expiration = expiration
    else:
        # データがない場合
        db_url = account.EmailConfirm()
        db_url.user_id = user_id
        db_url.confirm_url = confirm_url
        db_url.url_expiration = expiration
        db.add(db_url)
    db.flush()

""" パスワード変更 """

# パスワード変更情報を登録
def insert_update_change_password(db: Session, user_id, password, confirm_url, expiration):
    db_url = db.query(account.ChangePassword).filter(account.ChangePassword.user_id == user_id).first()
    if db_url:
        # 既にデータが存在する場合
        db_url.password = password
        db_url.confirm_url = confirm_url
        db_url.url_expiration = expiration
    else:
        # データがない場合
        db_url = account.ChangePassword()
        db_url.user_id = user_id
        db_url.password = password
        db_url.confirm_url = confirm_url
        db_url.url_expiration = expiration
        db.add(db_url)
    db.flush()
    return db_url

# パスワード変更情報を取得
def get_change_password(db: Session, confirm_url):
    db_change_password = db.query(account.ChangePassword)\
                                .filter(account.ChangePassword.confirm_url == confirm_url).first()
    return db_change_password

# パスワード変更情報を削除
def delete_change_password(db: Session, confirm_url):
    db.query(account.ChangePassword)\
            .filter(account.ChangePassword.confirm_url == confirm_url).delete()
    db.flush()

# 管理者チェック
def check_manager(db: Session, user_id: int):

    user = db.query(
                account.User
            ).filter(
                account.User.id == user_id,
                account.User.is_deleted == '0'
            ).order_by(
                account.User.id.desc()
            )

    user = user.first()

    return user