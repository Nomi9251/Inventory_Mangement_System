import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
from datetime import datetime
from tkinter import messagebox

# ---------- Generate PDF Report ----------
def generate_pdf_report():
    try:
        conn = sqlite3.connect("inventory.db")
        c = conn.cursor()
        c.execute("SELECT * FROM inventory")
        data = c.fetchall()
        conn.close()

        if not data:
            messagebox.showwarning("No Data", "No items found in the inventory to generate report.")
            return

        pdf_file = f"Inventory_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf = canvas.Canvas(pdf_file, pagesize=letter)
        pdf.setTitle("Inventory Report")

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(220, 750, "Inventory Report")

        # Add current date
        pdf.setFont("Helvetica", 12)
        pdf.drawString(400, 730, f"Date: {datetime.now().strftime('%d-%m-%Y')}")

        # Table headers
        headers = ["ID", "Name", "Qty", "Price", "Condition", "Location", "Date Added"]
        y = 700
        pdf.setFont("Helvetica-Bold", 10)
        for i, header in enumerate(headers):
            pdf.drawString(50 + i * 70, y, header)

        # Table data
        y -= 20
        pdf.setFont("Helvetica", 9)
        for row in data:
            for i, value in enumerate(row):
                pdf.drawString(50 + i * 70, y, str(value))
            y -= 15
            if y < 50:  # Add new page if space ends
                pdf.showPage()
                y = 750
                pdf.setFont("Helvetica", 9)

        pdf.save()
        messagebox.showinfo("Success", f"PDF report generated successfully:\n{pdf_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDF report.\n{e}")

# ---------- Generate Excel Report ----------
def generate_excel_report():
    try:
        conn = sqlite3.connect("inventory.db")
        df = pd.read_sql_query("SELECT * FROM inventory", conn)
        conn.close()

        if df.empty:
            messagebox.showwarning("No Data", "No items found in the inventory to export.")
            return

        file_name = f"Inventory_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(file_name, index=False)
        messagebox.showinfo("Success", f"Excel report generated successfully:\n{file_name}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate Excel report.\n{e}")
