import psycopg2

def connect():
    return psycopg2.connect(
        dbname="snake_db",
        user="postgres",
        password="Bekarys08",
        host="localhost",
        port=5432
    )

# ---------------- PLAYER ----------------
def get_or_create_player(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    r = cur.fetchone()

    if r:
        conn.close()
        return r[0]

    cur.execute(
        "INSERT INTO players(username) VALUES(%s) RETURNING id",
        (username,)
    )
    pid = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return pid


# ---------------- SAVE GAME ----------------
def save_score(pid, score, level):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (pid, score, level))

    conn.commit()
    conn.close()


# ---------------- LEADERBOARD ----------------
def get_top():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC
        LIMIT 10
    """)

    data = cur.fetchall()
    conn.close()
    return data


# ---------------- PERSONAL BEST ----------------
def best_score(pid):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(score)
        FROM game_sessions
        WHERE player_id=%s
    """, (pid,))

    result = cur.fetchone()[0]
    conn.close()

    return result if result else 0