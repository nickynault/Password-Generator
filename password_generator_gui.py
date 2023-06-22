import tkinter as tk
from tkinter import messagebox

import string
import random
import pyperclip
import argparse
import csv
import os
import zxcvbn
from datetime import datetime, timedelta

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
    score = result['score']
    feedback = result['feedback']['warning'] or result['feedback']['suggestions']
    if not feedback:
        feedback = 'Strong and secure password!'
    return score, feedback



def copy_to_clipboard(text):
    pyperclip.copy(text)

def save_password_to_history(password):
    expiration_date = datetime.now() + timedelta(days=EXPIRATION_DAYS)
    with open(HISTORY_FILE, 'a') as file:
        file.write(f"{password},{expiration_date.strftime('%Y-%m-%d')}\n")

# Create the main window
window = tk.Tk()
window.title("Password Generator")

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

    # Evaluate password strength
    score, feedback = evaluate_password_strength(password)

    strength_label.config(text="Strength Score: " + str(score))
    feedback_label.config(text="Feedback: " + feedback)

    # Copy the password to clipboard
    copy_to_clipboard(password)
    messagebox.showinfo("Password Generated", "Password copied to clipboard.")




# Label for password length
length_label = tk.Label(window, text="Password Length:")
length_label.pack()

# Entry field for password length
length_entry = tk.Entry(window)
length_entry.insert(0, "12")  # Set default length
length_entry.pack()

# Checkboxes for character types
letters_var = tk.BooleanVar(value=True)
letters_checkbox = tk.Checkbutton(window, text="Include Letters", variable=letters_var)
letters_checkbox.pack()

digits_var = tk.BooleanVar(value=True)
digits_checkbox = tk.Checkbutton(window, text="Include Digits", variable=digits_var)
digits_checkbox.pack()

symbols_var = tk.BooleanVar(value=True)
symbols_checkbox = tk.Checkbutton(window, text="Include Symbols", variable=symbols_var)
symbols_checkbox.pack()

# Button to generate password
generate_button = tk.Button(window, text="Generate", command=generate_password_handler)
generate_button.pack()

# Label to display generated password
password_label = tk.Label(window, text="Generated Password: ")
password_label.pack()

# Label for password strength score
strength_label = tk.Label(window, text="Strength Score: ")
strength_label.pack()

# Label for password strength feedback
feedback_label = tk.Label(window, text="Feedback: ")
feedback_label.pack()

# Run the Tkinter event loop
window.mainloop()
