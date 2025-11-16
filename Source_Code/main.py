import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from report import generate_pdf_report, generate_excel_report

# ================= DATABASE =====================
def connect_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''CREAT
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    quantity INTEGER,
                    price REAL,
                    condition TEXT,
                    location TEXT,
                    date_added TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    conn.commit()
    conn.close()


connect_db()

# ================= ROOT WINDOW =====================
root = tk.Tk()
root.title("Institute Inventory Dashboard")
root.geometry("1000x600")
root.minsize(900, 550)  # allows maximizing and resizing
root.configure(bg="#E8F0FE")

# ================= HEADER =====================
header_frame = tk.Frame(root, bg="#1565C0", height=60)
header_frame.pack(fill=tk.X)

tk.Label(header_frame, text="Institute Inventory Dashboard",
         fg="white", bg="#1565C0", font=("Arial Rounded MT Bold", 20)).pack(side=tk.LEFT, padx=20, pady=10)

# ================= MAIN DASHBOARD FRAME =====================
main_frame = tk.Frame(root, bg="#E8F0FE", padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# ================= CONTROL BUTTONS =====================
button_frame = tk.Frame(main_frame, bg="#E8F0FE")
button_frame.pack(fill=tk.X, pady=5)

style = {"font": ("Arial", 10, "bold"), "bg": "#1976D2", "fg": "white", "width": 15}

tk.Button(button_frame, text="Add Item", command=lambda: add_item_window(), **style).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Item", command=lambda: update_item_window(), **style).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Item", command=lambda: delete_item(), **style).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Generate PDF", command=generate_pdf_report, **style).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Generate Excel", command=generate_excel_report, **style).grid(row=0, column=4, padx=5)

# ================= TABLE =====================
tree_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Quantity", "Price", "Condition", "Location", "Date Added"),
                    show="headings", height=12)

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

tree.pack(fill=tk.BOTH, expand=True)

# ================= DATABASE FUNCTIONS =====================
def fetch_data():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    conn.close()

    for i in tree.get_children():
        tree.delete(i)
    for row in rows:
        tree.insert("", tk.END, values=row)


fetch_data()

# ================= ITEM MANAGEMENT WINDOWS =====================
def add_item_window():
    win = tk.Toplevel(root)
    win.title("Add Inventory Item")
    win.geometry("400x350")
    win.configure(bg="#E8F0FE")

    fields = ["Name", "Quantity", "Price", "Condition", "Location"]
    entries = {}

    for i, f in enumerate(fields):
        tk.Label(win, text=f+":", bg="#E8F0FE").grid(row=i, column=0, padx=10, pady=10, sticky="w")
        e = tk.Entry(win, width=25)
        e.grid(row=i, column=1, padx=10)
        entries[f] = e

    def save_item():
        vals = [entries[f].get() for f in fields]
        if not all(vals[:3]):
            messagebox.showerror("Error", "Name, Quantity, and Price are required.")
            return
        conn = sqlite3.connect("inventory.db")
        c = conn.cursor()
        c.execute("INSERT INTO inventory (name, quantity, price, condition, location, date_added) VALUES (?, ?, ?, ?, ?, DATE('now'))",
                  vals)
        conn.commit()
        conn.close()
        fetch_data()
        win.destroy()
        messagebox.showinfo("Added", "Item added successfully!")

    tk.Button(win, text="Save Item", bg="#1976D2", fg="white", width=15, command=save_item).grid(row=len(fields), column=1, pady=20)


def update_item_window():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select an item to update.")
        return
    values = tree.item(selected, "values")
    win = tk.Toplevel(root)
    win.title("Update Item")
    win.geometry("400x350")
    win.configure(bg="#E8F0FE")

    fields = ["Name", "Quantity", "Price", "Condition", "Location"]
    entries = {}

    for i, f in enumerate(fields):
        tk.Label(win, text=f+":", bg="#E8F0FE").grid(row=i, column=0, padx=10, pady=10, sticky="w")
        e = tk.Entry(win, width=25)
        e.insert(0, values[i+1])
        e.grid(row=i, column=1, padx=10)
        entries[f] = e

    def save_update():
        conn = sqlite3.connect("inventory.db")
        c = conn.cursor()
        c.execute("""UPDATE inventory SET name=?, quantity=?, price=?, condition=?, location=? WHERE id=?""",
                  (entries["Name"].get(), entries["Quantity"].get(), entries["Price"].get(),
                   entries["Condition"].get(), entries["Location"].get(), values[0]))
        conn.commit()
        conn.close()
        fetch_data()
        win.destroy()
        messagebox.showinfo("Updated", "Item updated successfully!")

    tk.Button(win, text="Update Item", bg="#1976D2", fg="white", width=15, command=save_update).grid(row=len(fields), column=1, pady=20)


def delete_item():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select an item to delete.")
        return
    values = tree.item(selected, "values")
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id=?", (values[0],))
    conn.commit()
    conn.close()
    fetch_data()
    messagebox.showinfo("Deleted", "Item deleted successfully!")

# ================== MENU BAR =====================
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

report_menu = tk.Menu(menu_bar, tearoff=0)
report_menu.add_command(label="Generate PDF", command=generate_pdf_report)
report_menu.add_command(label="Generate Excel", command=generate_excel_report)
menu_bar.add_cascade(label="Reports", menu=report_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)

def change_password_window():
    win = tk.Toplevel(root)
    win.title("Change Password")
    win.geometry("300x230")
    win.resizable(False, False)
    win.configure(bg="#E8F0FE")

    tk.Label(win, text="Username:", bg="#E8F0FE").pack(pady=5)
    username_entry = tk.Entry(win)
    username_entry.pack()

    tk.Label(win, text="Old Password:", bg="#E8F0FE").pack(pady=5)
    old_pass_entry = tk.Entry(win, show="*")
    old_pass_entry.pack()

    tk.Label(win, text="New Password:", bg="#E8F0FE").pack(pady=5)
    new_pass_entry = tk.Entry(win, show="*")
    new_pass_entry.pack()

    tk.Label(win, text="Confirm New Password:", bg="#E8F0FE").pack(pady=5)
    confirm_pass_entry = tk.Entry(win, show="*")
    confirm_pass_entry.pack()

    def update_password():
        username = username_entry.get().strip()
        old_pass = old_pass_entry.get().strip()
        new_pass = new_pass_entry.get().strip()
        confirm_pass = confirm_pass_entry.get().strip()

        if not all([username, old_pass, new_pass, confirm_pass]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New passwords do not match!")
            return

        conn = sqlite3.connect("inventory.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, old_pass))
        user = c.fetchone()

        if user:
            c.execute("UPDATE users SET password=? WHERE username=?", (new_pass, username))
            conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or old password!")

        conn.close()

    tk.Button(win, text="Update Password", bg="#1976D2", fg="white", command=update_password).pack(pady=10)


def show_about():
    messagebox.showinfo("About", "Institute Inventory Dashboard\nVersion 2.0\nDeveloped by Noman Shafi")

help_menu.add_command(label="Change Password", command=change_password_window)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# ================= RUN APP =====================
root.state('zoomed')  # start maximized automatically
root.mainloop()
