import sqlite3


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def initial_setup():
    conn = connect_to_db()
    conn.execute(
        """
        DROP TABLE IF EXISTS workouts;
        """
    )
    conn.execute(
        """
        CREATE TABLE workouts (
          id INTEGER PRIMARY KEY NOT NULL,
          name TEXT,
          type TEXT,
          duration INTERVAL
        );
        """
    )
    conn.commit()
    print("Table created successfully")

workouts_seed_data = [
        ("1st workout", "arms", "1min"),
        ("2nd workout", "legs", "2min"),
        ("3rd workout", "back", "3min"),
    ]

if __name__ == "__main__":
    initial_setup()

def workouts_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM workouts
        """
    ).fetchall()
    return [dict(row) for row in rows]

def workouts_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM workouts
        WHERE id = ?
        """,
        (id,),
    ).fetchone()
    return dict(row)

def workouts_create(name, type, duration):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO workouts (name, muscle group, duration)
        VALUES (?, ?, ?)
        RETURNING *
        """,
        (name, type, duration),
    ).fetchone()
    conn.commit()
    return dict(row)

def workouts_update_by_id(id, name, type, duration):
    conn = connect_to_db()
    try:
        row = conn.execute(
            """
            UPDATE workouts SET name = ?, muscle group = ?, duration = ?
            WHERE id = ?
            RETURNING *
            """,
            (name, type, duration, id),
        ).fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()  
    return dict(row) if row else None


def workouts_destroy_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
              """
        DELETE from workouts
        WHERE id = ?
        """,
        (id,),
    )
    conn.commit()
    return {"message": "Workout destroyed successfully"}
    
    # def workouts_update_by_id(id):
#     conn = connect_to_db()
#     row = conn.execute(
#          """
#         UPDATE workouts SET name = ?, type = ?, duration = ?
#         WHERE id = ?
#         RETURNING *
#         """,
#         (name, type, duration, id),
#     ).fetchone()
#     conn.commit()
#     return dict(row)

# workouts_seed_data = [
#         ("1st workout", "arms", "1min"),
#         ("2nd workout", "legs", "2min"),
#         ("3rd workout", "back", "3min"),
#     ]

# def connect_to_db():
#     return sqlite3.connect("your_database.db")

# # Function to seed the workouts data
# def seed_workouts():
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     for name, muscle_group, duration in workouts_seed_data:
#         cursor.execute(
#             "INSERT INTO workouts (name, muscle group, duration) VALUES (?, ?, ?)",
#             (name, muscle_group, duration)
#         )
#     conn.commit()
#     conn.close()
#     print("Database seeded with workout data!")

# if __name__ == "__main__":
#     seed_workouts()