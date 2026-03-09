import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from recipes_service import get_recipe_details


class ExecuteRecipeWindow:
    def __init__(self, parent, recipe_id):
        self.recipe_id = recipe_id
        self.details = get_recipe_details(recipe_id)
        
        if not self.details:
            messagebox.showerror("Σφάλμα", "Δεν βρέθηκε η συνταγή")
            return
        
        self.recipe = self.details['recipe']
        self.steps = self.details['steps']
        self.current_step = 0
        self.completed_minutes = 0
        self.total_minutes = self.recipe[4]
        
        if not self.steps:
            messagebox.showinfo("Πληροφορία", "Η συνταγή δεν έχει βήματα")
            return
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Εκτέλεση: {self.recipe[1]}")
        self.window.geometry("600x500")
        
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Τίτλος συνταγής
        ttk.Label(main_frame, text=self.recipe[1], 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        
        ttk.Label(main_frame, text=f"Συνολικός χρόνος: {self.format_time(self.total_minutes)}", 
                 font=("Arial", 10)).grid(row=1, column=0, columnspan=3, pady=5)
        
        # Progress bar
        ttk.Label(main_frame, text="Πρόοδος:", 
                 font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=10)
        
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(main_frame, length=400, mode='determinate', 
                                           variable=self.progress_var)
        self.progress_bar.grid(row=2, column=1, pady=10, padx=10)
        
        self.progress_label = ttk.Label(main_frame, text="0%", font=("Arial", 10, "bold"))
        self.progress_label.grid(row=2, column=2, pady=10)
        
        # Πληροφορίες βήματος
        step_frame = ttk.LabelFrame(main_frame, text="Τρέχον Βήμα", padding="10")
        step_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.step_title = ttk.Label(step_frame, text="", font=("Arial", 12, "bold"))
        self.step_title.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.step_time = ttk.Label(step_frame, text="", font=("Arial", 10))
        self.step_time.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(step_frame, text="Υλικά:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.step_ingredients = tk.Text(step_frame, width=50, height=4, state='disabled')
        self.step_ingredients.grid(row=3, column=0, pady=5)
        
        ttk.Label(step_frame, text="Περιγραφή:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.step_description = tk.Text(step_frame, width=50, height=6, state='disabled', wrap=tk.WORD)
        self.step_description.grid(row=5, column=0, pady=5)
        
        # Κουμπιά πλοήγησης
        nav_frame = ttk.Frame(main_frame)
        nav_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.prev_button = ttk.Button(nav_frame, text="← Προηγούμενο", 
                                      command=self.previous_step)
        self.prev_button.grid(row=0, column=0, padx=10)
        
        self.next_button = ttk.Button(nav_frame, text="Επόμενο →", 
                                      command=self.next_step)
        self.next_button.grid(row=0, column=1, padx=10)
        
        ttk.Button(nav_frame, text="Κλείσιμο", 
                  command=self.window.destroy).grid(row=0, column=2, padx=10)
        
        # Ρύθμιση grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Εμφάνιση πρώτου βήματος
        self.display_current_step()
    
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
    
    def calculate_progress(self):
        """Υπολογισμός προόδου με βάση τον χρόνο"""
        if self.total_minutes > 0:
            return int((self.completed_minutes / self.total_minutes) * 100)
        return 0
    
    def display_current_step(self):
        """Εμφάνιση τρέχοντος βήματος"""
        step = self.steps[self.current_step]
        
        # Ενημέρωση τίτλου
        self.step_title.config(text=f"Βήμα {step['order']}: {step['title']}")
        
        # Ενημέρωση χρόνου
        self.step_time.config(text=f"Χρόνος: {self.format_time(step['minutes'])}")
        
        # Ενημέρωση υλικών
        self.step_ingredients.config(state='normal')
        self.step_ingredients.delete("1.0", tk.END)
        if step['ingredients']:
            for ing in step['ingredients']:
                self.step_ingredients.insert(tk.END, f"• {ing}\n")
        else:
            self.step_ingredients.insert(tk.END, "(κανένα υλικό)")
        self.step_ingredients.config(state='disabled')
        
        # Ενημέρωση περιγραφής
        self.step_description.config(state='normal')
        self.step_description.delete("1.0", tk.END)
        self.step_description.insert(tk.END, step['description'])
        self.step_description.config(state='disabled')
        
        # Ενημέρωση προόδου
        progress = self.calculate_progress()
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{progress}%")
        
        # Ενημέρωση κουμπιών
        self.prev_button.config(state='normal' if self.current_step > 0 else 'disabled')
        
        if self.current_step < len(self.steps) - 1:
            self.next_button.config(text="Επόμενο →")
        else:
            self.next_button.config(text="Ολοκλήρωση")
    
    def next_step(self):
        """Μετάβαση στο επόμενο βήμα"""
        if self.current_step < len(self.steps) - 1:
            # Προσθήκη χρόνου τρέχοντος βήματος
            self.completed_minutes += self.steps[self.current_step]['minutes']
            self.current_step += 1
            self.display_current_step()
        else:
            # Τελευταίο βήμα - ολοκλήρωση
            self.completed_minutes = self.total_minutes
            self.progress_var.set(100)
            self.progress_label.config(text="100%")
            messagebox.showinfo("Ολοκλήρωση", 
                              f"Συγχαρητήρια! Ολοκληρώσατε τη συνταγή '{self.recipe[1]}'!")
            self.window.destroy()
    
    def previous_step(self):
        """Επιστροφή στο προηγούμενο βήμα"""
        if self.current_step > 0:
            self.current_step -= 1
            # Αφαίρεση χρόνου τρέχοντος βήματος
            self.completed_minutes -= self.steps[self.current_step]['minutes']
            self.display_current_step()
