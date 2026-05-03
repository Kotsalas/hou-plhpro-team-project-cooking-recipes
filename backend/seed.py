import sqlite3

DB_NAME = "recipes.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


RECIPES = [
    {
        "name": "Καρμπονάρα",
        "category": "Ζυμαρικά",
        "difficulty": "Μέτρια",
        "total_minutes": 20,
        "ingredients": ["Μακαρόνια", "Αλάτι", "Μπέικον", "Αυγά", "Παρμεζάνα", "Πιπέρι"],
        "steps": [
            {
                "title": "Βράσιμο ζυμαρικών",
                "description": "Βράζουμε τα μακαρόνια σε αλατισμένο νερό.",
                "minutes": 10,
                "ingredients": ["Μακαρόνια", "Αλάτι"],
            },
            {
                "title": "Ψήσιμο μπέικον",
                "description": "Σοτάρουμε το μπέικον μέχρι να γίνει τραγανό.",
                "minutes": 6,
                "ingredients": ["Μπέικον"],
            },
            {
                "title": "Σάλτσα",
                "description": "Ανακατεύουμε αυγά, παρμεζάνα και πιπέρι και ενώνουμε εκτός φωτιάς.",
                "minutes": 4,
                "ingredients": ["Αυγά", "Παρμεζάνα", "Πιπέρι"],
            },
        ],
    },
    {
        "name": "Μοκέκα",
        "category": "Φαγητό",
        "difficulty": "Εύκολη",
        "total_minutes": 90,
        "ingredients": [
            "Σφυρίδα",
            "Λεμόνι",
            "Κρεμμύδι",
            "Κόκκινη πιπεριά",
            "Πράσινη πιπεριά",
            "Τομάτες",
            "Κόλιαντρο",
            "Γάλα καρύδας",
            "Ελαιόλαδο με καπνιστή πάπρικα",
            "Ζωμός γαρίδας",
            "Αλάτι",
        ],
        "steps": [
            {
                "title": "Μαρινάρισμα ψαριού",
                "description": "Πλένουμε καλά το ψάρι, το αλείφουμε με χυμό λεμονιού και το αφήνουμε να ξεκουραστεί.",
                "minutes": 60,
                "ingredients": ["Σφυρίδα", "Λεμόνι"],
            },
            {
                "title": "Στήσιμο κατσαρόλας",
                "description": "Βάζουμε σε μεγάλη κατσαρόλα το ψάρι, το κρεμμύδι, τις πιπεριές και τις τομάτες. Πασπαλίζουμε με κόλιαντρο.",
                "minutes": 5,
                "ingredients": ["Σφυρίδα", "Κρεμμύδι", "Κόκκινη πιπεριά", "Πράσινη πιπεριά", "Τομάτες", "Κόλιαντρο"],
            },
            {
                "title": "Μαγείρεμα",
                "description": "Προσθέτουμε ζωμό γαρίδας και γάλα καρύδας. Μαγειρεύουμε σε χαμηλή φωτιά ανακατεύοντας περιστασιακά.",
                "minutes": 20,
                "ingredients": ["Ζωμός γαρίδας", "Γάλα καρύδας"],
            },
            {
                "title": "Τελείωμα",
                "description": "Προσθέτουμε ελαιόλαδο με πάπρικα και αλάτι. Αφαιρούμε από τη φωτιά και σερβίρουμε.",
                "minutes": 5,
                "ingredients": ["Ελαιόλαδο με καπνιστή πάπρικα", "Αλάτι"],
            },
        ],
    },
    {
        "name": "Ακαραζέ",
        "category": "Σνακ",
        "difficulty": "Δύσκολη",
        "total_minutes": 90,
        "ingredients": [
            "Μαυρομάτικα φασόλια",
            "Κρεμμύδι",
            "Αλάτι",
            "Κάσιους",
            "Αράπικα φυστίκια",
            "Λευκό ψωμί",
            "Γαρίδες",
            "Ελαιόλαδο με καπνιστή πάπρικα",
            "Τομάτα",
            "Ζωμός γαρίδας",
            "Γάλα",
            "Γάλα καρύδας",
            "Μπάμιες",
            "Πράσινο κρεμμύδι",
            "Κόλιαντρο",
            "Μαϊντανός",
        ],
        "steps": [
            {
                "title": "Μούλιασμα φασολιών",
                "description": "Βάζουμε τα φασόλια σε νερό όλη τη νύχτα και αφαιρούμε τη φλούδα.",
                "minutes": 10,
                "ingredients": ["Μαυρομάτικα φασόλια"],
            },
            {
                "title": "Ζύμη ακαραζέ",
                "description": "Χτυπάμε τα φασόλια με κρεμμύδι και αλάτι. Ανακατεύουμε καλά μέχρι η ζύμη να γίνει αφράτη.",
                "minutes": 15,
                "ingredients": ["Μαυρομάτικα φασόλια", "Κρεμμύδι", "Αλάτι"],
            },
            {
                "title": "Τηγάνισμα",
                "description": "Σχηματίζουμε μικρά ψωμάκια και τα τηγανίζουμε σε ελαιόλαδο με πάπρικα.",
                "minutes": 15,
                "ingredients": ["Ελαιόλαδο με καπνιστή πάπρικα"],
            },
            {
                "title": "Γέμιση βαταπά",
                "description": "Μουσκεύουμε το ψωμί σε γάλα και γάλα καρύδας. Χτυπάμε με κάσιους, φυστίκια, γαρίδες και μπαχαρικά και δένουμε το μείγμα σε κατσαρόλα.",
                "minutes": 25,
                "ingredients": ["Λευκό ψωμί", "Γάλα", "Γάλα καρύδας", "Κάσιους", "Αράπικα φυστίκια", "Γαρίδες", "Ζωμός γαρίδας"],
            },
            {
                "title": "Γέμιση καρουρού",
                "description": "Βράζουμε τις μπάμιες και προσθέτουμε μείγμα από κάσιους, γαρίδες, φυστίκια, μυρωδικά, λάδι πάπρικας και γάλα καρύδας.",
                "minutes": 20,
                "ingredients": ["Μπάμιες", "Κάσιους", "Γαρίδες", "Αράπικα φυστίκια", "Πράσινο κρεμμύδι", "Κόλιαντρο", "Μαϊντανός", "Γάλα καρύδας"],
            },
            {
                "title": "Σερβίρισμα",
                "description": "Κόβουμε το ακαραζέ στη μέση και βάζουμε τη γέμιση.",
                "minutes": 5,
                "ingredients": [],
            },
        ],
    },
    {
        "name": "Σπιτική Μαρμελάδα Γάλακτος",
        "category": "Γλυκό",
        "difficulty": "Εύκολη",
        "total_minutes": 60,
        "ingredients": ["Ζάχαρη", "Γάλα"],
        "steps": [
            {
                "title": "Ανάμειξη",
                "description": "Ρίχνουμε στη χύτρα ταχύτητας το γάλα και τη ζάχαρη.",
                "minutes": 5,
                "ingredients": ["Ζάχαρη", "Γάλα"],
            },
            {
                "title": "Βράσιμο",
                "description": "Σε μέτρια φωτιά αφήνουμε τα υλικά για 45 λεπτά με μία ώρα.",
                "minutes": 50,
                "ingredients": ["Ζάχαρη", "Γάλα"],
            },
            {
                "title": "Έλεγχος υφής",
                "description": "Ανοίγουμε τη χύτρα και αφήνουμε να κρυώσει. Ελέγχουμε αν η σύσταση είναι κρεμώδης.",
                "minutes": 5,
                "ingredients": [],
            },
        ],
    },
]


