import tkinter as tk
from tkinter import ttk, messagebox
import database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

# Function to add expense
def add_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()
    description = entry_description.get()

    if not date or not category or not amount or not description:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        amount = float(amount)
        database.add_expense(date, category, amount, description)
        messagebox.showinfo("Success", "Expense added successfully!")
        entry_date.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        load_expenses()
        plot_expenses()  # Update graph
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")

# Function to load expenses into treeview
def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    expenses = database.get_expenses()
    for exp in expenses:
        tree.insert("", "end", values=exp)

# Function to delete an expense
def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Delete Error", "No expense selected!")
        return

    expense_id = tree.item(selected_item, "values")[0]
    database.delete_expense(expense_id)
    messagebox.showinfo("Success", "Expense deleted successfully!")
    load_expenses()
    plot_expenses()  # Update graph

# Function to plot expenses
def plot_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    # Clear previous graph
    for widget in frame_chart.winfo_children():
        widget.destroy()

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(amounts, labels=categories, autopct="%1.1f%%", colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
    ax.set_title("Expense Distribution")

    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Main GUI window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("650x500")
root.configure(bg="#f0f0f0")

# Frames
frame_input = tk.Frame(root, bg="#ffffff", padx=10, pady=10)
frame_input.pack(pady=10, fill="x")

frame_table = tk.Frame(root, bg="#f0f0f0")
frame_table.pack(pady=10)

frame_chart = tk.Frame(root, bg="#ffffff")
frame_chart.pack(pady=10)

# Input fields
tk.Label(frame_input, text="Date (YYYY-MM-DD):", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(frame_input)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Category:", bg="#ffffff").grid(row=1, column=0, padx=5, pady=5)
entry_category = tk.Entry(frame_input)
entry_category.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Amount:", bg="#ffffff").grid(row=2, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_input)
entry_amount.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Description:", bg="#ffffff").grid(row=3, column=0, padx=5, pady=5)
entry_description = tk.Entry(frame_input)
entry_description.grid(row=3, column=1, padx=5, pady=5)

# Buttons
tk.Button(frame_input, text="Add Expense", command=add_expense, bg="#4caf50", fg="white").grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(frame_input, text="Delete Expense", command=delete_expense, bg="#f44336", fg="white").grid(row=5, column=0, columnspan=2, pady=5)

# Expense List (Treeview)
columns = ("ID", "Date", "Category", "Amount", "Description")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack()

# Load existing expenses
load_expenses()
plot_expenses()

# Run the GUI
root.mainloop()
