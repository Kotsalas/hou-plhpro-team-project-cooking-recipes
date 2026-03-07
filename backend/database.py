import sqlite3

DB_NAME = "recipes.db"


def create_connection():
    """Δημιουργεί σύνδεση με τη βάση και ενεργοποιεί τα foreign keys"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables():
    """Δημιουργεί τους πίνακες της βάσης"""
    conn = create_connection()
    cursor = conn.cursor()

    # Πίνακας συνταγών
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        total_minutes INTEGER NOT NULL,
        UNIQUE(name, category)
    );
    """)

    # Πίνακας υλικών (ανεξάρτητα υλικά)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    """)

    # Πίνακας βημάτων
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        step_order INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        duration_minutes INTEGER NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
        UNIQUE(recipe_id, step_order)
    );
    """)

    # Συσχέτιση συνταγής - υλικών (many-to-many)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        recipe_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        PRIMARY KEY (recipe_id, ingredient_id),
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
    );
    """)

    # Συσχέτιση βήματος - υλικών (many-to-many)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS step_ingredients (
        step_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        PRIMARY KEY (step_id, ingredient_id),
        FOREIGN KEY (step_id) REFERENCES steps(id) ON DELETE CASCADE,
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
    );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Η βάση δεδομένων δημιουργήθηκε επιτυχώς!")