import csv
import random
import string
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, filedialog

import pyperclip
import zxcvbn

HISTORY_FILE = 'password_history.txt'
EXPIRATION_DAYS = 90


def generate_password(length=12, include_letters=True, include_digits=True, include_symbols=True):
    characters = ''
    if include_letters:
        characters += string.ascii_letters
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def evaluate_password_strength(password):
    result = zxcvbn.zxcvbn(password)
    # Suppress yellow underline: The 'score' key is present in the result dictionary
    score = result['score']  # type: ignore
    feedback = result['feedback']['suggestions'][0] if result['feedback'][
        'suggestions'] else 'Strong and secure password!'
    return score, feedback


def copy_to_clipboard(text):
    pyperclip.copy(text)


def save_password_to_history(password):
    expiration_date = datetime.now() + timedelta(days=EXPIRATION_DAYS)
    with open(HISTORY_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([password, expiration_date.strftime('%Y-%m-%d')])


# Function to handle the Save button click event
def save_password_handler():
    password = password_label['text'][19:]  # Extract the generated password from the label text

    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")],
        title="Save Password"
    )

    if filename:
        save_password_to_history(password)
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([password, datetime.now().strftime('%Y-%m-%d')])
        messagebox.showinfo("Password Saved", f"Password saved to file:\n{filename}")
    else:
        messagebox.showwarning("No File Selected",
                               "No file selected. Password saved in default location (password_history.txt).")


# Function to fade the "Copied to clipboard" label
def fade_copied_label():
    copied_label.config(text="")
    copied_label.after(3000, lambda: copied_label.config(fg="white"))


# Create the main window
window = tk.Tk()
window.title("Password Generator")

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the center position
window_width = 600
window_height = 600
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window geometry
window.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Function to generate a password and display it
def generate_password_handler():
    length = int(length_entry.get())
    include_letters = letters_var.get()
    include_digits = digits_var.get()
    include_symbols = symbols_var.get()

    password = generate_password(
        length=length,
        include_letters=include_letters,
        include_digits=include_digits,
        include_symbols=include_symbols
    )

    password_label.config(text="Generated Password: " + password)
    save_button.config(state="normal")

    # Evaluate password strength
    score, feedback = evaluate_password_strength(password)

    strength_label.config(text="Strength Score: " + str(score))
    feedback_label.config(text="Feedback: " + feedback)

    # Copy the password to clipboard
    copy_to_clipboard(password)
    copied_label.config(text="Copied to clipboard!", fg="green")


# Label for password length
length_label = tk.Label(window, text="Password Length:", font=("Arial", 18))
length_label.pack(pady=10)

# Entry field for password length
length_entry = tk.Entry(window, font=("Arial", 18))
length_entry.insert(0, "12")  # Set default length
length_entry.pack()

# Checkboxes for character types
letters_var = tk.BooleanVar(value=True)
letters_checkbox = tk.Checkbutton(window, text="Include Letters", variable=letters_var, font=("Arial", 18))
letters_checkbox.pack()

digits_var = tk.BooleanVar(value=True)
digits_checkbox = tk.Checkbutton(window, text="Include Digits", variable=digits_var, font=("Arial", 18))
digits_checkbox.pack()

symbols_var = tk.BooleanVar(value=True)
symbols_checkbox = tk.Checkbutton(window, text="Include Symbols", variable=symbols_var, font=("Arial", 18))
symbols_checkbox.pack()

# Button to generate password
generate_button = tk.Button(window, text="Generate", command=generate_password_handler, font=("Arial", 18))
generate_button.pack(pady=10)

# Label to display generated password
password_label = tk.Label(window, text="Generated Password:", font=("Arial", 18))
password_label.pack()

# Label for password strength score
strength_label = tk.Label(window, text="Strength Score:", font=("Arial", 18))
strength_label.pack()

# Label for password strength feedback
feedback_label = tk.Label(window, text="Feedback:", font=("Arial", 18))
feedback_label.pack()

# Label to display "Copied to clipboard" message
copied_label = tk.Label(window, text="", font=("Arial", 12), fg="green")
copied_label.pack(pady=10)

# Button to save password
save_button = tk.Button(window, text="Save", command=save_password_handler, font=("Ariel", 18), state="disabled")
save_button.pack(pady=(10, 20))

# Schedule the fading effect
window.after(3000, fade_copied_label)

# Run the Tkinter event loop
window.mainloop()
