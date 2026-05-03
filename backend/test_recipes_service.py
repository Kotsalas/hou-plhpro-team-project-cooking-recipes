import os
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import database
import recipes_service


class RecipesServiceEditingTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "recipes.db")
        self.old_database_name = database.DB_NAME
        self.old_get_connection = recipes_service.get_connection

        database.DB_NAME = self.db_path
        database.create_tables()

        def get_test_connection():
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn

        recipes_service.get_connection = get_test_connection

    def tearDown(self):
        recipes_service.get_connection = self.old_get_connection
        database.DB_NAME = self.old_database_name
        self.temp_dir.cleanup()

    def test_updates_existing_step_details(self):
        recipe_id, _ = recipes_service.add_recipe_basic("Σούπα", "Κυρίως", "Εύκολη", 30)
        step_id = recipes_service.add_step(recipe_id, "Παλαιός τίτλος", "Παλαιά περιγραφή", 10)

        ok = recipes_service.update_step(step_id, "Νέος τίτλος", "Νέα περιγραφή", 15)

        details = recipes_service.get_recipe_details(recipe_id)
        self.assertTrue(ok)
        self.assertEqual(details["steps"][0]["title"], "Νέος τίτλος")
        self.assertEqual(details["steps"][0]["description"], "Νέα περιγραφή")
        self.assertEqual(details["steps"][0]["minutes"], 15)

    def test_deletes_step_and_keeps_step_order_sequential(self):
        recipe_id, _ = recipes_service.add_recipe_basic("Πίτα", "Ορεκτικό", "Μέτρια", 45)
        first_id = recipes_service.add_step(recipe_id, "Πρώτο", "Πρώτη περιγραφή", 10)
        recipes_service.add_step(recipe_id, "Δεύτερο", "Δεύτερη περιγραφή", 15)
        recipes_service.add_step(recipe_id, "Τρίτο", "Τρίτη περιγραφή", 20)

        ok = recipes_service.delete_step(first_id)

        details = recipes_service.get_recipe_details(recipe_id)
        self.assertTrue(ok)
        self.assertEqual([step["order"] for step in details["steps"]], [1, 2])
        self.assertEqual([step["title"] for step in details["steps"]], ["Δεύτερο", "Τρίτο"])

    def test_removes_ingredients_from_recipe_and_step(self):
        recipe_id, _ = recipes_service.add_recipe_basic("Σαλάτα", "Σαλάτες", "Εύκολη", 10)
        step_id = recipes_service.add_step(recipe_id, "Ανάμειξη", "Ανακατεύουμε", 10)
        recipes_service.add_ingredient_to_recipe(recipe_id, "Ντομάτα")
        recipes_service.add_ingredient_to_recipe(recipe_id, "Αγγούρι")
        recipes_service.add_ingredient_to_step(step_id, "Ντομάτα")
        recipes_service.add_ingredient_to_step(step_id, "Αγγούρι")

        removed_recipe = recipes_service.remove_ingredient_from_recipe(recipe_id, "Αγγούρι")
        removed_step = recipes_service.remove_ingredient_from_step(step_id, "Ντομάτα")

        details = recipes_service.get_recipe_details(recipe_id)
        self.assertTrue(removed_recipe)
        self.assertTrue(removed_step)
        self.assertEqual(details["recipe_ingredients"], ["Ντομάτα"])
        self.assertEqual(details["steps"][0]["ingredients"], ["Αγγούρι"])

    def test_replaces_step_ingredients(self):
        recipe_id, _ = recipes_service.add_recipe_basic("Ρύζι", "Κυρίως", "Εύκολη", 20)
        step_id = recipes_service.add_step(recipe_id, "Βράσιμο", "Βράζουμε", 20)
        recipes_service.add_ingredient_to_step(step_id, "Ρύζι")

        ok = recipes_service.replace_step_ingredients(step_id, ["Νερό", "Αλάτι"])

        details = recipes_service.get_recipe_details(recipe_id)
        self.assertTrue(ok)
        self.assertEqual(details["steps"][0]["ingredients"], ["Αλάτι", "Νερό"])


if __name__ == "__main__":
    unittest.main()
