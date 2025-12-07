class Config:
    # Data Base
    SECRET_KEY = "test_secret_key"  
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Login-Manager 
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_DURATION = 86400  # 1 jour
    
    # Other
    DEBUG = True
