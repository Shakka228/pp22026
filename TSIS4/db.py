import psycopg2

conn = psycopg2.connect(
    dbname="snake_db",
    user="postgres",
    password="Bekarys08",
    host="localhost",
    port=5432
)

cur = conn.cursor()

def get_or_create_player(username):
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    r = cur.fetchone()
    if r:
        return r[0]

    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    conn.commit()
    return cur.fetchone()[0]

def save_score(pid, score, level):
    cur.execute(
        "INSERT INTO game_sessions(player_id,score,level_reached) VALUES(%s,%s,%s)",
        (pid, score, level)
    )
    conn.commit()

def get_top():
    cur.execute("""
        SELECT username, score, level_reached, played_at
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY score DESC
        LIMIT 10
    """)
    return cur.fetchall()

def best_score(pid):
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id=%s", (pid,))
    return cur.fetchone()[0] or 0