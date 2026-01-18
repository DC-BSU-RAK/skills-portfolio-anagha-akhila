import tkinter as tk
from tkinter import messagebox
import random
import winsound
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    path1 = os.path.join(BASE_DIR, filename)
    path2 = os.path.join(BASE_DIR, "..", filename)
    
    if os.path.exists(path1):
        return path1
    return path2

class MathMania:
    def __init__(self, root):
        self.root = root
        self.root.title("MATH MANIA")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # game workings
        self.score = 0
        self.question_count = 0
        self.difficulty = ""
        self.attempts = 0

        # background
        try:
            self.bg_img = tk.PhotoImage(file=get_path("background.png"))
            self.bg_label = tk.Label(self.root, image=self.bg_img)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Image Error: {e}")
            self.root.configure(bg="#E0F7FA")

        self.displayMenu()

    # --- FUNCTIONS ---

    def displayMenu(self):
        """Displays the difficulty level menu at the beginning."""
        self.clear_screen()
        
        # title
        tk.Label(self.root, text="MATH MANIA", font=("Arial Black", 55, "bold"), 
                 fg="#006064", bg="white").pack(pady=40)

        # menu
        menu_frame = tk.Frame(self.root, bg="white", bd=8, relief="ridge", padx=40, pady=30)
        menu_frame.pack()

        tk.Label(menu_frame, text="DIFFICULTY LEVEL", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # levels
        tk.Button(menu_frame, text="1. EASY", bg="#A5D6A7", width=20, font=("Arial", 10, "bold"),
                  command=lambda: self.start_quiz("Easy")).pack(pady=5)
        tk.Button(menu_frame, text="2. MODERATE", bg="#81D4FA", width=20, font=("Arial", 10, "bold"),
                  command=lambda: self.start_quiz("Moderate")).pack(pady=5)
        tk.Button(menu_frame, text="3. ADVANCED", bg="#EF9A9A", width=20, font=("Arial", 10, "bold"),
                  command=lambda: self.start_quiz("Advanced")).pack(pady=5)
        
        tk.Button(self.root, text="EXIT GAME", bg="#333", fg="white", font=("Arial", 10),
                  command=self.root.quit).pack(pady=30)

    def randomInt(self):
        """Determines the values based on difficulty."""
        if self.difficulty == "Easy":
            return random.randint(1, 9)
        elif self.difficulty == "Moderate":
            return random.randint(10, 99)
        else: # advanced
            return random.randint(1000, 9999)

    def decideOperation(self):
        """Randomly decides addition or subtraction."""
        return random.choice(['+', '-'])

    def displayProblem(self, problem_text):
        """Displays the question and accepts answer."""
        self.clear_screen()

        # problem container
        box = tk.Frame(self.root, bg="white", bd=3, relief="solid", padx=60, pady=50)
        box.pack(expand=True)

        tk.Label(box, text=f"Question {self.question_count + 1} of 10", bg="white", font=("Arial", 10)).pack()
        tk.Label(box, text=problem_text, font=("Arial", 35, "bold"), bg="white").pack(pady=20)

        self.ans_entry = tk.Entry(box, font=("Arial", 24), justify="center", width=10)
        self.ans_entry.pack(pady=10)
        self.ans_entry.focus_set()

        # submit
        tk.Button(box, text="SUBMIT", bg="#00C853", fg="white", font=("Arial", 12, "bold"),
                  width=15, height=2, command=self.check_logic).pack(pady=20)
        
        # allow 'Enter' key to submit
        self.root.bind('<Return>', lambda event: self.check_logic())

    def isCorrect(self, user_val):
        """Checks correctness and plays sounds."""
        if user_val == self.target_ans:
            self.play_sound("correct.wav")
            points = 10 if self.attempts == 0 else 5
            self.score += points
            messagebox.showinfo("Result", f"Correct! You earned {points} points.")
            return True
        else:
            self.play_sound("wrong.wav")
            return False

    def displayResults(self):
        """Outputs final score and ranking."""
        if self.score >= 90: rank = "A+"
        elif self.score >= 80: rank = "A"
        elif self.score >= 70: rank = "B"
        else: rank = "C"

        result_msg = f"Final Score: {self.score}/100\nRank: {rank}\n\nWould you like to play again?"
        if messagebox.askyesno("Quiz Finished", result_msg):
            self.displayMenu()
        else:
            self.root.quit()

    # --- INTERNAL WORKINGS OF THE GAME ---

    def start_quiz(self, level):
        self.difficulty = level
        self.score = 0
        self.question_count = 0
        self.generate_new_problem()

    def generate_new_problem(self):
        if self.question_count < 10:
            self.attempts = 0
            n1, n2 = self.randomInt(), self.randomInt()
            op = self.decideOperation()
            self.target_ans = n1 + n2 if op == '+' else n1 - n2
            self.displayProblem(f"{n1} {op} {n2} = ?")
        else:
            self.displayResults()

    def check_logic(self):
        try:
            val = int(self.ans_entry.get())
            if self.isCorrect(val):
                self.question_count += 1
                self.generate_new_problem()
            else:
                self.attempts += 1
                if self.attempts < 2:
                    messagebox.showwarning("Incorrect", "Incorrect Answer! One more chance remaining.")
                    self.ans_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Failed", f"Incorrect. The answer was {self.target_ans}")
                    self.question_count += 1
                    self.generate_new_problem()
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number!")

    def play_sound(self, file):
        try:
            path = get_path(file)
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            pass

    def clear_screen(self):
        for widget in self.root.winfo_children():
            if widget != getattr(self, 'bg_label', None):
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathMania(root)
    root.mainloop()