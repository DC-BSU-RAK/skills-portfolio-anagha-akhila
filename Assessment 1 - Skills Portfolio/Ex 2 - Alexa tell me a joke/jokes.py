import tkinter as tk
from tkinter import messagebox
import random
import winsound
import os
import threading 

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_res(filename):
    path = os.path.join(BASE_DIR, filename)
    return path if os.path.exists(path) else None

class JokeMaster3000:
    def __init__(self, root):
        self.root = root
        self.root.title("JOKEMASTER3000")
        self.root.geometry("940x788")
        self.root.resizable(False, False)

        # --- COLORS ---
        self.bg_pink = "#FFD1DC"  
        self.color_title = "#454075"    
        self.color_setup = "#000000"    
        self.color_punch = "#32CD32"    
        self.color_accent = "#FF1493"   
        self.c_blue = "#5CE1E6"
        self.c_red = "#FF5757"
        self.c_yellow = "#FFDE59"

        self.jokes = self.load_jokes()
        
        bg_path = get_res("backgrounds.png") 
        if bg_path:
            self.bg_img = tk.PhotoImage(file=bg_path)
            self.bg_label = tk.Label(self.root, image=self.bg_img)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.start_bg_music()
        self.main_menu()

    def load_jokes(self):
        jokes_list = []
        path = get_res("jokes.txt")
        if path:
            with open(path, "r") as f:
                for line in f:
                    if "?" in line:
                        parts = line.split("?", 1)
                        jokes_list.append((parts[0].strip() + "?", parts[1].strip()))
        return jokes_list

    def start_bg_music(self):
        music_path = get_res("music.wav")
        if music_path:
            winsound.PlaySound(music_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    def play_laugh_and_resume(self):
        laugh_path = get_res("laugh.wav")
        if laugh_path:
            winsound.PlaySound(laugh_path, winsound.SND_FILENAME)
            self.start_bg_music()

    def main_menu(self):
        self.clear()
        
        tk.Label(self.root, text="JOKEMASTER3000", font=("Comic Sans MS", 60, "bold"), 
                 fg=self.color_title, bg=self.bg_pink).pack(pady=(220, 10))
        
        tk.Label(self.root, text="The Ultimate Laugh Machine", font=("Comic Sans MS", 18, "bold"), 
                 fg=self.color_accent, bg=self.bg_pink).pack(pady=10)

        btn_style = {"font": ("Comic Sans MS", 14, "bold"), "width": 25, "height": 2, "bd": 0, "cursor": "hand2"}
        
        tk.Button(self.root, text="ALEXA, TELL ME A JOKE", bg=self.c_blue, fg="white", 
                  activebackground=self.c_blue, command=self.next_joke, **btn_style).pack(pady=15)
        
        tk.Button(self.root, text="QUIT", bg=self.c_red, fg="white", 
                  activebackground=self.c_red, command=self.root.quit, **btn_style).pack(pady=15)

    def next_joke(self):
        self.clear()
        setup, self.punch = random.choice(self.jokes)

        
        tk.Label(self.root, text="READY FOR A LAUGH?", font=("Comic Sans MS", 14, "bold"), 
                 fg=self.color_title, bg=self.bg_pink).pack(pady=(200, 10))
        
        self.setup_label = tk.Label(self.root, text=setup, font=("Comic Sans MS", 22, "bold"), 
                                    fg=self.color_setup, bg=self.bg_pink, wraplength=700)
        self.setup_label.pack(pady=10)

        self.punch_label = tk.Label(self.root, text="", font=("Comic Sans MS", 24, "bold"), 
                                    fg=self.color_punch, bg=self.bg_pink, wraplength=700)
        self.punch_label.pack(pady=10)

        self.star_frame = tk.Frame(self.root, bg=self.bg_pink)
        self.star_frame.pack(pady=10)
        self.stars = []
        for i in range(5):
            s = tk.Button(self.star_frame, text="☆", font=("Arial", 24), bg=self.bg_pink, 
                          fg="#FFD700", relief="flat", activebackground=self.bg_pink,
                          bd=0, command=lambda x=i: self.rate(x))
            s.pack(side="left", padx=2)
            self.stars.append(s)

        self.btn_reveal = tk.Button(self.root, text="SHOW PUNCHLINE", font=("Comic Sans MS", 12, "bold"), 
                                    bg=self.c_blue, fg="white", width=20, bd=0, command=self.reveal)
        self.btn_reveal.pack(pady=10)

        tk.Button(self.root, text="NEXT JOKE ➜", font=("Comic Sans MS", 12, "bold"), 
                  bg=self.c_yellow, fg="black", width=20, bd=0, command=self.next_joke).pack(pady=10)

        
        tk.Button(self.root, text="BACK TO MENU", font=("Comic Sans MS", 10, "bold"), 
                  bg=self.bg_pink, fg=self.color_title, bd=0, command=self.main_menu).pack(pady=15)

    def reveal(self):
        self.punch_label.config(text=self.punch)
        threading.Thread(target=self.play_laugh_and_resume, daemon=True).start()
        self.btn_reveal.config(state="disabled", bg="#CCCCCC")

    def rate(self, index):
        for i, btn in enumerate(self.stars):
            btn.config(text="★" if i <= index else "☆")
        messagebox.showinfo("JokeMaster", f"You rated this {index + 1} stars!")

    def clear(self):
        for w in self.root.winfo_children():
            if w != getattr(self, 'bg_label', None):
                w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeMaster3000(root)
    root.mainloop()