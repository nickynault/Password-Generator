# Password Generator

A simple command-line tool for generating random passwords.

## Prerequisites

- Python 3.x
- Git


## Getting Started

1. Clone the repository:
   git clone [<repository_url>](https://github.com/nickynault/Password-Generator.git)
   
2. Navigate to the project directory:
  cd password-generator

3. Create a virtual environment:
  python -m venv venv

4. Activate the virtual environment:
  For Windows:
    venv\Scripts\activate
  For macOS/Linux:
    source venv/bin/activate
   
5. Install the required packages:
  pip install pyperclip zxcvbn


## Usage
To generate a password, run the following command:
  python password_generator.py
  
The generated password will be printed, and it will be automatically copied to your clipboard.


## Customization

You can customize the length and character types of the generated password by using the command-line options:
  python password_generator.py -l <length> -lt -d -s

Options:

-l or --length: Specifies the length of the password (default: 12).
-lt or --letters: Include letters (both uppercase and lowercase) in the password.
-d or --digits: Include digits in the password.
-s or --symbols: Include symbols in the password.

Examples:

Generate a 10-character password with letters and digits:
  python password_generator.py -l 10 -lt -d

Generate a password with symbols only:
  python password_generator.py -lt -s


## Password History and Expiration

The tool keeps a password history and allows you to check for expired passwords. Passwords are stored in a file named password_history.txt.

To check for expired passwords, run the following command:
  python password_generator.py -E

To view the password history, run the following command:
  python password_generator.py -H

## License
This project is licensed under the MIT License.
