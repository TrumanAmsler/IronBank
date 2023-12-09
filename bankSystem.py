import tkinter as tk
from tkinter import ttk, messagebox
import csv

# Global variables
account_number = ""
account_type_var = None
transaction_type_var = None
account_types = ["Savings", "Checkings"]
transaction_types = ["Deposit", "Withdraw"]

def save_data(account_number, account_type, transaction_type, amount):
    data = []
    with open('TheIronBank.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4 and row[0] == account_number and row[1] == account_type:
                # Skip the existing entry for the specified account and account type
                continue
            data.append(row)

    # Add the new entry
    data.append([account_number, account_type, transaction_type, amount])

    # Write the data back to the CSV file, overwriting the previous content
    with open('TheIronBank.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def update_total(total_label):
    selected_account = account_type_var.get()
    total_amount = 0

    with open('TheIronBank.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4 and int(row[0]) == account_number and row[1] == selected_account:
                if row[2] == 'Deposit':
                    total_amount += float(row[3])
                elif row[2] == 'Withdraw':
                    total_amount -= float(row[3])

    total_label.config(text=f'Total Amount: {total_amount:.2f}')

def submit():
    global account_number, account_type_var, transaction_type_var

    account_type = account_type_var.get()
    transaction_type = transaction_type_var.get()
    amount_str = amount_entry.get()

    # Check if the entered account number is an integer
    try:
        int(account_number)
    except ValueError:
        messagebox.showerror("Error", "Account number must be an integer.")
        return

    # Check if the entered amount is a valid float or integer
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number.")
        return

    save_data(account_number, account_type, transaction_type, amount)
    clear_fields()
    update_total(total_label)

def clear_fields():
    amount_entry.delete(0, tk.END)
    account_type_var.set(None)
    transaction_type_var.set(None)

# Initial window for account
def submit_account_number():
    global account_number, account_type_var, transaction_type_var, amount_entry, welcome_label, total_label

    account_number_str = account_number_entry.get()

    # Check if the entered account number is an integer
    try:
        account_number = int(account_number_str)
    except ValueError:
        messagebox.showerror("Error", "Account number must be an integer.")
        return

    if account_number_str and isinstance(account_number, int):
        root_account.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Please enter a valid account number.")

def open_main_window():
    global account_type_var, transaction_type_var, amount_entry, total_label

    # Main GUI setup
    root = tk.Tk()
    root.title("The Iron Bank")
    root.geometry("400x300")
    root.resizable(False, False)

    # Account Type buttons
    tk.Label(root, text="Account Type:").grid(row=0, column=0, padx=10, pady=10)
    account_type_var = tk.StringVar(value=None)
    for i, acc_type in enumerate(account_types):
        acc_button = ttk.Radiobutton(root, text=acc_type, variable=account_type_var, value=acc_type, command=lambda: update_total(total_label))
        acc_button.grid(row=0, column=i+1, padx=10, pady=10)

    # Transaction Type buttons
    tk.Label(root, text="Transaction Type:").grid(row=1, column=0, padx=10, pady=10)
    transaction_type_var = tk.StringVar(value=None)
    for i, trans_type in enumerate(transaction_types):
        trans_button = ttk.Radiobutton(root, text=trans_type, variable=transaction_type_var, value=trans_type, command=lambda: update_total(total_label))
        trans_button.grid(row=1, column=i+1, padx=10, pady=10)

    # Amount
    tk.Label(root, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    # Total Amount Label
    total_label = tk.Label(root, text="Total Amount: 0.00")
    total_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

# sign-in window
root_account = tk.Tk()
root_account.title("Sign In")
root_account.geometry("350x250")
root_account.resizable(False, False)

# Welcome text
welcome_label = tk.Label(root_account, text="WELCOME TO THE IRON BANK", font=("Helvetica", 16, "bold"))
welcome_label.pack(pady=20)

tk.Label(root_account, text="Account Number:").pack(pady=10)
account_number_entry = tk.Entry(root_account)
account_number_entry.pack(pady=10)

submit_account_number_button = tk.Button(root_account, text="Submit", command=submit_account_number)
submit_account_number_button.pack(pady=10)

root_account.mainloop()
