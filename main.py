import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


FILE_NAME = "expenses.json"

expenses = []


def load_data():
    global expenses

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                expenses = json.load(file)
        except:
            expenses = []
    else:
        expenses = []


def save_data():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=4)


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except:
        return False


def add_expense():
    amount_text = entry_amount.get().strip()
    category = entry_category.get().strip()
    date_text = entry_date.get().strip()

    if amount_text == "" or category == "" or date_text == "":
        messagebox.showerror("Ошибка", "Заполните все поля")
        return

    try:
        amount = float(amount_text)
        if amount <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
            return
    except:
        messagebox.showerror("Ошибка", "Сумма должна быть числом")
        return

    if not is_valid_date(date_text):
        messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD")
        return

    expense = {
        "amount": amount,
        "category": category,
        "date": date_text
    }

    expenses.append(expense)
    save_data()
    update_table(expenses)

    entry_amount.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_date.delete(0, tk.END)


def update_table(data):
    for row in tree.get_children():
        tree.delete(row)

    for item in data:
        tree.insert("", tk.END, values=(item["amount"], item["category"], item["date"]))


def filter_expenses():
    filter_category = entry_filter_category.get().strip().lower()
    date_from = entry_date_from.get().strip()
    date_to = entry_date_to.get().strip()

    filtered = []

    for item in expenses:
        ok = True

        if filter_category != "":
            if item["category"].lower() != filter_category:
                ok = False

        item_date = item["date"]

        if date_from != "":
            if not is_valid_date(date_from):
                messagebox.showerror("Ошибка", "Начальная дата введена неправильно")
                return
            if item_date < date_from:
                ok = False

        if date_to != "":
            if not is_valid_date(date_to):
                messagebox.showerror("Ошибка", "Конечная дата введена неправильно")
                return
            if item_date > date_to:
                ok = False

        if ok:
            filtered.append(item)

    update_table(filtered)
    calculate_total(filtered)


def show_all():
    update_table(expenses)
    calculate_total(expenses)


def calculate_total(data):
    total = 0

    for item in data:
        total += float(item["amount"])

    label_total.config(text="Сумма: " + str(total))


root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x600")


frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Сумма").grid(row=0, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_top)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Категория").grid(row=0, column=2, padx=5, pady=5)
entry_category = tk.Entry(frame_top)
entry_category.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_top, text="Дата (YYYY-MM-DD)").grid(row=0, column=4, padx=5, pady=5)
entry_date = tk.Entry(frame_top)
entry_date.grid(row=0, column=5, padx=5, pady=5)

btn_add = tk.Button(frame_top, text="Добавить расход", command=add_expense)
btn_add.grid(row=0, column=6, padx=5, pady=5)


frame_filter = tk.Frame(root)
frame_filter.pack(pady=10)

tk.Label(frame_filter, text="Фильтр по категории").grid(row=0, column=0, padx=5, pady=5)
entry_filter_category = tk.Entry(frame_filter)
entry_filter_category.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_filter, text="Дата с").grid(row=0, column=2, padx=5, pady=5)
entry_date_from = tk.Entry(frame_filter)
entry_date_from.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_filter, text="Дата по").grid(row=0, column=4, padx=5, pady=5)
entry_date_to = tk.Entry(frame_filter)
entry_date_to.grid(row=0, column=5, padx=5, pady=5)

btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=filter_expenses)
btn_filter.grid(row=0, column=6, padx=5, pady=5)

btn_show_all = tk.Button(frame_filter, text="Показать всё", command=show_all)
btn_show_all.grid(row=0, column=7, padx=5, pady=5)


columns = ("amount", "category", "date")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

tree.heading("amount", text="Сумма")
tree.heading("category", text="Категория")
tree.heading("date", text="Дата")

tree.column("amount", width=150)
tree.column("category", width=200)
tree.column("date", width=150)

tree.pack(pady=10)


label_total = tk.Label(root, text="Сумма: 0")
label_total.pack(pady=10)


load_data()
update_table(expenses)
calculate_total(expenses)

root.mainloop()