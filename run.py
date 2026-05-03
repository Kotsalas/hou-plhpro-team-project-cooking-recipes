import argparse
import runpy
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"


def add_backend_to_path():
    """Προσθέτει το backend στα imports για να φορτώνονται σωστά τα modules."""
    backend_path = str(BACKEND_DIR)
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)


def create_database():
    """Δημιουργεί τη βάση και τους πίνακες αν δεν υπάρχουν ήδη."""
    add_backend_to_path()
    import database

    database.create_tables()


def seed_database():
    """Προσθέτει ενδεικτικές συνταγές στη βάση."""
    add_backend_to_path()
    import seed

    seed.seed()


def ask_for_seed():
    """Ρωτά τον χρήστη αν θέλει να προστεθούν ενδεικτικές συνταγές."""
    while True:
        answer = input("Θέλετε να προστεθούν ενδεικτικές συνταγές; (ν/ο): ").strip().lower()

        if answer in ("ν", "ναι", "y", "yes"):
            return True

        if answer in ("ο", "όχι", "οχι", "n", "no"):
            return False

        print("Παρακαλώ απαντήστε με ναι ή όχι.")


def run_gui():
    """Εκκινεί την εφαρμογή με γραφικό περιβάλλον."""
    runpy.run_path(str(ROOT_DIR / "gui" / "app_gui.py"), run_name="__main__")


def run_cli():
    """Εκκινεί την εφαρμογή από τη γραμμή εντολών."""
    runpy.run_path(str(BACKEND_DIR / "app_cli.py"), run_name="__main__")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Εκκίνηση της εφαρμογής διαχείρισης συνταγών."
    )

    seed_group = parser.add_mutually_exclusive_group()
    seed_group.add_argument(
        "--seed",
        action="store_true",
        help="Προσθέτει ενδεικτικές συνταγές πριν ανοίξει η εφαρμογή.",
    )
    seed_group.add_argument(
        "--no-seed",
        action="store_true",
        help="Δεν ρωτά για seed και ανοίγει απευθείας την εφαρμογή.",
    )

    parser.add_argument(
        "--cli",
        action="store_true",
        help="Ανοίγει την έκδοση γραμμής εντολών αντί για το GUI.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    create_database()

    if args.seed:
        seed_database()
    elif not args.no_seed:
        if ask_for_seed():
            seed_database()

    if args.cli:
        run_cli()
    else:
        run_gui()


if __name__ == "__main__":
    main()
