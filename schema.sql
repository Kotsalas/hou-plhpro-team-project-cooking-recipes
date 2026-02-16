-- Δημιουργία πίνακα συνταγών μαγειρικής
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- μοναδικό αναγνωριστικό για κάθε συνταγή
    name TEXT NOT NULL, -- όνομα της συνταγής
    category TEXT NOT NULL, -- κατηγορία της συνταγής (π.χ. "κυρίως πιάτο", "επιδόρπιο", "σαλάτα")
    difficulty TEXT CHECK(difficulty IN ('εύκολη', 'μέτρια', 'δύσκολη')), -- επίπεδο δυσκολίας της συνταγής
    total_time_minutes INTEGER NOT NULL -- συνολικός χρόνος προετοιμασίας και μαγειρέματος σε λεπτά
);

-- Δημιουργία πίνακα συστατικών
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- μοναδικό αναγνωριστικό για κάθε συστατικό
    recipe_id INTEGER NOT NULL, -- αναφορά στη συνταγή στην οποία ανήκει το συστατικό
    name TEXT NOT NULL, -- όνομα του συστατικού (π.χ. "αλεύρι", "ζάχαρη", "αυγά")
    quantity TEXT, -- ποσότητα του συστατικού (π.χ. "2 φλιτζάνια", "1 κουταλιά της σούπας")
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE -- όταν διαγράφεται μια συνταγή, διαγράφονται και τα συστατικά της
);

-- Δημιουργία πίνακα βημάτων
CREATE TABLE steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- μοναδικό αναγνωριστικό για κάθε βήμα
    recipe_id INTEGER NOT NULL, -- αναφορά στη συνταγή στην οποία ανήκει το βήμα
    step_number INTEGER NOT NULL, -- αριθμός του βήματος (π.χ. 1, 2, 3)
    title TEXT NOT NULL, -- τίτλος του βήματος (π.χ. "Προετοιμασία", "Μαγείρεμα")
    description TEXT NOT NULL, -- περιγραφή του βήματος (π.χ. "Προθερμάνετε το φούρνο στους 180°C", "Ανακατέψτε τα υλικά σε ένα μπολ")
    duration_hours INTEGER DEFAULT 0, -- διάρκεια του βήματος σε ώρες
    duration_minutes INTEGER DEFAULT 0, -- διάρκεια του βήματος σε λεπτά
    ingredients_text TEXT, -- κείμενο που περιγράφει τα συστατικά που χρησιμοποιούνται σε αυτό το βήμα (π.χ. "2 φλιτζάνια αλεύρι, 1 κουταλιά της σούπας ζάχαρη")
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE -- όταν διαγράφεται μια συνταγή, διαγράφονται και τα βήματά της
);