import tkinter as tk
from tkinter import messagebox, ttk
from mysql.connector import connect

mydb = connect(host="localhost", user="root", passwd="12345", database="library")
mycursor = mydb.cursor()

root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")
root.configure(bg="#f7f7f7")

def create_account():
    def save_account():
        cardno = entry_cardno.get()
        name = entry_name.get()
        phone = entry_phone.get()
        address = entry_address.get()
        dob = entry_dob.get()
        try:
            mycursor.execute(
                "INSERT INTO library_master (cardno, name_of_person, phone_no, address, dob) VALUES (%s, %s, %s, %s, %s)",
                (cardno, name, phone, address, dob),
            )
            mydb.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            new_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    new_window = tk.Toplevel(root)
    new_window.title("Create Account")
    new_window.geometry("400x400")
    new_window.configure(bg="#e6f7ff")

    tk.Label(new_window, text="Create Account", font=("Arial", 16), bg="#e6f7ff").pack(pady=10)
    tk.Label(new_window, text="Card Number:", bg="#e6f7ff").pack(pady=5)
    entry_cardno = tk.Entry(new_window, font=("Arial", 12))
    entry_cardno.pack(pady=5)
    tk.Label(new_window, text="Name:", bg="#e6f7ff").pack(pady=5)
    entry_name = tk.Entry(new_window, font=("Arial", 12))
    entry_name.pack(pady=5)
    tk.Label(new_window, text="Phone Number:", bg="#e6f7ff").pack(pady=5)
    entry_phone = tk.Entry(new_window, font=("Arial", 12))
    entry_phone.pack(pady=5)
    tk.Label(new_window, text="Address:", bg="#e6f7ff").pack(pady=5)
    entry_address = tk.Entry(new_window, font=("Arial", 12))
    entry_address.pack(pady=5)
    tk.Label(new_window, text="Date of Birth:", bg="#e6f7ff").pack(pady=5)
    entry_dob = tk.Entry(new_window, font=("Arial", 12))
    entry_dob.pack(pady=5)
    tk.Button(new_window, text="Save", command=save_account, font=("Arial", 12), bg="#007BFF", fg="white", width=10).pack(pady=20)

def update_account():
    def save_update():
        cardno = entry_cardno.get()
        phone = entry_phone.get()
        address = entry_address.get()
        try:
            mycursor.execute(
                "UPDATE library_master SET phone_no = %s, address = %s WHERE cardno = %s",
                (phone, address, cardno),
            )
            mydb.commit()
            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", "Account updated successfully!")
            else:
                messagebox.showinfo("Info", "No account found with the given Card Number.")
            new_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    new_window = tk.Toplevel(root)
    new_window.title("Update Account")
    new_window.geometry("400x300")
    new_window.configure(bg="#fdf8e4")

    tk.Label(new_window, text="Update Account", font=("Arial", 16), bg="#fdf8e4").pack(pady=10)
    tk.Label(new_window, text="Card Number:", bg="#fdf8e4").pack(pady=5)
    entry_cardno = tk.Entry(new_window, font=("Arial", 12))
    entry_cardno.pack(pady=5)
    tk.Label(new_window, text="New Phone Number:", bg="#fdf8e4").pack(pady=5)
    entry_phone = tk.Entry(new_window, font=("Arial", 12))
    entry_phone.pack(pady=5)
    tk.Label(new_window, text="New Address:", bg="#fdf8e4").pack(pady=5)
    entry_address = tk.Entry(new_window, font=("Arial", 12))
    entry_address.pack(pady=5)
    tk.Button(new_window, text="Save", command=save_update, font=("Arial", 12), bg="#FFA500", fg="white", width=10).pack(pady=20)

def delete_account():
    def confirm_delete():
        cardno = entry_cardno.get()
        try:
            mycursor.execute("DELETE FROM library_master WHERE cardno = %s", (cardno,))
            mydb.commit()
            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", "Account deleted successfully!")
            else:
                messagebox.showinfo("Info", "No account found with the given Card Number.")
            new_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    new_window = tk.Toplevel(root)
    new_window.title("Delete Account")
    new_window.geometry("300x200")
    new_window.configure(bg="#ffeeee")

    tk.Label(new_window, text="Delete Account", font=("Arial", 16), bg="#ffeeee").pack(pady=10)
    tk.Label(new_window, text="Card Number:", bg="#ffeeee").pack(pady=5)
    entry_cardno = tk.Entry(new_window, font=("Arial", 12))
    entry_cardno.pack(pady=5)
    tk.Button(new_window, text="Delete", command=confirm_delete, font=("Arial", 12), bg="#FF0000", fg="white", width=10).pack(pady=20)

def view_accounts():
    new_window = tk.Toplevel(root)
    new_window.title("View Accounts")
    new_window.geometry("600x400")
    new_window.configure(bg="#f5f5f5")

    tk.Label(new_window, text="View Accounts", font=("Arial", 16), bg="#f5f5f5").pack(pady=10)

    tree = ttk.Treeview(new_window, columns=("Card No", "Name", "Phone", "Address", "DOB"), show="headings")
    tree.heading("Card No", text="Card No")
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Address", text="Address")
    tree.heading("DOB", text="DOB")
    tree.pack(fill="both", expand=True)

    try:
        mycursor.execute("SELECT * FROM library_master")
        rows = mycursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

tk.Label(root, text="Library Management System", font=("Arial", 24), bg="#f7f7f7", fg="#333").pack(pady=20)
button_style = {"font": ("Arial", 14), "bg": "#4CAF50", "fg": "white", "width": 20, "height": 2}
tk.Button(root, text="Create Account", command=create_account, **button_style).pack(pady=10)
tk.Button(root, text="Update Account", command=update_account, **button_style).pack(pady=10)
tk.Button(root, text="Delete Account", command=delete_account, **button_style).pack(pady=10)
tk.Button(root, text="View Accounts", command=view_accounts, **button_style).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14), bg="#f44336", fg="white", width=20, height=2).pack(pady=20)

root.mainloop()
