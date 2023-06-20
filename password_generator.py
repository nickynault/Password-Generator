import string
import random
import pyperclip
import argparse
import zxcvbn
import csv

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
    return result

def copy_to_clipboard(text):
    pyperclip.copy(text)

def save_passwords_to_file(filename, passwords):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(passwords)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate random passwords')
    parser.add_argument('-l', '--length', type=int, default=12, help='Length of the password (default: 12)')
    parser.add_argument('-lt', '--letters', action='store_true', help='Include letters in the password')
    parser.add_argument('-d', '--digits', action='store_true', help='Include digits in the password')
    parser.add_argument('-s', '--symbols', action='store_true', help='Include symbols in the password')
    parser.add_argument('-f', '--filename', type=str, default=None, help='Name of the file to save passwords')
    parser.add_argument('-n', '--count', type=int, default=1, help='Number of passwords to generate')

    args = parser.parse_args()

    passwords = []
    for _ in range(args.count):
        password = generate_password(
            length=args.length,
            include_letters=args.letters,
            include_digits=args.digits,
            include_symbols=args.symbols
        )
        passwords.append([password])

    password_strength = evaluate_password_strength(passwords[0][0])
    score = password_strength['score']
    feedback = password_strength['feedback']

    if args.filename:
        save_passwords_to_file(args.filename, passwords)

    copy_to_clipboard(passwords[0][0])
    print(f'Generated {args.count} passwords:')
    for password in passwords:
        print(password[0])
    print('Password Strength Score:', score)
    print('Feedback:', feedback)
