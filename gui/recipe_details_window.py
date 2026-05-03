import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from recipes_service import (
    add_ingredient_to_recipe,
    add_ingredient_to_step,
    add_step,
    delete_step,
    get_recipe_details,
    remove_ingredient_from_recipe,
    replace_step_ingredients,
    update_recipe_basic,
    update_step,
)
from create_recipe_window import StepDialog


class RecipeDetailsWindow:
    def __init__(self, parent, recipe_id, callback):
        self.recipe_id = recipe_id
        self.callback = callback
        self.details = get_recipe_details(recipe_id)
        
        if not self.details:
            messagebox.showerror("Σφάλμα", "Δεν βρέθηκε η συνταγή")
            return
        
        self.window = tk.Toplevel(parent)
        self.window.title("Λεπτομέρειες Συνταγής")
        self.window.geometry("700x600")
        
        # Κύριο frame με scrollbar
        canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Σύνδεση ροδέλας ποντικιού
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        recipe = self.details['recipe']
        
        # Τίτλος
        self.title_label = ttk.Label(main_frame, text=recipe[1], font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Βασικά στοιχεία
        ttk.Label(main_frame, text="Βασικά Στοιχεία", 
                 font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="ID:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text=str(recipe[0])).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Όνομα:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.insert(0, recipe[1])
        self.name_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(main_frame, text="Κατηγορία:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.category_entry = ttk.Entry(main_frame, width=40)
        self.category_entry.insert(0, recipe[2])
        self.category_entry.grid(row=4, column=1, pady=5)
        
        ttk.Label(main_frame, text="Δυσκολία:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.difficulty_var = tk.StringVar(value=recipe[3])
        difficulty_combo = ttk.Combobox(main_frame, textvariable=self.difficulty_var,
                                       values=["Εύκολη", "Μέτρια", "Δύσκολη"], width=37)
        difficulty_combo.grid(row=5, column=1, pady=5)
        
        # Χρόνος
        total_minutes = recipe[4]
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Συνολικός Χρόνος:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.hours_spin = ttk.Spinbox(time_frame, from_=0, to=24, width=5)
        self.hours_spin.set(hours)
        self.hours_spin.grid(row=0, column=0)
        ttk.Label(time_frame, text="ώρες").grid(row=0, column=1, padx=5)
        
        self.minutes_spin = ttk.Spinbox(time_frame, from_=0, to=59, width=5)
        self.minutes_spin.set(minutes)
        self.minutes_spin.grid(row=0, column=2)
        ttk.Label(time_frame, text="λεπτά").grid(row=0, column=3, padx=5)
        
        # Υλικά συνταγής
        ttk.Label(main_frame, text="Υλικά Συνταγής", 
                 font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=2, pady=(20, 10))
        
        ingredient_form = ttk.Frame(main_frame)
        ingredient_form.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.ingredient_entry = ttk.Entry(ingredient_form, width=40)
        self.ingredient_entry.grid(row=0, column=0, padx=5)
        self.ingredient_entry.bind('<Return>', lambda e: self.add_recipe_ingredient())

        ttk.Button(ingredient_form, text="Προσθήκη Υλικού",
                  command=self.add_recipe_ingredient).grid(row=0, column=1, padx=5)

        self.ingredients_listbox = tk.Listbox(main_frame, width=50, height=6)
        self.ingredients_listbox.grid(row=9, column=0, columnspan=2, pady=5)

        ttk.Button(main_frame, text="Αφαίρεση Επιλεγμένου Υλικού",
                  command=self.remove_selected_ingredient).grid(row=10, column=0, columnspan=2, pady=5)
        
        # Βήματα
        ttk.Label(main_frame, text="Βήματα Εκτέλεσης", 
                 font=("Arial", 12, "bold")).grid(row=11, column=0, columnspan=2, pady=(20, 10))
        
        step_buttons_frame = ttk.Frame(main_frame)
        step_buttons_frame.grid(row=12, column=0, columnspan=2, pady=5)

        ttk.Button(step_buttons_frame, text="Προσθήκη Βήματος",
                  command=self.add_step_dialog).grid(row=0, column=0, padx=5)
        ttk.Button(step_buttons_frame, text="Επεξεργασία Βήματος",
                  command=self.edit_selected_step).grid(row=0, column=1, padx=5)
        ttk.Button(step_buttons_frame, text="Διαγραφή Βήματος",
                  command=self.delete_selected_step).grid(row=0, column=2, padx=5)

        self.steps_listbox = tk.Listbox(main_frame, width=70, height=10)
        self.steps_listbox.grid(row=13, column=0, columnspan=2, pady=5)
        
        # Κουμπιά
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=14, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Ενημέρωση Βασικών Στοιχείων", 
                  command=self.update_recipe).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Κλείσιμο", 
                  command=self.window.destroy).grid(row=0, column=1, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_details()
    
    def format_time(self, total_minutes):
        """Μετατρέπει λεπτά σε μορφή ώρες και λεπτά"""
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        parts = []
        if hours == 1:
            parts.append("1 ώρα")
        elif hours > 1:
            parts.append(f"{hours} ώρες")
        
        if minutes == 1:
            parts.append("1 λεπτό")
        elif minutes > 1 or total_minutes == 0:
            parts.append(f"{minutes} λεπτά")
        
        return " και ".join(parts) if parts else "0 λεπτά"
    
    def update_recipe(self):
        """Ενημέρωση βασικών στοιχείων συνταγής"""
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        difficulty = self.difficulty_var.get()
        
        if not name or not category:
            messagebox.showerror("Σφάλμα", "Παρακαλώ συμπληρώστε όνομα και κατηγορία")
            return
        
        hours = int(self.hours_spin.get())
        minutes = int(self.minutes_spin.get())
        total_minutes = hours * 60 + minutes
        
        ok, err = update_recipe_basic(self.recipe_id, name, category, difficulty, total_minutes)
        
        if ok:
            messagebox.showinfo("Επιτυχία", "Η συνταγή ενημερώθηκε επιτυχώς")
            self.refresh_details()
            self.callback()
        else:
            messagebox.showerror("Σφάλμα", f"Αποτυχία ενημέρωσης: {err}")

    def refresh_details(self):
        """Ανανεώνει τα στοιχεία της συνταγής από τη βάση"""
        self.details = get_recipe_details(self.recipe_id)
        if not self.details:
            messagebox.showerror("Σφάλμα", "Δεν βρέθηκε η συνταγή")
            self.window.destroy()
            return

        recipe = self.details['recipe']
        self.title_label.config(text=recipe[1])

        self.ingredients_listbox.delete(0, tk.END)
        for ingredient in self.details['recipe_ingredients']:
            self.ingredients_listbox.insert(tk.END, ingredient)

        self.steps_listbox.delete(0, tk.END)
        for step in self.details['steps']:
            ingredients = ", ".join(step['ingredients']) if step['ingredients'] else "χωρίς υλικά"
            step_text = (
                f"Βήμα {step['order']}: {step['title']} | "
                f"{self.format_time(step['minutes'])} | {ingredients}"
            )
            self.steps_listbox.insert(tk.END, step_text)

    def add_recipe_ingredient(self):
        """Προσθέτει υλικό στην υπάρχουσα συνταγή"""
        ingredient = self.ingredient_entry.get().strip()
        if not ingredient:
            return

        add_ingredient_to_recipe(self.recipe_id, ingredient)
        self.ingredient_entry.delete(0, tk.END)
        self.refresh_details()
        self.callback()

    def remove_selected_ingredient(self):
        """Αφαιρεί το επιλεγμένο υλικό από τη συνταγή"""
        selection = self.ingredients_listbox.curselection()
        if not selection:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ επιλέξτε υλικό")
            return

        ingredient = self.ingredients_listbox.get(selection[0])
        remove_ingredient_from_recipe(self.recipe_id, ingredient)
        self.refresh_details()
        self.callback()

    def add_step_dialog(self):
        """Ανοίγει φόρμα για προσθήκη βήματος σε υπάρχουσα συνταγή"""
        StepDialog(self.window, self.add_step_to_recipe)

    def add_step_to_recipe(self, step_data):
        """Αποθηκεύει νέο βήμα στην υπάρχουσα συνταγή"""
        step_id = add_step(
            self.recipe_id,
            step_data['title'],
            step_data['description'],
            step_data['duration']
        )

        for ingredient in step_data['ingredients']:
            add_ingredient_to_step(step_id, ingredient)

        self.refresh_details()
        self.callback()

    def edit_selected_step(self):
        """Ανοίγει φόρμα επεξεργασίας για το επιλεγμένο βήμα"""
        selection = self.steps_listbox.curselection()
        if not selection:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ επιλέξτε βήμα")
            return

        step = self.details['steps'][selection[0]]
        StepDialog(
            self.window,
            lambda step_data: self.update_selected_step(step['step_id'], step_data),
            step_data=step,
            window_title="Επεξεργασία Βήματος",
            button_text="Αποθήκευση Βήματος"
        )

    def update_selected_step(self, step_id, step_data):
        """Ενημερώνει το επιλεγμένο βήμα και τα υλικά του"""
        step_updated = update_step(
            step_id,
            step_data['title'],
            step_data['description'],
            step_data['duration']
        )
        ingredients_updated = replace_step_ingredients(step_id, step_data['ingredients'])

        if step_updated and ingredients_updated:
            self.refresh_details()
            self.callback()
        else:
            messagebox.showerror("Σφάλμα", "Αποτυχία ενημέρωσης βήματος")

    def delete_selected_step(self):
        """Διαγράφει το επιλεγμένο βήμα από τη συνταγή"""
        selection = self.steps_listbox.curselection()
        if not selection:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ επιλέξτε βήμα")
            return

        step = self.details['steps'][selection[0]]
        if not messagebox.askyesno("Επιβεβαίωση", "Να διαγραφεί το επιλεγμένο βήμα;"):
            return

        if delete_step(step['step_id']):
            self.refresh_details()
            self.callback()
        else:
            messagebox.showerror("Σφάλμα", "Αποτυχία διαγραφής βήματος")
