import tkinter
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, tkinter.END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)

    pyperclip.copy(password)
    messagebox.showinfo("Password copied", "Password copied to clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    # Get data from entry fields
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # Check fields if they are completed
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror("Oops", "Please make sure you haven't left any fields empty")
    else:
        is_ok = messagebox.askokcancel(f"{website}",
                                       f"These are the details entered:\nEmail: {email}\nPassword: {password}\nIs it ok to save?")

        # Save data to file
        if is_ok:
            try:
                with open("password_manager.json", "r") as data_file:
                    # Read old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("password_manager.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Update old data with new data
                data.update(new_data)

                with open("password_manager.json", "w") as data_file:
                    # Save updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, tkinter.END)
                email_entry.delete(0, tkinter.END)
                password_entry.delete(0, tkinter.END)


# ---------------------------- FIND DATA ------------------------------- #
def find_password():
    try:
        with open("password_manager.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror("File not found", "No data file found")
    else:
        for key in data:
            if key == website_entry.get():
                messagebox.showinfo(f"{key}", f"Email: {data[key]['email']}\nPassword: {data[key]['password']}")
            else:
                messagebox.showerror("Website not found", f"No details for {key}")


# ---------------------------- UI SETUP ------------------------------- #


window = tkinter.Tk()
window.title("Password generator")
window.config(padx=20, pady=20)

# Logo canvas
canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
logo_img = tkinter.PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Label
website_label = tkinter.Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = tkinter.Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = tkinter.Label(text="Password:")
password_label.grid(row=3, column=0)

# Entry
website_entry = tkinter.Entry(width=33)
website_entry.focus()
website_entry.grid(row=1, column=1)

email_entry = tkinter.Entry(width=51)
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = tkinter.Entry(width=33)
password_entry.grid(row=3, column=1)

# Button
search_website_button = tkinter.Button(text="Search", width=14, bg="#0077B6", fg="white", command=find_password)
search_website_button.grid(row=1, column=2)

password_button = tkinter.Button(text="Generate password", width=14, command=generate_password)
password_button.grid(row=3, column=2)

add_button = tkinter.Button(text="Add", width=43, command=save_data)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
