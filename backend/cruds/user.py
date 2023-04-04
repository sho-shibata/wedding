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
def get_100_users(db: Session, skip: int = 0, limit: int = 100):
    db_user = db.query(account.User).fileter(account.User.is_deleted == '0').offset(skip).limit(limit).all()
    return db_user

# 全ユーザ情報取得
def get_users(db: Session):
    db_user = db.query(userModels.User).all()
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

