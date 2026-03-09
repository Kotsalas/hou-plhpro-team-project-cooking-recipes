import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Προσθήκη του backend στο path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from recipes_service import search_recipes, get_recipe_details, delete_recipe
from create_recipe_window import CreateRecipeWindow
from recipe_details_window import RecipeDetailsWindow
from execute_recipe_window import ExecuteRecipeWindow


class RecipesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Σύστημα Διαχείρισης Συνταγών")
        self.root.geometry("900x600")
        
        # Κεντρικό frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Τίτλος
        title = ttk.Label(main_frame, text="Σύστημα Διαχείρισης Συνταγών", 
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Frame αναζήτησης
        search_frame = ttk.LabelFrame(main_frame, text="Αναζήτηση Συνταγής", padding="10")
        search_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(search_frame, text="Όνομα ή Κατηγορία:").grid(row=0, column=0, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_recipes())
        
        ttk.Button(search_frame, text="Αναζήτηση", 
                  command=self.search_recipes).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Εμφάνιση Όλων", 
                  command=self.show_all).grid(row=0, column=3, padx=5)
        
        # Πίνακας αποτελεσμάτων
        results_frame = ttk.LabelFrame(main_frame, text="Αποτελέσματα", padding="10")
        results_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Treeview για τα αποτελέσματα
        columns = ("ID", "Όνομα", "Κατηγορία", "Δυσκολία", "Χρόνος")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.column("ID", width=50)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Κουμπιά ενεργειών
        actions_frame = ttk.Frame(main_frame)
        actions_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(actions_frame, text="Νέα Συνταγή", 
                  command=self.create_recipe).grid(row=0, column=0, padx=5)
        ttk.Button(actions_frame, text="Προβολή Λεπτομερειών", 
                  command=self.view_details).grid(row=0, column=1, padx=5)
        ttk.Button(actions_frame, text="Εκτέλεση Συνταγής", 
                  command=self.execute_recipe).grid(row=0, column=2, padx=5)
        ttk.Button(actions_frame, text="Διαγραφή", 
                  command=self.delete_recipe).grid(row=0, column=3, padx=5)
        
        # Ρύθμιση grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Φόρτωση όλων των συνταγών κατά την εκκίνηση
        self.show_all()
    
    def format_time(self, total_minutes):
        """Μετατρέπει λεπτά σε μορφή ώρες και λεπτά"""
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0 and minutes > 0:
            return f"{hours}ω {minutes}λ"
        elif hours > 0:
            return f"{hours}ω"
        else:
            return f"{minutes}λ"
    
    def search_recipes(self):
        """Αναζήτηση συνταγών"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ εισάγετε όρο αναζήτησης")
            return
        
        results = search_recipes(keyword)
        self.display_results(results)
    
    def show_all(self):
        """Εμφάνιση όλων των συνταγών"""
        results = search_recipes("")
        self.display_results(results)
    
    def display_results(self, results):
        """Εμφάνιση αποτελεσμάτων στον πίνακα"""
        # Καθαρισμός υπάρχοντων αποτελεσμάτων
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Προσθήκη νέων αποτελεσμάτων
        for recipe in results:
            recipe_id, name, category, difficulty, total_minutes = recipe
            time_str = self.format_time(total_minutes)
            self.tree.insert("", tk.END, values=(recipe_id, name, category, difficulty, time_str))
    
    def get_selected_recipe_id(self):
        """Επιστρέφει το ID της επιλεγμένης συνταγής"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ επιλέξτε μια συνταγή")
            return None
        
        item = self.tree.item(selection[0])
        return item['values'][0]
    
    def create_recipe(self):
        """Άνοιγμα παραθύρου δημιουργίας συνταγής"""
        CreateRecipeWindow(self.root, self.refresh_results)
    
    def view_details(self):
        """Προβολή λεπτομερειών συνταγής"""
        recipe_id = self.get_selected_recipe_id()
        if recipe_id:
            RecipeDetailsWindow(self.root, recipe_id, self.refresh_results)
    
    def execute_recipe(self):
        """Εκτέλεση συνταγής βήμα-βήμα"""
        recipe_id = self.get_selected_recipe_id()
        if recipe_id:
            ExecuteRecipeWindow(self.root, recipe_id)
    
    def delete_recipe(self):
        """Διαγραφή συνταγής"""
        recipe_id = self.get_selected_recipe_id()
        if not recipe_id:
            return
        
        # Επιβεβαίωση διαγραφής
        if messagebox.askyesno("Επιβεβαίωση", "Είστε σίγουροι ότι θέλετε να διαγράψετε αυτή τη συνταγή;"):
            if delete_recipe(recipe_id):
                messagebox.showinfo("Επιτυχία", "Η συνταγή διαγράφηκε επιτυχώς")
                self.refresh_results()
            else:
                messagebox.showerror("Σφάλμα", "Αποτυχία διαγραφής συνταγής")
    
    def refresh_results(self):
        """Ανανέωση αποτελεσμάτων"""
        self.show_all()


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipesApp(root)
    root.mainloop()
