import os
import logging
from psycopg2 import pool

logger = logging.getLogger("db")

db_pool = None


def init_db_pool():
    global db_pool

    if db_pool:
        return

    try:
        db_pool = pool.SimpleConnectionPool(
            1, 10,
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            connect_timeout=5
        )

        logger.info("DB pool initialized")

    except Exception as e:
        logger.exception("DB pool initialization failed")
        raise


def get_connection():
    if not db_pool:
        init_db_pool()

    return db_pool.getconn()


def release_connection(conn):
    if db_pool and conn:
        db_pool.putconn(conn)


def close_pool():
    global db_pool

    if db_pool:
        db_pool.closeall()
        db_pool = None