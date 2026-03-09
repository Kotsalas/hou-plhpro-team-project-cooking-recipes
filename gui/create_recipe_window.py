import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from recipes_service import add_recipe_basic, add_ingredient_to_recipe, add_step, add_ingredient_to_step


class CreateRecipeWindow:
    def __init__(self, parent, callback):
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title("Δημιουργία Νέας Συνταγής")
        self.window.geometry("700x600")
        
        # Λίστες για υλικά και βήματα
        self.recipe_ingredients = []
        self.steps = []
        
        # Canvas με scrollbar
        canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Βασικά στοιχεία συνταγής
        ttk.Label(main_frame, text="Βασικά Στοιχεία Συνταγής", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="Όνομα:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Κατηγορία:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_entry = ttk.Entry(main_frame, width=40)
        self.category_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(main_frame, text="Δυσκολία:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.difficulty_var = tk.StringVar(value="Εύκολη")
        difficulty_combo = ttk.Combobox(main_frame, textvariable=self.difficulty_var, 
                                       values=["Εύκολη", "Μέτρια", "Δύσκολη"], width=37)
        difficulty_combo.grid(row=3, column=1, pady=5)
        
        # Χρόνος
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Συνολικός Χρόνος:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.hours_spin = ttk.Spinbox(time_frame, from_=0, to=24, width=5)
        self.hours_spin.set(0)
        self.hours_spin.grid(row=0, column=0)
        ttk.Label(time_frame, text="ώρες").grid(row=0, column=1, padx=5)
        
        self.minutes_spin = ttk.Spinbox(time_frame, from_=0, to=59, width=5)
        self.minutes_spin.set(0)
        self.minutes_spin.grid(row=0, column=2)
        ttk.Label(time_frame, text="λεπτά").grid(row=0, column=3, padx=5)
        
        # Υλικά συνταγής
        ttk.Label(main_frame, text="Υλικά Συνταγής", 
                 font=("Arial", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=(20, 10))
        
        ing_frame = ttk.Frame(main_frame)
        ing_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.ingredient_entry = ttk.Entry(ing_frame, width=40)
        self.ingredient_entry.grid(row=0, column=0, padx=5)
        self.ingredient_entry.bind('<Return>', lambda e: self.add_ingredient())
        
        ttk.Button(ing_frame, text="Προσθήκη Υλικού", 
                  command=self.add_ingredient).grid(row=0, column=1, padx=5)
        
        # Λίστα υλικών
        self.ingredients_listbox = tk.Listbox(main_frame, height=5, width=50)
        self.ingredients_listbox.grid(row=7, column=0, columnspan=2, pady=5)
        
        ttk.Button(main_frame, text="Αφαίρεση Υλικού", 
                  command=self.remove_ingredient).grid(row=8, column=0, columnspan=2, pady=5)
        
        # Βήματα
        ttk.Label(main_frame, text="Βήματα Εκτέλεσης", 
                 font=("Arial", 12, "bold")).grid(row=9, column=0, columnspan=2, pady=(20, 10))
        
        ttk.Button(main_frame, text="Προσθήκη Βήματος", 
                  command=self.add_step_dialog).grid(row=10, column=0, columnspan=2, pady=5)
        
        # Λίστα βημάτων
        self.steps_listbox = tk.Listbox(main_frame, height=5, width=50)
        self.steps_listbox.grid(row=11, column=0, columnspan=2, pady=5)
        
        ttk.Button(main_frame, text="Αφαίρεση Βήματος", 
                  command=self.remove_step).grid(row=12, column=0, columnspan=2, pady=5)
        
        # Κουμπιά αποθήκευσης
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=13, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Αποθήκευση", 
                  command=self.save_recipe).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Ακύρωση", 
                  command=self.window.destroy).grid(row=0, column=1, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
    
    def add_ingredient(self):
        """Προσθήκη υλικού στη λίστα"""
        ingredient = self.ingredient_entry.get().strip()
        if ingredient:
            self.recipe_ingredients.append(ingredient)
            self.ingredients_listbox.insert(tk.END, ingredient)
            self.ingredient_entry.delete(0, tk.END)
    
    def remove_ingredient(self):
        """Αφαίρεση επιλεγμένου υλικού"""
        selection = self.ingredients_listbox.curselection()
        if selection:
            index = selection[0]
            self.ingredients_listbox.delete(index)
            del self.recipe_ingredients[index]
    
    def add_step_dialog(self):
        """Άνοιγμα διαλόγου για προσθήκη βήματος"""
        StepDialog(self.window, self.add_step_to_list)
    
    def add_step_to_list(self, step_data):
        """Προσθήκη βήματος στη λίστα"""
        self.steps.append(step_data)
        step_text = f"Βήμα {len(self.steps)}: {step_data['title']} ({step_data['duration']} λεπτά)"
        self.steps_listbox.insert(tk.END, step_text)
    
    def remove_step(self):
        """Αφαίρεση επιλεγμένου βήματος"""
        selection = self.steps_listbox.curselection()
        if selection:
            index = selection[0]
            self.steps_listbox.delete(index)
            del self.steps[index]
            # Ανανέωση αρίθμησης
            self.steps_listbox.delete(0, tk.END)
            for i, step in enumerate(self.steps, 1):
                step_text = f"Βήμα {i}: {step['title']} ({step['duration']} λεπτά)"
                self.steps_listbox.insert(tk.END, step_text)
    
    def save_recipe(self):
        """Αποθήκευση συνταγής στη βάση"""
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        difficulty = self.difficulty_var.get()
        
        if not name or not category:
            messagebox.showerror("Σφάλμα", "Παρακαλώ συμπληρώστε όνομα και κατηγορία")
            return
        
        hours = int(self.hours_spin.get())
        minutes = int(self.minutes_spin.get())
        total_minutes = hours * 60 + minutes
        
        # Δημιουργία συνταγής
        recipe_id, created = add_recipe_basic(name, category, difficulty, total_minutes)
        
        # Προσθήκη υλικών
        for ingredient in self.recipe_ingredients:
            add_ingredient_to_recipe(recipe_id, ingredient)
        
        # Προσθήκη βημάτων
        for step in self.steps:
            step_id = add_step(recipe_id, step['title'], step['description'], step['duration'])
            for ingredient in step['ingredients']:
                add_ingredient_to_step(step_id, ingredient)
        
        messagebox.showinfo("Επιτυχία", "Η συνταγή αποθηκεύτηκε επιτυχώς")
        self.callback()
        self.window.destroy()


class StepDialog:
    def __init__(self, parent, callback):
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title("Προσθήκη Βήματος")
        self.window.geometry("500x450")
        
        self.step_ingredients = []
        
        # Canvas με scrollbar
        canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Τίτλος Βήματος:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="Περιγραφή:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.description_text = tk.Text(main_frame, width=40, height=5)
        self.description_text.grid(row=1, column=1, pady=5)
        
        # Χρόνος βήματος
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Χρόνος:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.hours_spin = ttk.Spinbox(time_frame, from_=0, to=24, width=5)
        self.hours_spin.set(0)
        self.hours_spin.grid(row=0, column=0)
        ttk.Label(time_frame, text="ώρες").grid(row=0, column=1, padx=5)
        
        self.minutes_spin = ttk.Spinbox(time_frame, from_=0, to=59, width=5)
        self.minutes_spin.set(0)
        self.minutes_spin.grid(row=0, column=2)
        ttk.Label(time_frame, text="λεπτά").grid(row=0, column=3, padx=5)
        
        # Υλικά βήματος
        ttk.Label(main_frame, text="Υλικά Βήματος:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        ing_frame = ttk.Frame(main_frame)
        ing_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.ingredient_entry = ttk.Entry(ing_frame, width=30)
        self.ingredient_entry.grid(row=0, column=0, padx=5)
        self.ingredient_entry.bind('<Return>', lambda e: self.add_ingredient())
        
        ttk.Button(ing_frame, text="Προσθήκη", 
                  command=self.add_ingredient).grid(row=0, column=1, padx=5)
        
        self.ingredients_listbox = tk.Listbox(main_frame, height=5, width=40)
        self.ingredients_listbox.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Button(main_frame, text="Αφαίρεση", 
                  command=self.remove_ingredient).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Κουμπιά
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Προσθήκη Βήματος", 
                  command=self.save_step).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Ακύρωση", 
                  command=self.window.destroy).grid(row=0, column=1, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_ingredient(self):
        """Προσθήκη υλικού στο βήμα"""
        ingredient = self.ingredient_entry.get().strip()
        if ingredient:
            self.step_ingredients.append(ingredient)
            self.ingredients_listbox.insert(tk.END, ingredient)
            self.ingredient_entry.delete(0, tk.END)
    
    def remove_ingredient(self):
        """Αφαίρεση υλικού από το βήμα"""
        selection = self.ingredients_listbox.curselection()
        if selection:
            index = selection[0]
            self.ingredients_listbox.delete(index)
            del self.step_ingredients[index]
    
    def save_step(self):
        """Αποθήκευση βήματος"""
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε τίτλο βήματος")
            return
        
        hours = int(self.hours_spin.get())
        minutes = int(self.minutes_spin.get())
        duration = hours * 60 + minutes
        
        step_data = {
            'title': title,
            'description': description,
            'duration': duration,
            'ingredients': self.step_ingredients
        }
        
        self.callback(step_data)
        self.window.destroy()
