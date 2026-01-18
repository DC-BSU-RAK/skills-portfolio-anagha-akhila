import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from PIL import Image, ImageTk

# --- yale brand ---
YALE_BLUE = "#00356b"
WHITE = "#ffffff"
YALE_GOLD = "#bd9319"
LIGHT_GRAY = "#f0f0f0"
ACADEMIC_FONT = "Times New Roman"


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class YalePortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Yale University | Student Dashboard")
        self.root.geometry("1150x750")
        self.root.resizable(False, False)
        
        self.students = []
        self.file_path = os.path.join(SCRIPT_DIR, "studentMarks.txt")
        self.load_data()

        # main layout
        self.main_frame = tk.Frame(self.root, bg=WHITE)
        self.main_frame.pack(fill="both", expand=True)

        # sidebar
        self.create_sidebar()
        
        self.content_area = tk.Frame(self.main_frame, bg=WHITE)
        self.content_area.pack(side="right", fill="both", expand=True)
        
        #login screen
        self.show_login_screen()

    def load_data(self):
        """Loads and parses the studentMarks.txt file."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write("10\n1345,John Curry,8,15,7,45\n2345,Sam Sturtivant,14,15,14,77\n9876,Lee Scott,17,11,16,99\n3724,Matt Thompson,19,11,15,81\n1212,Ron Herrema,14,17,18,66\n8439,Jake Hobbs,10,11,10,43\n2344,Jo Hyde,6,15,10,55\n9384,Gareth Southgate,5,6,8,33\n8327,Alan Shearer,20,20,20,100\n2983,Les Ferdinand,15,17,18,92")
        
        self.students = []
        try:
            with open(self.file_path, "r") as f:
                lines = f.readlines()
                for line in lines[1:]:
                    p = line.strip().split(',')
                    if len(p) == 6:
                        self.students.append({
                            "id": p[0], "name": p[1], 
                            "m1": int(p[2]), "m2": int(p[3]), 
                            "m3": int(p[4]), "exam": int(p[5])
                        })
        except Exception as e:
            print(f"Error loading file: {e}")

    def save_to_file(self):
        """Syncs the internal list back to the text file."""
        with open(self.file_path, "w") as f:
            f.write(f"{len(self.students)}\n")
            for s in self.students:
                f.write(f"{s['id']},{s['name']},{s['m1']},{s['m2']},{s['m3']},{s['exam']}\n")

    def calc_stats(self, s):
        """Calculates marks and returns (CW_Total, Exam, Pct, Grade)."""
        cw = s['m1'] + s['m2'] + s['m3']
        total = cw + s['exam']
        # percentage
        pct = (total / 160) * 100
        # grade based on percentage
        if pct >= 70: g = 'A'
        elif pct >= 60: g = 'B'
        elif pct >= 50: g = 'C'
        elif pct >= 40: g = 'D'
        else: g = 'F'
        return cw, s['exam'], round(pct, 2), g

    def create_sidebar(self):
        sidebar = tk.Frame(self.main_frame, bg=YALE_BLUE, width=320)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        canvas = tk.Canvas(sidebar, width=120, height=140, bg=YALE_BLUE, highlightthickness=0)
        canvas.pack(pady=(50, 5))
        canvas.create_polygon(20, 10, 100, 10, 100, 90, 60, 130, 20, 90, fill=WHITE, outline=YALE_GOLD, width=3)
        canvas.create_text(60, 60, text="Y", font=(ACADEMIC_FONT, 55, "bold"), fill=YALE_BLUE)

        tk.Label(sidebar, text="YALE UNIVERSITY", font=(ACADEMIC_FONT, 22, "bold"), fg=WHITE, bg=YALE_BLUE).pack()
        tk.Label(sidebar, text="REGISTRAR'S PORTAL", font=(ACADEMIC_FONT, 10), fg=YALE_GOLD, bg=YALE_BLUE).pack()
        
        tk.Frame(sidebar, bg=YALE_GOLD, height=1, width=200).pack(pady=25)

        self.menu_btns = []
        options = [
            ("Registry Dashboard", self.view_all), 
            ("Performance Analytics", self.view_analytics), 
            ("Enroll New Student", self.add_student_ui), 
            ("Archive Management", self.manage_records_ui)
        ]

        for text, cmd in options:
            btn = tk.Button(sidebar, text=text, font=("Helvetica", 11), fg=WHITE, bg=YALE_BLUE, 
                           activebackground=YALE_GOLD, activeforeground=WHITE, bd=0, 
                           cursor="hand2", pady=15, state="disabled", command=cmd)
            btn.pack(fill="x", padx=35)
            self.menu_btns.append(btn)

        tk.Label(sidebar, text="Lux et Veritas", font=(ACADEMIC_FONT, 12, "italic"), fg=WHITE, bg=YALE_BLUE).pack(side="bottom", pady=30)

    def set_background(self):
        """Properly places the background image so it covers the white area."""
        try:
            bg_path = os.path.join(SCRIPT_DIR, "yale.png")
            img = Image.open(bg_path).resize((830, 750), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            
            # image label
            bg_lbl = tk.Label(self.content_area, image=self.bg_photo)
            bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Background Error: {e}")
            self.content_area.config(bg="#f4f4f4")

    def show_login_screen(self):
        self.clear_content()
        self.set_background()
        
        login_box = tk.Frame(self.content_area, bg=WHITE, padx=50, pady=50, highlightthickness=2, highlightbackground=YALE_BLUE)
        login_box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_box, text="STUDENT DASHBOARD", font=(ACADEMIC_FONT, 24, "bold"), bg=WHITE, fg=YALE_BLUE).pack(pady=(0, 5))
        tk.Label(login_box, text="Authorized Personnel Only", font=("Helvetica", 9), bg=WHITE, fg="gray").pack(pady=(0, 30))
        
        tk.Label(login_box, text="Access Pin:", bg=WHITE, font=("Helvetica", 10, "bold")).pack(anchor="w")
        pass_e = tk.Entry(login_box, width=35, show="*", highlightthickness=1, font=("Arial", 12))
        pass_e.pack(pady=10)

        # password hint
        tk.Label(login_box, text="Hint: Yale foundation year (1701)", font=("Helvetica", 8, "italic"), bg=WHITE, fg="gray").pack(anchor="w")

        def attempt_login():
            if pass_e.get() == "1701":
                for b in self.menu_btns: b.config(state="normal")
                self.view_all()
            else:
                messagebox.showerror("Denied", "The security pin is incorrect.")

        tk.Button(login_box, text="VERIFY & ENTER", bg=YALE_BLUE, fg=WHITE, font=("Helvetica", 10, "bold"), 
                  width=25, pady=10, cursor="hand2", command=attempt_login).pack(pady=30)

    def clear_content(self):
        """Removes existing widgets but keeps the container ready."""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def view_all(self):
        self.clear_content()
        self.set_background()
        overlay = tk.Frame(self.content_area, bg=WHITE, padx=30, pady=30, highlightthickness=1, highlightbackground=LIGHT_GRAY)
        overlay.pack(padx=40, pady=40, fill="both", expand=True)

        tk.Label(overlay, text="STUDENT REGISTRY", font=(ACADEMIC_FONT, 24, "bold"), bg=WHITE, fg=YALE_BLUE).pack()
        
        search_frame = tk.Frame(overlay, bg=WHITE)
        search_frame.pack(fill="x", pady=15)
        tk.Label(search_frame, text="Quick Search:", bg=WHITE, font=("Helvetica", 10, "italic")).pack(side="left")
        search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=search_var, width=50).pack(side="left", padx=10)

        cols = ("ID", "Full Name", "CW Total", "Exam Score", "Grade")
        tree = ttk.Treeview(overlay, columns=cols, show="headings", height=15)
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)

        def update_table(*args):
            tree.delete(*tree.get_children())
            q = search_var.get().lower()
            for s in self.students:
                cw, ex, pct, g = self.calc_stats(s)
                if q in s['name'].lower() or q in s['id']:
                    tree.insert("", "end", values=(s['id'], s['name'], cw, ex, g))
        
        search_var.trace("w", update_table)
        update_table()

    def view_analytics(self):
        self.clear_content()
        self.set_background()
        overlay = tk.Frame(self.content_area, bg=WHITE, padx=40, pady=40)
        overlay.place(relx=0.5, rely=0.5, anchor="center")

        best = max(self.students, key=lambda s: self.calc_stats(s)[2])
        worst = min(self.students, key=lambda s: self.calc_stats(s)[2])
        avg = sum(self.calc_stats(s)[2] for s in self.students) / len(self.students)

        tk.Label(overlay, text="ACADEMIC PERFORMANCE SUMMARY", font=(ACADEMIC_FONT, 24, "bold"), bg=WHITE, fg=YALE_BLUE).pack(pady=20)
        
        stats = [
            ("Highest Performing Student", f"{best['name']} ({self.calc_stats(best)[2]}%)"),
            ("Lowest Performing Student", f"{worst['name']} ({self.calc_stats(worst)[2]}%)"),
            ("Overall Class Average", f"{avg:.2f}%")
        ]

        for title, val in stats:
            f = tk.Frame(overlay, bg=LIGHT_GRAY, pady=15, padx=25)
            f.pack(fill="x", pady=8)
            tk.Label(f, text=title, font=("Helvetica", 11, "bold"), bg=LIGHT_GRAY).pack(side="left")
            tk.Label(f, text=val, font=(ACADEMIC_FONT, 13), bg=LIGHT_GRAY, fg=YALE_BLUE).pack(side="right")

    def add_student_ui(self):
        self.clear_content()
        self.set_background()
        overlay = tk.Frame(self.content_area, bg=WHITE, padx=40, pady=40)
        overlay.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(overlay, text="ENROLL NEW STUDENT", font=(ACADEMIC_FONT, 22, "bold"), bg=WHITE, fg=YALE_BLUE).pack(pady=20)
        
        fields = ["ID Number", "Full Name", "CW 1 (0-20)", "CW 2 (0-20)", "CW 3 (0-20)", "Exam (0-100)"]
        ents = {}
        for f in fields:
            row = tk.Frame(overlay, bg=WHITE)
            row.pack(pady=7)
            tk.Label(row, text=f, width=15, anchor="w", bg=WHITE, font=("Helvetica", 10)).pack(side="left")
            e = tk.Entry(row, width=25, highlightthickness=1)
            e.pack(side="left")
            ents[f] = e

        def save():
            try:
                new_data = {
                    "id": ents["ID Number"].get(), "name": ents["Full Name"].get(), 
                    "m1": int(ents["CW 1 (0-20)"].get()), "m2": int(ents["CW 2 (0-20)"].get()), 
                    "m3": int(ents["CW 3 (0-20)"].get()), "exam": int(ents["Exam (0-100)"].get())
                }
                self.students.append(new_data)
                self.save_to_file()
                messagebox.showinfo("Success", "Student archive updated.")
                self.view_all()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric scores.")

        tk.Button(overlay, text="ARCHIVE RECORD", bg=YALE_BLUE, fg=WHITE, padx=30, pady=10, font=("Helvetica", 10, "bold"), command=save).pack(pady=25)

    def manage_records_ui(self):
        name = simpledialog.askstring("Database Management", "Enter the Full Name of the student record to remove:")
        if name:
            filtered = [s for s in self.students if s['name'].lower() != name.lower()]
            if len(filtered) < len(self.students):
                self.students = filtered
                self.save_to_file()
                self.view_all()
                messagebox.showinfo("Action Complete", f"Records for {name} have been purged.")
            else:
                messagebox.showwarning("Not Found", "No matching student record found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = YalePortal(root)
    root.mainloop()