import tkinter as tk
from tkinter import messagebox
import sqlite3
from utils.security import hash_password

def show_register_window(parent_root):
    def register_user():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        conn = sqlite3.connect("task_manager.db")
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                        (username, hash_password(password)))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            win.destroy()
            parent_root.destroy()  # Close main window too
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    win = tk.Toplevel()
    win.title("Register")
    win.geometry("300x200")

    tk.Label(win, text="Username").pack()
    username_entry = tk.Entry(win)
    username_entry.pack()

    tk.Label(win, text="Password").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack()

    tk.Button(win, text="Register", command=register_user).pack(pady=10)
