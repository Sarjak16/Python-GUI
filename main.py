import tkinter as tk
from db.database import init_db
from ui.register_ui import show_register_window
from ui.login_ui import show_login_window

init_db()


root = tk.Tk()
root.withdraw()  

main_menu = tk.Toplevel()
main_menu.title("Task Manager")
main_menu.geometry("400x300")

tk.Label(main_menu, text="Welcome to Task Manager", font=("Arial", 16)).pack(pady=20)
tk.Button(main_menu, text="Login", command=lambda: show_login_window(main_menu)).pack(pady=10)
tk.Button(main_menu, text="Register", command=lambda: show_register_window(main_menu)).pack(pady=10)

main_menu.protocol("WM_DELETE_WINDOW", root.quit) 
root.mainloop()
