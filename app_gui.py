import tkinter as tk
from tkinter import messagebox

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("CoD BoT")
        self.is_running = False
        self.is_paused = False
        self.create_widgets()

    def create_widgets(self):
        self.start_btn = tk.Button(self.root, text="Start", command=self.start_app, width=10)
        self.start_btn.pack(pady=10)

        self.pause_btn = tk.Button(self.root, text="Pause", command=self.pause_app, width=10, state=tk.DISABLED)
        self.pause_btn.pack(pady=10)

        self.end_btn = tk.Button(self.root, text="End", command=self.end_app, width=10, state=tk.DISABLED)
        self.end_btn.pack(pady=10)

    def start_app(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.end_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Info", "App Started!")

    def pause_app(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_btn.config(text="Resume")
            messagebox.showinfo("Info", "App Paused!")
        elif self.is_running and self.is_paused:
            self.is_paused = False
            self.pause_btn.config(text="Pause")
            messagebox.showinfo("Info", "App Resumed!")

    def end_app(self):
        if self.is_running:
            self.is_running = False
            self.is_paused = False
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED, text="Pause")
            self.end_btn.config(state=tk.DISABLED)
            messagebox.showinfo("Info", "App Ended!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()
