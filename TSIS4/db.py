import psycopg2


#  CONNECTION 
conn = psycopg2.connect(
    dbname="snake_db",
    user="sabinaermukhanova",
    password="",      # CHANGE if needed
    host="localhost",
    port="5432"
)

cur = conn.cursor()


# CREATE TABLES 
cur.execute("""
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS game_sessions (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    score INTEGER NOT NULL,
    level INTEGER NOT NULL,
    played_at TIMESTAMP DEFAULT NOW()
)
""")

conn.commit()


#  SAVE RESULT 
def save_result(username, score, level):

    # check if player exists
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player = cur.fetchone()

    # if not -> create
    if player is None:
        cur.execute(
            "INSERT INTO players(username) VALUES(%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
    else:
        player_id = player[0]

    # insert game session
    cur.execute(
        "INSERT INTO game_sessions(player_id, score, level) VALUES(%s, %s, %s)",
        (player_id, score, level)
    )

    conn.commit()


#  TOP 10 
def get_top10():
    cur.execute("""
        SELECT players.username, game_sessions.score, game_sessions.level
        FROM game_sessions
        JOIN players ON players.id = game_sessions.player_id
        ORDER BY game_sessions.score DESC
        LIMIT 10
    """)

    return cur.fetchall()


#  PERSONAL BEST 
def get_best(username):
    cur.execute("""
        SELECT MAX(game_sessions.score)
        FROM game_sessions
        JOIN players ON players.id = game_sessions.player_id
        WHERE players.username = %s
    """, (username,))

    result = cur.fetchone()[0]

    return result if result else 0