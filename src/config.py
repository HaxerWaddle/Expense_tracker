from datetime import timedelta
class Config:
    SECRET_KEY = 'super secret key'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    REMEMBER_COOKIE_DURATION = timedelta(days=1)
