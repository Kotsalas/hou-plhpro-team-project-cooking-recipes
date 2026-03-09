import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from recipes_service import get_recipe_details, update_recipe_basic


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
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        recipe = self.details['recipe']
        
        # Τίτλος
        ttk.Label(main_frame, text=recipe[1], 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
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
        
        ingredients_text = tk.Text(main_frame, width=50, height=6, state='disabled')
        ingredients_text.grid(row=8, column=0, columnspan=2, pady=5)
        
        if self.details['recipe_ingredients']:
            ingredients_text.config(state='normal')
            for ing in self.details['recipe_ingredients']:
                ingredients_text.insert(tk.END, f"• {ing}\n")
            ingredients_text.config(state='disabled')
        
        # Βήματα
        ttk.Label(main_frame, text="Βήματα Εκτέλεσης", 
                 font=("Arial", 12, "bold")).grid(row=9, column=0, columnspan=2, pady=(20, 10))
        
        steps_text = tk.Text(main_frame, width=50, height=15, state='disabled')
        steps_text.grid(row=10, column=0, columnspan=2, pady=5)
        
        if self.details['steps']:
            steps_text.config(state='normal')
            for step in self.details['steps']:
                steps_text.insert(tk.END, f"Βήμα {step['order']}: {step['title']}\n", "bold")
                steps_text.insert(tk.END, f"Χρόνος: {self.format_time(step['minutes'])}\n")
                if step['ingredients']:
                    steps_text.insert(tk.END, f"Υλικά: {', '.join(step['ingredients'])}\n")
                steps_text.insert(tk.END, f"{step['description']}\n\n")
            steps_text.tag_config("bold", font=("Arial", 10, "bold"))
            steps_text.config(state='disabled')
        
        # Κουμπιά
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=11, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Ενημέρωση Βασικών Στοιχείων", 
                  command=self.update_recipe).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Κλείσιμο", 
                  command=self.window.destroy).grid(row=0, column=1, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
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
            self.callback()
        else:
            messagebox.showerror("Σφάλμα", f"Αποτυχία ενημέρωσης: {err}")
