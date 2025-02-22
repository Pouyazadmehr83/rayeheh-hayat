# config.py
import os

class Config:
    # رشته اتصال به پایگاه داده MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql://your_username:your_password@localhost/company_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key-change-me'
