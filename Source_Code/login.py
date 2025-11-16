import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import subprocess
import sys

# ---------- Constants ----------
USERNAME = "admin"   # Default username
PASSWORD = "admin123"  # Default password (you can change it)

# ---------- Functions ----------
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == USERNAME and password == PASSWORD:
        messagebox.showinfo("Login Successful", "Welcome to Institute Inventory System!")
        root.destroy()  # Close login window
        subprocess.run([sys.executable, "main.py"])  # Run main interface
    else:
        messagebox.showerror("Error", "Invalid username or password")

def forgot_password():
    # Ask for recovery key
    key = simpledialog.askstring("Security Check", "Enter security key:")

    if key == "institute123":  # 🔑 You can change this key if you want
        new_pass = simpledialog.askstring("Reset Password", "Enter new password:")

        if new_pass:
            # Update password in database (if exists)
            try:
                conn = sqlite3.connect("inventory.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password=? WHERE username='admin'", (new_pass,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Password reset successfully!")
            except Exception as e:
                messagebox.showwarning("Warning", f"Password reset locally only.\nError: {e}")

            # Update local variable (for temporary login)
            global PASSWORD
            PASSWORD = new_pass
    else:
        messagebox.showerror("Error", "Invalid security key.")

# ---------- Login Window ----------
root = tk.Tk()
root.title("Login - Institute Inventory System")
root.geometry("400x280")
root.config(bg="#E9F2FF")
root.resizable(False, False)

# ---------- UI ----------
tk.Label(root, text="Institute Inventory System", font=("Arial", 16, "bold"), bg="#E9F2FF").pack(pady=15)
tk.Label(root, text="Username:", font=("Arial", 12), bg="#E9F2FF").pack(pady=5)
username_entry = tk.Entry(root, font=("Arial", 12), width=25)
username_entry.pack(pady=5)

tk.Label(root, text="Password:", font=("Arial", 12), bg="#E9F2FF").pack(pady=5)
password_entry = tk.Entry(root, font=("Arial", 12), width=25, show="*")
password_entry.pack(pady=5)

# ---------- Buttons ----------
tk.Button(root, text="Login", font=("Arial", 12), bg="#1976D2", fg="white",
          width=20, command=login).pack(pady=10)

# 🔹 Forgot Password Button
tk.Button(root, text="Forgot Password?", font=("Arial", 10, "underline"),
          bg="#E9F2FF", fg="blue", bd=0, cursor="hand2",
          command=forgot_password).pack(pady=5)

# ---------- Run ----------
root.mainloop()
