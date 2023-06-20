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
  pip install pyperclip


## Usage
To generate a password, run the following command:
  python password_generator.py
  
The generated password will be printed, and it will be automatically copied to your clipboard.


## Customization

You can customize the length of the generated password by modifying the length parameter in the generate_password() function.
If you wish to exclude certain character types from the generated password, you can modify the characters variable in the generate_password() function.


## License
This project is licensed under the MIT License.
