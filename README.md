# Secure Random Password Generator

This project contains a beginner-friendly command-line password generator and an advanced Tkinter GUI version.

## Project Features

### Beginner Tier
- Validates password length
- Requires at least 8 characters
- Accepts user-selected character categories
- Ensures at least one character from every selected category appears in the final password
- Allows repeated password generation without restarting the program

### Advanced Tier
- GUI-based password generator using Tkinter
- Uses `secrets` for cryptographic randomness
- Requires at least two selected character types
- Includes a copy-to-clipboard button
- Stores recent generated passwords in history
- Includes an optional feature to exclude ambiguous characters

## Why `secrets` is preferred over `random`

The `random` module is designed for simulation and general-purpose randomness. It is not suitable for passwords because it is predictable. The `secrets` module is built specifically for security-sensitive tasks. It uses cryptographically secure random sources, so passwords generated with it are much harder to predict.

## Setup (without virtual environments)

1. Open a terminal in the project folder.
2. Make sure Python is installed.
3. Install the extra package used by the GUI version:

```bash
pip install pyperclip
```

4. Run the beginner version:

```bash
python beginner_cli.py
```

5. Run the advanced version:

```bash
python advanced_gui.py
```

## Example commands

### Beginner example
```text
Enter password length: 12
Select character types:
1. Uppercase
2. Lowercase
3. Numbers
4. Symbols
Enter your choices: 1 2 3
Generated Password: A7#mK92@pLq!
```

### Advanced example
- Choose a length from 8 to 128
- Select at least two types
- Click "Generate Password"
- Click "Copy to Clipboard" to copy the password

## Files in this project

- `password_generator.py` – shared password logic
- `beginner_cli.py` – command line app
- `advanced_gui.py` – Tkinter GUI app
- `README.md` – instructions and explanation
