from password_generator import generate_password, parse_character_choices, validate_length


def show_character_types_menu():
    print("\nSelect character types:")
    print("1. Uppercase")
    print("2. Lowercase")
    print("3. Numbers")
    print("4. Symbols")


def main():
    print("========================================")
    print("     SECURE RANDOM PASSWORD GENERATOR")
    print("========================================")

    while True:
        try:
            raw_length = input("Enter password length: ").strip()
            length = validate_length(raw_length)
        except ValueError as error:
            print(error)
            continue

        show_character_types_menu()
        try:
            selection = input("Enter your choices: ").strip()
            selected_types = parse_character_choices(selection)
        except ValueError as error:
            print(error)
            continue

        password = generate_password(length, selected_types)
        print(f"Generated Password: {password}")

        while True:
            choice = input("Generate another password? (y/n): ").strip().lower()
            if choice in {"y", "n"}:
                break
            print("Please enter 'y' or 'n'.")

        if choice == "n":
            print("Thank you for using Secure Password Generator.")
            break


if __name__ == "__main__":
    main()
