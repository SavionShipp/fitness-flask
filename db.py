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
    conn.executemany(
        """
        INSERT INTO workouts (name, muscle group, duration)
        VALUES (?,?,?)
        """,
        workouts_seed_data,
    )
    conn.commit()
    print("Seed data created successfully")

    conn.close()


if __name__ == "__main__":
    initial_setup()