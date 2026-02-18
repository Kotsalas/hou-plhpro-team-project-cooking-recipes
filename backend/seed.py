import sqlite3

DB_NAME = "recipes.db"


def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def seed_recipe():
    conn = get_conn()
    cur = conn.cursor()

    # 1) Βάζουμε συνταγή (χωρίς διπλότυπα)
    cur.execute("""
    INSERT OR IGNORE INTO recipes (name, category, difficulty, total_minutes)
    VALUES (?, ?, ?, ?)
    """, ("Καρμπονάρα", "Ζυμαρικά", "Μέτρια", 20))

    cur.execute("""
    SELECT id FROM recipes
    WHERE name = ? AND category = ?
    """, ("Καρμπονάρα", "Ζυμαρικά"))
    recipe_id = cur.fetchone()[0]

    # 2) Υλικά (με ΜΠΕΪΚΟΝ)
    ingredient_names = ["Μακαρόνια", "Αλάτι", "Μπέικον", "Αυγά", "Παρμεζάνα", "Πιπέρι"]
    ingredient_ids = {}

    for name in ingredient_names:
        cur.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?);", (name,))
        cur.execute("SELECT id FROM ingredients WHERE name = ?;", (name,))
        ing_id = cur.fetchone()[0]
        ingredient_ids[name] = ing_id

        cur.execute("""
        INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id)
        VALUES (?, ?)
        """, (recipe_id, ing_id))

    # 3) Βήματα + υλικά βημάτων
    steps_data = [
        (1, "Βράσιμο ζυμαρικών", "Βράζουμε τα μακαρόνια σε αλατισμένο νερό", 10, ["Μακαρόνια", "Αλάτι"]),
        (2, "Ψήνουμε το μπέικον", "Σοτάρουμε το μπέικον μέχρι να γίνει τραγανό", 6, ["Μπέικον"]),
        (3, "Σάλτσα & ανακάτεμα", "Χτυπάμε αυγά με παρμεζάνα και πιπέρι και ανακατεύουμε εκτός φωτιάς", 4,
         ["Αυγά", "Παρμεζάνα", "Πιπέρι"]),
    ]

    for step_order, title, description, minutes, step_ings in steps_data:
        cur.execute("""
        INSERT OR IGNORE INTO steps (recipe_id, step_order, title, description, duration_minutes)
        VALUES (?, ?, ?, ?, ?)
        """, (recipe_id, step_order, title, description, minutes))

        cur.execute("""
        SELECT id FROM steps WHERE recipe_id = ? AND step_order = ?
        """, (recipe_id, step_order))
        step_id = cur.fetchone()[0]

        for ing_name in step_ings:
            cur.execute("""
            INSERT OR IGNORE INTO step_ingredients (step_id, ingredient_id)
            VALUES (?, ?)
            """, (step_id, ingredient_ids[ing_name]))

    conn.commit()
    conn.close()

    return recipe_id


def load_full_recipe(recipe_id: int):
    conn = get_conn()
    cur = conn.cursor()

    # Συνταγή
    cur.execute("""
    SELECT id, name, category, difficulty, total_minutes
    FROM recipes
    WHERE id = ?
    """, (recipe_id,))
    r = cur.fetchone()

    # Υλικά συνταγής
    cur.execute("""
    SELECT i.name
    FROM ingredients i
    JOIN recipe_ingredients ri ON ri.ingredient_id = i.id
    WHERE ri.recipe_id = ?
    ORDER BY i.name
    """, (recipe_id,))
    recipe_ings = [row[0] for row in cur.fetchall()]

    # Βήματα
    cur.execute("""
    SELECT id, step_order, title, description, duration_minutes
    FROM steps
    WHERE recipe_id = ?
    ORDER BY step_order
    """, (recipe_id,))
    steps_rows = cur.fetchall()

    steps_full = []
    for step_id, step_order, title, description, duration_minutes in steps_rows:
        cur.execute("""
        SELECT i.name
        FROM ingredients i
        JOIN step_ingredients si ON si.ingredient_id = i.id
        WHERE si.step_id = ?
        ORDER BY i.name
        """, (step_id,))
        step_ings = [row[0] for row in cur.fetchall()]

        steps_full.append({
            "step_order": step_order,
            "title": title,
            "description": description,
            "duration_minutes": duration_minutes,
            "ingredients": step_ings
        })

    conn.close()

    return {
        "id": r[0],
        "name": r[1],
        "category": r[2],
        "difficulty": r[3],
        "total_minutes": r[4],
        "ingredients": recipe_ings,
        "steps": steps_full
    }


if __name__ == "__main__":
    rid = seed_recipe()
    full = load_full_recipe(rid)
    print("OK! Seed done.")
    print(full)