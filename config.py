import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uchechukwu'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///lessons.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  