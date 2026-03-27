# This file stores configuration settings for database connection
# We separate config from logic → good practice (easier to change later)

DB_CONFIG = {
    # "host" → where database server is located
    # "localhost" means it is on your own computer
    "host": "localhost",

    # "database" → name of your PostgreSQL database
    # You must create this database manually in PostgreSQL
    "database": "phonebook",

    # "user" → PostgreSQL username
    # Usually default is "postgres"
    "user": "sabinaermukhanova",

    # "password" → password for database
    # IMPORTANT: replace with your real password
    "password": ""
}