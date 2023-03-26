from .Base import BaseModel
import sqlalchemy as sa

class User(BaseModel):
    __tablename__ = "m_user"
    last_name = sa.Column('last_name', sa.String(100), nullable=False)
    first_name = sa.Column('first_name', sa.String(100), nullable=False)
    last_name_kana = sa.Column('last_name_kana', sa.String(100), nullable=False)
    first_name_kana = sa.Column('first_name_kana', sa.String(100), nullable=False)
    gender = sa.Column('gender', sa.String(1), nullable=False)
    zip_code = sa.Column('zip_code', sa.String(20), nullable=False)
    address = sa.Column('address', sa.String(100), nullable=False)
    email = sa.Column('email', sa.String(100), nullable=False)
    allergy = sa.Column('allergy', sa.String(1000))
    message = sa.Column('message', sa.String(10000))
    invitation_side = sa.Column('invitation_side', sa.String(1), nullable=False)
    attendance = sa.Column('attendence', sa.String(1), nullable=False)
    relationship = sa.Column('relationship', sa.String(1), nullable=False)
    mail_check = sa.Column('mail_check', sa.String(1), default=0)

