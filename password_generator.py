import string
import random
import pyperclip
import argparse
import os
import zxcvbn
from datetime import datetime, timedelta

HISTORY_FILE = 'password_history.txt'
EXPIRATION_DAYS = 90

# Generates a random password with customizable options
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

# Evaluates the strength of a password using zxcvbn library
def evaluate_password_strength(password):
    result = zxcvbn.zxcvbn(password)
    return result

# Copies the given text to the clipboard
def copy_to_clipboard(text):
    pyperclip.copy(text)

# Saves the password and its expiration date to the password history file
def save_password_to_history(password):
    expiration_date = datetime.now() + timedelta(days=EXPIRATION_DAYS)
    with open(HISTORY_FILE, 'a') as file:
        file.write(f"{password},{expiration_date.strftime('%Y-%m-%d')}\n")

# Loads the password history from the file
def load_password_history():
    if not os.path.isfile(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as file:
        password_history = file.read().splitlines()
    return password_history

# Checks for expired passwords in the password history
def check_password_expiration():
    password_history = load_password_history()
    if not password_history:
        print('No password history found.')
        return

    today = datetime.now().date()
    expired_passwords = []
    for password_entry in password_history:
        try:
            password, expiration_date = password_entry.split(',')
            expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()
            if expiration_date <= today:
                expired_passwords.append(password)
        except ValueError:
            continue

    if expired_passwords:
        print('Expired passwords:')
        for password in expired_passwords:
            print(password)
    else:
        print('No expired passwords.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate random passwords')
    parser.add_argument('-l', '--length', type=int, default=12, help='Length of the password (default: 12)')
    parser.add_argument('-lt', '--letters', action='store_true', help='Include letters in the password')
    parser.add_argument('-d', '--digits', action='store_true', help='Include digits in the password')
    parser.add_argument('-s', '--symbols', action='store_true', help='Include symbols in the password')
    parser.add_argument('-f', '--filename', type=str, default=None, help='Name of the file to save passwords')
    parser.add_argument('-n', '--count', type=int, default=1, help='Number of passwords to generate')
    parser.add_argument('-H', '--history', action='store_true', help='Show password history')
    parser.add_argument('-E', '--expiration', action='store_true', help='Check password expiration')

    args = parser.parse_args()

    # Check password expiration if the corresponding flag is provided
    if args.expiration:
        check_password_expiration()
    # Display password history if the corresponding flag is provided
    elif args.history:
        password_history = load_password_history()
        if password_history:
            print('Password History:')
            for password_entry in password_history:
                password, expiration_date = password_entry.split(',')
                print(f"Password: {password} (Expires on: {expiration_date})")
        else:
            print('No password history found.')
    # Generate and handle passwords
    else:
        # Set default options if no specific options are provided
        if not args.letters and not args.digits and not args.symbols:
            args.letters = True
            args.digits = True
            args.symbols = True

        passwords = []
        for _ in range(args.count):
            password = generate_password(
                length=args.length,
                include_letters=args.letters,
                include_digits=args.digits,
                include_symbols=args.symbols
            )
            passwords.append([password])
            save_password_to_history(password)

        # Evaluate the strength of the first password generated
        password_strength = evaluate_password_strength(passwords[0][0])
        score = password_strength['score']
        feedback = password_strength['feedback']

        # Save passwords to a file if the filename is provided
        if args.filename:
            with open(args.filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(passwords)

        # Copy the first password to the clipboard
        copy_to_clipboard(passwords[0][0])
        print(f'Generated {args.count} passwords:')
        for password in passwords:
            print(password[0])
        print('Password Strength Score:', score)
        print('Feedback:', feedback)
