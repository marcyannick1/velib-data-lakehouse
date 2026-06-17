from sqlalchemy import create_engine


DATABASE_URL = (
    "postgresql://"
    "velib_user:"
    "velib_password@"
    "postgres:5432/"
    "velib"
)


engine = create_engine(
    DATABASE_URL
)