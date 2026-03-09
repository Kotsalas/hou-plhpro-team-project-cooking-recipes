from db import get_connection


# Βοηθητική συνάρτηση που βρίσκει υλικό ή το δημιουργεί αν δεν υπάρχει
def _get_or_create_ingredient(cur, name: str) -> int:
    name = name.strip()

    if not name:
        raise ValueError("Κενό όνομα υλικού.")

    cur.execute("SELECT id FROM ingredients WHERE name = ?", (name,))
    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("INSERT INTO ingredients (name) VALUES (?)", (name,))
    return cur.lastrowid


# Αναζήτηση συνταγών με βάση όνομα ή κατηγορία
def search_recipes(keyword: str):
    kw = f"%{keyword.strip()}%"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, category, difficulty, total_minutes
        FROM recipes
        WHERE name LIKE ? OR category LIKE ?
        ORDER BY name
    """, (kw, kw))

    rows = cur.fetchall()
    conn.close()
    return rows


# Επιστρέφει όλα τα στοιχεία μιας συνταγής
def get_recipe_details(recipe_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, category, difficulty, total_minutes
        FROM recipes
        WHERE id = ?
    """, (recipe_id,))
    recipe = cur.fetchone()

    if recipe is None:
        conn.close()
        return None

    cur.execute("""
        SELECT i.name
        FROM recipe_ingredients ri
        JOIN ingredients i ON i.id = ri.ingredient_id
        WHERE ri.recipe_id = ?
        ORDER BY i.name
    """, (recipe_id,))
    recipe_ingredients = [row[0] for row in cur.fetchall()]

    cur.execute("""
        SELECT id, step_order, title, description, duration_minutes
        FROM steps
        WHERE recipe_id = ?
        ORDER BY step_order
    """, (recipe_id,))
    step_rows = cur.fetchall()

    steps = []

    for step_id, step_order, title, description, duration_minutes in step_rows:
        cur.execute("""
            SELECT i.name
            FROM step_ingredients si
            JOIN ingredients i ON i.id = si.ingredient_id
            WHERE si.step_id = ?
            ORDER BY i.name
        """, (step_id,))
        step_ingredients = [row[0] for row in cur.fetchall()]

        steps.append({
            "step_id": step_id,
            "order": step_order,
            "title": title,
            "description": description,
            "minutes": duration_minutes,
            "ingredients": step_ingredients
        })

    conn.close()

    return {
        "recipe": recipe,
        "recipe_ingredients": recipe_ingredients,
        "steps": steps
    }


# Προσθέτει νέα συνταγή με τα βασικά στοιχεία
# Επιστρέφει (recipe_id, created)
# created=True αν δημιουργήθηκε νέα συνταγή
# created=False αν υπήρχε ήδη
def add_recipe_basic(name: str, category: str, difficulty: str, total_minutes: int):
    name = name.strip()
    category = category.strip()
    difficulty = difficulty.strip()
    total_minutes = int(total_minutes)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM recipes
        WHERE name = ? AND category = ?
    """, (name, category))
    row = cur.fetchone()

    if row:
        conn.close()
        return row[0], False

    cur.execute("""
        INSERT INTO recipes (name, category, difficulty, total_minutes)
        VALUES (?, ?, ?, ?)
    """, (name, category, difficulty, total_minutes))

    recipe_id = cur.lastrowid
    conn.commit()
    conn.close()

    return recipe_id, True


# Προσθέτει υλικό στη συνταγή
# Επιστρέφει True αν προστέθηκε
# Επιστρέφει False αν υπήρχε ήδη
def add_ingredient_to_recipe(recipe_id: int, ingredient_name: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    ing_id = _get_or_create_ingredient(cur, ingredient_name)

    cur.execute("""
        INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id)
        VALUES (?, ?)
    """, (recipe_id, ing_id))

    inserted = cur.rowcount > 0
    conn.commit()
    conn.close()

    return inserted


# Προσθέτει νέο βήμα στο τέλος της συνταγής
# Επιστρέφει το id του βήματος
def add_step(recipe_id: int, title: str, description: str, duration_minutes: int) -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(MAX(step_order), 0) + 1
        FROM steps
        WHERE recipe_id = ?
    """, (recipe_id,))
    next_order = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO steps (recipe_id, step_order, title, description, duration_minutes)
        VALUES (?, ?, ?, ?, ?)
    """, (recipe_id, next_order, title.strip(), description.strip(), int(duration_minutes)))

    step_id = cur.lastrowid
    conn.commit()
    conn.close()

    return step_id


# Προσθέτει υλικό σε συγκεκριμένο βήμα
# Επιστρέφει True αν προστέθηκε
# Επιστρέφει False αν υπήρχε ήδη
def add_ingredient_to_step(step_id: int, ingredient_name: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    ing_id = _get_or_create_ingredient(cur, ingredient_name)

    cur.execute("""
        INSERT OR IGNORE INTO step_ingredients (step_id, ingredient_id)
        VALUES (?, ?)
    """, (step_id, ing_id))

    inserted = cur.rowcount > 0
    conn.commit()
    conn.close()

    return inserted


# Ενημερώνει τα βασικά στοιχεία της συνταγής
# Επιστρέφει (ok, error_msg)
def update_recipe_basic(recipe_id: int, name: str, category: str, difficulty: str, total_minutes: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE recipes
            SET name = ?, category = ?, difficulty = ?, total_minutes = ?
            WHERE id = ?
        """, (name.strip(), category.strip(), difficulty.strip(), int(total_minutes), recipe_id))

        ok = cur.rowcount > 0
        conn.commit()
        conn.close()
        return ok, None

    except Exception as e:
        conn.rollback()
        conn.close()
        return False, str(e)


# Εκτελεί τη συνταγή βήμα-βήμα και εμφανίζει την πρόοδο
def run_recipe(recipe_id: int):
    details = get_recipe_details(recipe_id)

    if details is None:
        print("Δεν βρέθηκε συνταγή.")
        return

    recipe = details["recipe"]
    steps = details["steps"]
    total_minutes = recipe[4]
    completed = 0

    print("\n==============================")
    print("Ξεκινάμε εκτέλεση:", recipe[1])
    print("Συνολικός χρόνος:", total_minutes, "λεπτά")
    print("==============================\n")

    if not steps:
        print("Η συνταγή δεν έχει βήματα.")
        return

    for s in steps:
        progress = 0

        if total_minutes > 0:
            progress = int((completed / total_minutes) * 100)

        print(f"Βήμα {s['order']}: {s['title']}")
        print("Χρόνος:", s["minutes"], "λεπτά")
        print("Υλικά:", ", ".join(s["ingredients"]) if s["ingredients"] else "(κανένα)")
        print("Περιγραφή:", s["description"])
        print("Πρόοδος:", progress, "%\n")

        input("Πάτα Enter για επόμενο βήμα...")

        completed += s["minutes"]
        print()

    print("Η συνταγή ολοκληρώθηκε.")
    print("Τελική πρόοδος: 100%")


# Διαγράφει συνταγή με βάση το id
# Επιστρέφει True αν διαγράφηκε
# Επιστρέφει False αν δεν βρέθηκε
def delete_recipe(recipe_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    deleted = cur.rowcount > 0

    conn.commit()
    conn.close()

    return deleted