def get_or_create_ingredient(cur, name):
    cur.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)", (name,))
    cur.execute("SELECT id FROM ingredients WHERE name = ?", (name,))
    return cur.fetchone()[0]


def seed_recipe(cur, recipe):
    cur.execute("""
        INSERT OR IGNORE INTO recipes (name, category, difficulty, total_minutes)
        VALUES (?, ?, ?, ?)
    """, (
        recipe["name"],
        recipe["category"],
        recipe["difficulty"],
        recipe["total_minutes"],
    ))

    cur.execute("""
        SELECT id FROM recipes
        WHERE name = ? AND category = ?
    """, (recipe["name"], recipe["category"]))
    recipe_id = cur.fetchone()[0]

    ingredient_ids = {}
    for ingredient in recipe["ingredients"]:
        ingredient_ids[ingredient] = get_or_create_ingredient(cur, ingredient)
        cur.execute("""
            INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id)
            VALUES (?, ?)
        """, (recipe_id, ingredient_ids[ingredient]))

    for step_order, step in enumerate(recipe["steps"], start=1):
        cur.execute("""
            INSERT OR IGNORE INTO steps
            (recipe_id, step_order, title, description, duration_minutes)
            VALUES (?, ?, ?, ?, ?)
        """, (
            recipe_id,
            step_order,
            step["title"],
            step["description"],
            step["minutes"],
        ))

        cur.execute("""
            SELECT id FROM steps
            WHERE recipe_id = ? AND step_order = ?
        """, (recipe_id, step_order))
        step_id = cur.fetchone()[0]

        for ingredient in step["ingredients"]:
            ingredient_ids[ingredient] = get_or_create_ingredient(cur, ingredient)
            cur.execute("""
                INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id)
                VALUES (?, ?)
            """, (recipe_id, ingredient_ids[ingredient]))
            cur.execute("""
                INSERT OR IGNORE INTO step_ingredients (step_id, ingredient_id)
                VALUES (?, ?)
            """, (step_id, ingredient_ids[ingredient]))


def seed():
    conn = get_connection()
    cur = conn.cursor()

    for recipe in RECIPES:
        seed_recipe(cur, recipe)

    conn.commit()
    conn.close()

    print("Seed ολοκληρώθηκε επιτυχώς!")


if __name__ == "__main__":
    seed()
