import tkinter as tk

try:
    import pyperclip
except ImportError:
    pyperclip = None

from password_generator import generate_password, password_strength


def get_selected_types(checkboxes):
    selected = []
    if checkboxes["uppercase"].get():
        selected.append("uppercase")
    if checkboxes["lowercase"].get():
        selected.append("lowercase")
    if checkboxes["numbers"].get():
        selected.append("numbers")
    if checkboxes["symbols"].get():
        selected.append("symbols")
    return selected


def build_gui():
    root = tk.Tk()
    root.title("Secure Password Generator")
    root.geometry("480x620")
    root.resizable(False, False)

    title = tk.Label(root, text="SECURE PASSWORD GENERATOR", font=("Arial", 18, "bold"))
    title.pack(pady=(18, 10))

    length_frame = tk.Frame(root)
    length_frame.pack(fill="x", padx=20, pady=4)

    tk.Label(length_frame, text="Password Length:", font=("Arial", 11, "bold")).pack(anchor="w")
    length_var = tk.IntVar(value=16)
    length_scale = tk.Scale(length_frame, from_=8, to=128, orient="horizontal", variable=length_var, length=430)
    length_scale.pack(fill="x")

    checkbox_frame = tk.Frame(root)
    checkbox_frame.pack(fill="x", padx=20, pady=10)

    checkboxes = {
        "uppercase": tk.BooleanVar(value=True),
        "lowercase": tk.BooleanVar(value=True),
        "numbers": tk.BooleanVar(value=True),
        "symbols": tk.BooleanVar(value=True),
    }

    for label, var in [
        ("Uppercase Letters", checkboxes["uppercase"]),
        ("Lowercase Letters", checkboxes["lowercase"]),
        ("Numbers", checkboxes["numbers"]),
        ("Symbols", checkboxes["symbols"]),
    ]:
        tk.Checkbutton(checkbox_frame, text=label, variable=var, font=("Arial", 10)).pack(anchor="w")

    exclude_var = tk.BooleanVar(value=False)
    tk.Checkbutton(checkbox_frame, text="Exclude ambiguous characters", variable=exclude_var, font=("Arial", 10)).pack(anchor="w", pady=(4, 0))

    generate_button = tk.Button(root, text="Generate Password", font=("Arial", 11, "bold"), width=25, command=lambda: None)
    generate_button.pack(pady=12)

    password_var = tk.StringVar(value="")
    tk.Label(root, text="Password:", font=("Arial", 11, "bold")).pack(anchor="w", padx=20)
    password_entry = tk.Entry(root, textvariable=password_var, font=("Arial", 12), width=42, justify="center")
    password_entry.pack(padx=20, pady=(4, 8), fill="x")

    strength_var = tk.StringVar(value="")
    tk.Label(root, textvariable=strength_var, font=("Arial", 11, "bold"), fg="darkgreen").pack(anchor="w", padx=20, pady=(0, 8))

    copy_button = tk.Button(root, text="Copy to Clipboard", width=25, command=lambda: None)
    copy_button.pack(pady=(0, 8))

    history_frame = tk.Frame(root)
    history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    tk.Label(history_frame, text="Generation History:", font=("Arial", 11, "bold")).pack(anchor="w")

    history_list = tk.Listbox(history_frame, height=6, width=38, font=("Arial", 10))
    history_list.pack(fill="both", expand=True)

    status_var = tk.StringVar(value="")
    tk.Label(root, textvariable=status_var, fg="red", font=("Arial", 10), wraplength=400, justify="left").pack(padx=20, pady=(0, 8))

    def generate_password_action():
        selected_types = get_selected_types(checkboxes)
        password_length = length_var.get()

        if len(selected_types) < 2:
            status_var.set("Please select at least two character types.")
            strength_var.set("")
            password_var.set("")
            return

        try:
            password = generate_password(
                password_length,
                selected_types,
                exclude_ambiguous=exclude_var.get(),
                secure=True,
            )
            password_var.set(password)
            strength_var.set(f"Strength: {password_strength(password)}")
            status_var.set("")

            history_list.insert(0, password)
            if history_list.size() > 5:
                history_list.delete(5)
        except ValueError as error:
            status_var.set(str(error))
            password_var.set("")
            strength_var.set("")

    def copy_action():
        current_password = password_var.get()
        if not current_password:
            status_var.set("Generate a password before copying.")
            return
        if pyperclip is None:
            status_var.set("Install pyperclip to enable clipboard copying.")
            return
        try:
            pyperclip.copy(current_password)
            status_var.set("Password copied to clipboard.")
        except Exception:
            status_var.set("Clipboard access is unavailable. Copy manually.")

    generate_button.config(command=generate_password_action)
    copy_button.config(command=copy_action)

    root.mainloop()


if __name__ == "__main__":
    build_gui()
