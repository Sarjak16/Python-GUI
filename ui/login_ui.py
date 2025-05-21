import tkinter as tk
from tkinter import messagebox
import sqlite3
from utils.security import verify_password
from ui.dashboard_ui import show_dashboard

def show_login_window(parent_root):
    def login_user():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("task_manager.db")
        cur = conn.cursor()

        cur.execute("SELECT id, password FROM users WHERE username=?", (username,))
        result = cur.fetchone()

        if result and verify_password(password, result[1]):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            win.destroy()
            parent_root.destroy()  # Close main window too
            show_dashboard(result[0])
        else:
            messagebox.showerror("Error", "Invalid credentials")

        conn.close()

    win = tk.Toplevel()
    win.title("Login")
    win.geometry("300x200")

    tk.Label(win, text="Username").pack()
    username_entry = tk.Entry(win)
    username_entry.pack()

    tk.Label(win, text="Password").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack()

    tk.Button(win, text="Login", command=login_user).pack(pady=10)
