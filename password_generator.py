import string
import random
import pyperclip

# Generates a 12 character random password
def generate_password(length = 12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Automatically copies the password to your clipboard for use
def copy_to_clipboard(text):
    pyperclip.copy(text)

# Runs the functions
if __name__ == '__main__':
    password = generate_password()
    copy_to_clipboard(password)
    print('Generated password: ', password)