import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key_change_this_in_prod'
    # Update the below URI with your actual MySQL credentials: mysql+pymysql://username:password@localhost/holiday_booking
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:pahulpreetbcasem1@localhost/holiday_booking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
