import sqlite3

DB_NAME = "recipes.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def seed():
    conn = get_connection()
    cur = conn.cursor()

    # 1️⃣ Δημιουργία συνταγής
    cur.execute("""
        INSERT OR IGNORE INTO recipes (name, category, difficulty, total_minutes)
        VALUES (?, ?, ?, ?)
    """, ("Καρμπονάρα", "Ζυμαρικά", "Μέτρια", 20))

    cur.execute("""
        SELECT id FROM recipes
        WHERE name = ? AND category = ?
    """, ("Καρμπονάρα", "Ζυμαρικά"))

    recipe_id = cur.fetchone()[0]

    # 2️⃣ Υλικά
    ingredients = ["Μακαρόνια", "Αλάτι", "Μπέικον", "Αυγά", "Παρμεζάνα", "Πιπέρι"]
    ingredient_ids = {}

    for name in ingredients:
        cur.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)", (name,))
        cur.execute("SELECT id FROM ingredients WHERE name = ?", (name,))
        ingredient_ids[name] = cur.fetchone()[0]

        cur.execute("""
            INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id)
            VALUES (?, ?)
        """, (recipe_id, ingredient_ids[name]))

    # 3️⃣ Βήματα
    steps = [
        (1, "Βράσιμο ζυμαρικών",
         "Βράζουμε τα μακαρόνια σε αλατισμένο νερό", 10,
         ["Μακαρόνια", "Αλάτι"]),

        (2, "Ψήσιμο μπέικον",
         "Σοτάρουμε το μπέικον μέχρι να γίνει τραγανό", 6,
         ["Μπέικον"]),

        (3, "Σάλτσα",
         "Ανακατεύουμε αυγά, παρμεζάνα και πιπέρι και ενώνουμε εκτός φωτιάς", 4,
         ["Αυγά", "Παρμεζάνα", "Πιπέρι"])
    ]

    for step_order, title, description, minutes, step_ingredients in steps:
        cur.execute("""
            INSERT OR IGNORE INTO steps
            (recipe_id, step_order, title, description, duration_minutes)
            VALUES (?, ?, ?, ?, ?)
        """, (recipe_id, step_order, title, description, minutes))

        cur.execute("""
            SELECT id FROM steps
            WHERE recipe_id = ? AND step_order = ?
        """, (recipe_id, step_order))

        step_id = cur.fetchone()[0]

        for ing_name in step_ingredients:
            cur.execute("""
                INSERT OR IGNORE INTO step_ingredients (step_id, ingredient_id)
                VALUES (?, ?)
            """, (step_id, ingredient_ids[ing_name]))

    conn.commit()
    conn.close()

    print("Seed ολοκληρώθηκε επιτυχώς!")


if __name__ == "__main__":
    seed()