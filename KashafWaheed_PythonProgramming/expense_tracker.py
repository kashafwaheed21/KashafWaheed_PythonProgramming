import customtkinter as ctk
import pandas as pd
import os
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# ---------------- Appearance ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- Window ----------------
app = ctk.CTk()
app.title("💰 Personal Expense Tracker Pro")
app.geometry("1000x700")
app.resizable(False, False)

CSV_FILE = "transactions.csv"

# ---------------- Create CSV ----------------
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(
        columns=[
            "Date",
            "Type",
            "Category",
            "Description",
            "Amount"
        ]
    )
    df.to_csv(CSV_FILE, index=False)

# ---------------- Variables ----------------
type_var = ctk.StringVar(value="Expense")
category_var = ctk.StringVar(value="Food")

# ---------------- Header ----------------
header = ctk.CTkFrame(app, corner_radius=0, height=80)
header.pack(fill="x")

title = ctk.CTkLabel(
    header,
    text="💰 Personal Expense Tracker Pro",
    font=("Arial",30,"bold")
)
title.pack(pady=20)

# ---------------- Summary Cards ----------------
cards = ctk.CTkFrame(app, fg_color="transparent")
cards.pack(pady=20)

income_card = ctk.CTkFrame(cards, width=220, height=100)
income_card.grid(row=0,column=0,padx=15)

expense_card = ctk.CTkFrame(cards, width=220, height=100)
expense_card.grid(row=0,column=1,padx=15)

balance_card = ctk.CTkFrame(cards, width=220, height=100)
balance_card.grid(row=0,column=2,padx=15)

income_title = ctk.CTkLabel(
    income_card,
    text="💵 Total Income",
    font=("Arial",18,"bold")
)
income_title.pack(pady=(15,5))

income_value = ctk.CTkLabel(
    income_card,
    text="Rs 0",
    font=("Arial",24,"bold"),
    text_color="green"
)
income_value.pack()

expense_title = ctk.CTkLabel(
    expense_card,
    text="💸 Total Expense",
    font=("Arial",18,"bold")
)
expense_title.pack(pady=(15,5))

expense_value = ctk.CTkLabel(
    expense_card,
    text="Rs 0",
    font=("Arial",24,"bold"),
    text_color="red"
)
expense_value.pack()

balance_title = ctk.CTkLabel(
    balance_card,
    text="💳 Balance",
    font=("Arial",18,"bold")
)
balance_title.pack(pady=(15,5))

balance_value = ctk.CTkLabel(
    balance_card,
    text="Rs 0",
    font=("Arial",24,"bold"),
    text_color="cyan"
)
balance_value.pack()

# ---------------- Input Section ----------------
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(
    input_frame,
    text="Type"
).grid(row=0,column=0,padx=10,pady=10)

type_menu = ctk.CTkOptionMenu(
    input_frame,
    values=["Income","Expense"],
    variable=type_var
)
type_menu.grid(row=0,column=1)

ctk.CTkLabel(
    input_frame,
    text="Category"
).grid(row=0,column=2,padx=10)

category_menu = ctk.CTkOptionMenu(
    input_frame,
    values=[
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Salary",
        "Other"
    ],
    variable=category_var
)
category_menu.grid(row=0,column=3)

ctk.CTkLabel(
    input_frame,
    text="Description"
).grid(row=1,column=0,padx=10,pady=15)

description_entry = ctk.CTkEntry(
    input_frame,
    width=220
)
description_entry.grid(row=1,column=1)

ctk.CTkLabel(
    input_frame,
    text="Amount"
).grid(row=1,column=2)

amount_entry = ctk.CTkEntry(
    input_frame,
    width=150
)
amount_entry.grid(row=1,column=3)

def update_summary():

    df = pd.read_csv(CSV_FILE)

    income = df[df["Type"] == "Income"]["Amount"].sum()

    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    balance = income - expense

    income_value.configure(text=f"Rs {income:.2f}")

    expense_value.configure(text=f"Rs {expense:.2f}")

    balance_value.configure(text=f"Rs {balance:.2f}")


