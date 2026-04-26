import psycopg2

conn = psycopg2.connect(
    dbname="snake_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS game_sessions (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    score INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    played_at TIMESTAMP DEFAULT NOW()
);
""")
conn.commit()

def get_or_create_player(username):
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    r = cur.fetchone()
    if r: return r[0]
    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    conn.commit()
    return cur.fetchone()[0]

def save_score(pid, score, level):
    cur.execute("INSERT INTO game_sessions(player_id,score,level_reached) VALUES(%s,%s,%s)",(pid,score,level))
    conn.commit()

def get_top():
    cur.execute("""
    SELECT username, score, level_reached, played_at
    FROM game_sessions gs JOIN players p ON p.id=gs.player_id
    ORDER BY score DESC LIMIT 10
    """)
    return cur.fetchall()

def best_score(pid):
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id=%s",(pid,))
    return cur.fetchone()[0] or 0
