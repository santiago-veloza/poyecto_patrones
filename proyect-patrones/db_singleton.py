from flask_sqlalchemy import SQLAlchemy

class DatabaseSingleton:
    _instance = None
    db = SQLAlchemy()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_db(cls):
        return cls.db
