# Import psycopg2 library
# It is used to connect Python with PostgreSQL
import psycopg2

# Import configuration dictionary from config.py
from config import DB_CONFIG

# Function that creates and returns connection
def get_connection():
    # psycopg2.connect() → establishes connection to database
    # **DB_CONFIG → unpacks dictionary into arguments
    # same as: host=..., database=..., user=..., password=...
    conn = psycopg2.connect(**DB_CONFIG)

    # Return connection object
    return conn