def load_transactions():

    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        df = pd.DataFrame(columns=[
            "Date",
            "Type",
            "Category",
            "Description",
            "Amount"
        ])
        df.to_csv(CSV_FILE, index=False)

    for item in tree.get_children():
        tree.delete(item)

    df = pd.read_csv(CSV_FILE)

    for _, row in df.iterrows():
        tree.insert(
            "",
            "end",
            values=(
                row["Date"],
                row["Type"],
                row["Category"],
                row["Description"],
                row["Amount"]
            )
        )

    update_summary()

def add_transaction():

    description = description_entry.get().strip()

    amount = amount_entry.get().strip()

    if description == "" or amount == "":

        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )

        return

    try:

        amount = float(amount)

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Enter a valid number."
        )

        return

    today = datetime.now().strftime("%d-%m-%Y")

    new_data = pd.DataFrame([{

        "Date": today,

        "Type": type_var.get(),

        "Category": category_var.get(),

        "Description": description,

        "Amount": amount

    }])

    new_data.to_csv(
        CSV_FILE,
        mode="a",
        header=False,
        index=False
    )

    description_entry.delete(0, "end")

    amount_entry.delete(0, "end")

    load_transactions()

    messagebox.showinfo(
        "Success",
        "Transaction Added Successfully!"
    )

def delete_transaction():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select a transaction."
        )
        return

    item = tree.item(selected[0])

    values = item["values"]

    df = pd.read_csv(CSV_FILE)

    df = df[
        ~(
            (df["Date"] == values[0]) &
            (df["Type"] == values[1]) &
            (df["Category"] == values[2]) &
            (df["Description"] == values[3]) &
            (df["Amount"] == float(values[4]))
        )
    ]

    df.to_csv(CSV_FILE, index=False)

    load_transactions()

    messagebox.showinfo(
        "Deleted",
        "Transaction deleted successfully!"
    )
def clear_transactions():

    answer = messagebox.askyesno(
        "Clear All",
        "Delete all transactions?"
    )

    if answer:

        df = pd.DataFrame(
            columns=[
                "Date",
                "Type",
                "Category",
                "Description",
                "Amount"
            ]
        )

        df.to_csv(CSV_FILE, index=False)

        load_transactions()
def show_chart():

    df = pd.read_csv(CSV_FILE)

    expense_df = df[df["Type"] == "Expense"]

    if expense_df.empty:
        messagebox.showinfo(
            "No Data",
            "No expense data available."
        )
        return

    category_data = expense_df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(6,6))

    plt.pie(
        category_data,
        labels=category_data.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Expense Distribution by Category")

    plt.axis("equal")

    plt.show()
# ---------------- Buttons ----------------
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=15)

add_button = ctk.CTkButton(
    button_frame,
    text="➕ Add Transaction",
    width=170,
    command=add_transaction
)
add_button.grid(row=0,column=0,padx=10)

delete_button = ctk.CTkButton(
    button_frame,
    text="🗑 Delete",
    width=130,
    command=delete_transaction

)
delete_button.grid(row=0,column=1,padx=10)

clear_button = ctk.CTkButton(
    button_frame,
    text="🧹 Clear All",
    width=130,
    command=clear_transactions

)
clear_button.grid(row=0,column=2,padx=10)

exit_button = ctk.CTkButton(
    button_frame,
    text="❌ Exit",
    width=130,
    fg_color="red",
    hover_color="#8B0000",
    command=app.destroy
)
chart_button = ctk.CTkButton(
    button_frame,
    text="📊 Show Chart",
    width=150,
    command=show_chart
)

chart_button.grid(row=0, column=3, padx=10)

exit_button.grid(row=0,column=4,padx=10)

# ---------------- Table ----------------
table_frame = ctk.CTkFrame(app)
table_frame.pack(fill="both", expand=True, padx=20, pady=20)

columns = (
    "Date",
    "Type",
    "Category",
    "Description",
    "Amount"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)
style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    rowheight=28,
    font=("Arial", 11)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 12, "bold")
)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=170, anchor="center")

tree.pack(fill="both", expand=True)

load_transactions()

app.mainloop()