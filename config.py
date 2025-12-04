class Config:
    SECRET_KEY = "supersecretkey123"
    SQLALCHEMY_DATABASE_URI = "sqlite:///expense_data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email settings (optional)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "youremail@gmail.com"
    MAIL_PASSWORD = "your-app-password"
