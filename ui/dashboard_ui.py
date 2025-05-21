import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def show_dashboard(user_id):
    def load_tasks(filter_status=None):
        task_list.delete(0, tk.END)
        conn = sqlite3.connect("task_manager.db")
        cur = conn.cursor()

        query = "SELECT id, title, completed FROM tasks WHERE user_id=?"
        params = [user_id]

        if filter_status == "Completed":
            query += " AND completed=1"
        elif filter_status == "Pending":
            query += " AND completed=0"

        cur.execute(query, params)
        for row in cur.fetchall():
            label = f"{row[0]}. {row[1]} {'✔' if row[2] else ''}"
            task_list.insert(tk.END, label)

        conn.close()

    def add_task():
        title = title_entry.get()
        desc = desc_entry.get()

        if not title:
            messagebox.showwarning("Missing Field", "Please enter a task title.")
            return

        conn = sqlite3.connect("task_manager.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
                    (user_id, title, desc))
        conn.commit()
        conn.close()
        title_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        load_tasks(status_filter.get())

    def delete_task():
        selected = task_list.curselection()
        if not selected:
            return
        task_id = task_list.get(selected[0]).split('.')[0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
        if confirm:
            conn = sqlite3.connect("task_manager.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM tasks WHERE id=? AND user_id=?", (task_id, user_id))
            conn.commit()
            conn.close()
            load_tasks(status_filter.get())
            desc_box.config(state=tk.NORMAL)
            desc_box.delete("1.0", tk.END)
            desc_box.config(state=tk.DISABLED)

    def mark_complete():
        selected = task_list.curselection()
        if not selected:
            return
        task_id = task_list.get(selected[0]).split('.')[0]

        conn = sqlite3.connect("task_manager.db")
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET completed=1 WHERE id=? AND user_id=?", (task_id, user_id))
        conn.commit()
        conn.close()
        load_tasks(status_filter.get())

    def edit_task():
        selected = task_list.curselection()
        if not selected:
            return
        task_id = task_list.get(selected[0]).split('.')[0]

        new_title = title_entry.get()
        new_desc = desc_entry.get()

        if not new_title:
            messagebox.showwarning("Missing Field", "Task title cannot be empty.")
            return

        conn = sqlite3.connect("task_manager.db")
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET title=?, description=? WHERE id=? AND user_id=?",
                    (new_title, new_desc, task_id, user_id))
        conn.commit()
        conn.close()
        load_tasks(status_filter.get())

    def on_task_select(event):
        selected = task_list.curselection()
        if selected:
            task_id = task_list.get(selected[0]).split('.')[0]
            conn = sqlite3.connect("task_manager.db")
            cur = conn.cursor()
            cur.execute("SELECT title, description FROM tasks WHERE id=? AND user_id=?", (task_id, user_id))
            row = cur.fetchone()
            conn.close()
            if row:
                title_entry.delete(0, tk.END)
                title_entry.insert(0, row[0])
                desc_entry.delete(0, tk.END)
                desc_entry.insert(0, row[1])

                # Show description below
                desc_box.config(state=tk.NORMAL)
                desc_box.delete("1.0", tk.END)
                desc_box.insert(tk.END, row[1])
                desc_box.config(state=tk.DISABLED)

    # Window setup
    win = tk.Toplevel()
    win.title("Your Tasks")
    win.geometry("500x600")
    win.resizable(False, False)

    tk.Label(win, text="Title:", anchor="w").pack(fill=tk.X, padx=10, pady=(10, 0))
    title_entry = tk.Entry(win)
    title_entry.pack(fill=tk.X, padx=10)

    tk.Label(win, text="Description:", anchor="w").pack(fill=tk.X, padx=10, pady=(10, 0))
    desc_entry = tk.Entry(win)
    desc_entry.pack(fill=tk.X, padx=10)

    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Task", width=15, command=add_task).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Edit Task", width=15, command=edit_task).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Mark as Completed", width=20, command=mark_complete).grid(row=1, column=0, columnspan=2, pady=5)

    tk.Label(win, text="Filter:", anchor="w").pack(fill=tk.X, padx=10, pady=(5, 0))
    status_filter = ttk.Combobox(win, values=["All", "Pending", "Completed"])
    status_filter.current(0)
    status_filter.pack(fill=tk.X, padx=10)
    status_filter.bind("<<ComboboxSelected>>", lambda e: load_tasks(status_filter.get()))

    task_list = tk.Listbox(win, height=10)
    task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
    task_list.bind("<<ListboxSelect>>", on_task_select)

    tk.Button(win, text="Delete Selected Task", command=delete_task).pack(pady=10)

    tk.Label(win, text="Selected Task Description:", anchor="w").pack(fill=tk.X, padx=10)
    desc_box = tk.Text(win, height=5, wrap="word")
    desc_box.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0, 10))
    desc_box.config(state=tk.DISABLED)

    load_tasks()
