import sqlite3

DB_NAME = "recipes.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


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

    for s in steps:
        progress = int((completed / total_minutes) * 100)

        print("Βήμα", s["order"], ":", s["title"])
        print("Χρόνος:", s["minutes"], "λεπτά")
        print("Υλικά:", ", ".join(s["ingredients"]))
        print("Περιγραφή:", s["description"])
        print("Πρόοδος:", progress, "%\n")

        input("Πάτα Enter για επόμενο βήμα...")

        completed += s["minutes"]
        print()

    print("Η συνταγή ολοκληρώθηκε.")
    print("Τελική πρόοδος: 100%")


def delete_recipe(recipe_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    deleted = cur.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


if __name__ == "__main__":
    term = input("Δώσε όνομα ή κατηγορία για αναζήτηση: ")
    results = search_recipes(term)

    if not results:
        print("Δεν βρέθηκε καμία συνταγή.")
    else:
        print("\nΑποτελέσματα:")
        for r in results:
            print("ID:", r[0], "| Όνομα:", r[1])

        selected_id = int(input("\nΔώσε ID: "))

        action = input("Τι θέλεις να κάνεις; (e=εκτέλεση, p=προβολή, d=διαγραφή): ").strip().lower()

        if action == "d":
            confirm = input("Σίγουρα διαγραφή; (ν/ο): ").strip().lower()
            if confirm == "ν":
                ok = delete_recipe(selected_id)
                if ok:
                    print("Η συνταγή διαγράφηκε.")
                else:
                    print("Δεν βρέθηκε συνταγή με αυτό το ID.")
            else:
                print("Ακύρωση διαγραφής.")

        elif action == "e":
            run_recipe(selected_id)

        else:
            details = get_recipe_details(selected_id)

            if details is None:
                print("Μη έγκυρο ID.")
            else:
                print("\nΛΕΠΤΟΜΕΡΕΙΕΣ")
                print("Recipe:", details["recipe"])
                print("Υλικά συνταγής:", details["recipe_ingredients"])

                print("\nΒήματα:")
                for s in details["steps"]:
                    print(s["order"], ".", s["title"], "(", s["minutes"], "λεπτά )")
                    print("   ", s["description"])
                    print("   Υλικά:", ", ".join(s["ingredients"]))