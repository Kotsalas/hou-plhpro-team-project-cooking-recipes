from recipes_service import (
    search_recipes,
    get_recipe_details,
    run_recipe,
    delete_recipe,
    add_recipe_basic,
    add_ingredient_to_recipe,
    add_step,
    add_ingredient_to_step,
    update_recipe_basic
)


def show_details(details):
    r = details["recipe"]

    print("\n==============================")
    print("ΛΕΠΤΟΜΕΡΕΙΕΣ ΣΥΝΤΑΓΗΣ")
    print("==============================")
    print(f"ID: {r[0]}")
    print(f"Όνομα: {r[1]}")
    print(f"Κατηγορία: {r[2]}")
    print(f"Δυσκολία: {r[3]}")
    print(f"Συνολικός χρόνος: {r[4]} λεπτά")

    print("\nΥλικά συνταγής:")
    if details["recipe_ingredients"]:
        for ing in details["recipe_ingredients"]:
            print(" -", ing)
    else:
        print(" (κανένα)")

    print("\nΒήματα:")
    if details["steps"]:
        for s in details["steps"]:
            print(f"{s['order']}. {s['title']} ({s['minutes']} λεπτά)")
            print("   ", s["description"])
            print("   Υλικά:", ", ".join(s["ingredients"]) if s["ingredients"] else "(κανένα)")
    else:
        print(" (δεν υπάρχουν βήματα)")


def create_flow():
    name = input("Όνομα συνταγής: ").strip()
    category = input("Κατηγορία: ").strip()
    difficulty = input("Δυσκολία (Εύκολη/Μέτρια/Δύσκολη): ").strip()
    total_minutes = int(input("Συνολικός χρόνος (λεπτά): ").strip())

    recipe_id, created = add_recipe_basic(name, category, difficulty, total_minutes)

    if created:
        print("Η συνταγή καταχωρήθηκε με ID:", recipe_id)
    else:
        print("Η συνταγή υπήρχε ήδη (ID:", recipe_id, ").")
        cont = input("Θες να συνεχίσουμε να προσθέτουμε υλικά/βήματα σε αυτή; (ν/ο): ").strip().lower()
        if cont != "ν":
            print("ΟΚ, δεν θα προσθέσουμε άλλα στοιχεία τώρα.")
            return

    print("\nΠροσθήκη υλικών συνταγής (Enter κενό για τέλος):")
    while True:
        ing = input("Υλικό: ").strip()
        if not ing:
            break

        ok = add_ingredient_to_recipe(recipe_id, ing)
        print("  + προστέθηκε" if ok else "  (υπήρχε ήδη)")

    print("\nΠροσθήκη βημάτων (Enter κενό στον τίτλο για τέλος):")
    while True:
        title = input("Τίτλος βήματος: ").strip()
        if not title:
            break

        desc = input("Περιγραφή: ").strip()
        mins = int(input("Διάρκεια (λεπτά): ").strip())

        step_id = add_step(recipe_id, title, desc, mins)

        print("  Υλικά για αυτό το βήμα (Enter κενό για τέλος):")
        while True:
            ing = input("   - Υλικό: ").strip()
            if not ing:
                break

            ok = add_ingredient_to_step(step_id, ing)
            print("     + προστέθηκε" if ok else "     (υπήρχε ήδη)")

    print("\n✅ Ολοκληρώθηκε η καταχώρηση.")
    details = get_recipe_details(recipe_id)
    if details:
        show_details(details)


def edit_basic_flow(recipe_id: int):
    details = get_recipe_details(recipe_id)
    if details is None:
        print("Μη έγκυρο ID.")
        return

    r = details["recipe"]

    print("\nΆφησε κενό για να μείνει όπως είναι.")
    new_name = input(f"Όνομα ({r[1]}): ").strip()
    new_category = input(f"Κατηγορία ({r[2]}): ").strip()
    new_difficulty = input(f"Δυσκολία ({r[3]}): ").strip()
    new_total = input(f"Συνολικός χρόνος λεπτά ({r[4]}): ").strip()

    name = new_name if new_name else r[1]
    category = new_category if new_category else r[2]
    difficulty = new_difficulty if new_difficulty else r[3]
    total_minutes = int(new_total) if new_total else r[4]

    ok, err = update_recipe_basic(recipe_id, name, category, difficulty, total_minutes)

    if ok:
        print("✅ Η συνταγή ενημερώθηκε.")
    else:
        if err:
            print("❌ Αποτυχία ενημέρωσης:", err)
        else:
            print("Δεν βρέθηκε συνταγή.")


def search_flow():
    term = input("Δώσε όνομα ή κατηγορία για αναζήτηση: ").strip()
    results = search_recipes(term)

    if not results:
        print("Δεν βρέθηκε καμία συνταγή.")
        return

    print("\nΑποτελέσματα:")
    for r in results:
        print(f"ID: {r[0]} | Όνομα: {r[1]} | Κατηγορία: {r[2]} | Δυσκολία: {r[3]} | Χρόνος: {r[4]} λεπτά")

    selected_id = int(input("\nΔώσε ID: ").strip())
    action = input(
        "Τι θέλεις να κάνεις; (e=εκτέλεση, p=προβολή, d=διαγραφή, u=τροποποίηση): "
    ).strip().lower()

    if action == "d":
        confirm = input("Σίγουρα διαγραφή; (ν/ο): ").strip().lower()
        if confirm == "ν":
            ok = delete_recipe(selected_id)
            print("Η συνταγή διαγράφηκε." if ok else "Δεν βρέθηκε συνταγή με αυτό το ID.")
        else:
            print("Ακύρωση διαγραφής.")

    elif action == "e":
        run_recipe(selected_id)

    elif action == "p":
        details = get_recipe_details(selected_id)
        if details is None:
            print("Μη έγκυρο ID.")
        else:
            show_details(details)

    elif action == "u":
        edit_basic_flow(selected_id)

    else:
        print("Μη έγκυρη επιλογή.")


if __name__ == "__main__":
    while True:
        print("\n==============================")
        print("ΣΥΣΤΗΜΑ ΔΙΑΧΕΙΡΙΣΗΣ ΣΥΝΤΑΓΩΝ")
        print("==============================")
        print("1. Δημιουργία νέας συνταγής")
        print("2. Αναζήτηση συνταγής")
        print("0. Έξοδος")

        choice = input("Επιλογή: ").strip()

        if choice == "1":
            create_flow()
        elif choice == "2":

            search_flow()
        elif choice == "0":
            print("Έξοδος από το πρόγραμμα.")
            break
        else:
            print("Μη έγκυρη επιλογή.")