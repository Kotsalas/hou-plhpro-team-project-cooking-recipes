import sqlite3

DB_NAME = "recipes.db"


def create_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Πίνακας συνταγών
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT CHECK(difficulty IN ('εύκολη', 'μέτρια', 'δύσκολη')),
            total_time_minutes INTEGER NOT NULL
        );
    """)

    # Πίνακας υλικών
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            quantity TEXT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
        );
    """)

    # Πίνακας βημάτων
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            step_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            duration_hours INTEGER DEFAULT 0,
            duration_minutes INTEGER DEFAULT 0,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()
    print("Η βάση δεδομένων δημιουργήθηκε επιτυχώς!")


if __name__ == "__main__":
    create_tables()