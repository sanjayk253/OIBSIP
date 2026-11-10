import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# Character sets
CHARACTERS = {
    "Uppercase": string.ascii_uppercase,
    "Lowercase": string.ascii_lowercase,
    "Numbers": string.digits,
    "Symbols": "!@#$%^&*()_+-=[]{};:,.<>?"
}

AMBIGUOUS = "0O1Il"


class PasswordGenerator:

    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # Password history
        self.history = []

        # Variables
        self.length = tk.IntVar(value=16)

        self.options = {
            name: tk.BooleanVar(value=True)
            for name in CHARACTERS
        }

        self.exclude = tk.BooleanVar(value=True)

        self.create_interface()

    def create_interface(self):

        tk.Label(
            self.root,
            text="SECURE PASSWORD GENERATOR",
            font=("Arial", 17, "bold")
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Password Length"
        ).pack()

        tk.Spinbox(
            self.root,
            from_=1,
            to=128,
            textvariable=self.length,
            width=10
        ).pack(pady=8)

        tk.Label(
            self.root,
            text="Character Types",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        for name, variable in self.options.items():

            tk.Checkbutton(
                self.root,
                text=name,
                variable=variable
            ).pack(anchor="w", padx=150)

        tk.Checkbutton(
            self.root,
            text="Exclude ambiguous characters (0, O, 1, l, I)",
            variable=self.exclude
        ).pack(pady=12)

        tk.Button(
            self.root,
            text="Generate Password",
            command=self.generate,
            bg="#2563eb",
            fg="white",
            width=25
        ).pack(pady=12)

        self.password_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            justify="center",
            width=35
        )

        self.password_entry.pack(pady=10)

        tk.Button(
            self.root,
            text="Copy to Clipboard",
            command=self.copy_password
        ).pack(pady=5)

        self.strength = tk.Label(
            self.root,
            text="Password Strength: Not Generated",
            font=("Arial", 11, "bold")
        )

        self.strength.pack(pady=12)

        tk.Label(
            self.root,
            text="Recent Passwords (Last 5)",
            font=("Arial", 12, "bold")
        ).pack(pady=8)

        self.history_box = tk.Listbox(
            self.root,
            width=42,
            height=5
        )

        self.history_box.pack(pady=5)

        self.status = tk.Label(
            self.root,
            text="Ready to generate a secure password."
        )

        self.status.pack(pady=10)

    def generate(self):

        # Validate password length
        try:
            length = self.length.get()

            if length < 8 or length > 128:
                raise ValueError

        except (ValueError, tk.TclError):

            messagebox.showerror(
                "Invalid Length",
                "Enter a password length between 8 and 128."
            )

            return

        # Get selected character types
        selected = [
            CHARACTERS[name]
            for name, variable in self.options.items()
            if variable.get()
        ]

        # Validate character selection
        if len(selected) < 2:

            messagebox.showerror(
                "Selection Error",
                "Select at least two character types."
            )

            return

        # Exclude ambiguous characters
        if self.exclude.get():

            selected = [
                ''.join(
                    char for char in group
                    if char not in AMBIGUOUS
                )
                for group in selected
            ]

        if any(not group for group in selected):

            messagebox.showerror(
                "Selection Error",
                "A selected character group is empty."
            )

            return

        # Combine selected character groups
        pool = ''.join(selected)

        # Guarantee at least one character from each selected type
        password = [
            secrets.choice(group)
            for group in selected
        ]

        # Generate remaining characters
        password.extend(
            secrets.choice(pool)
            for _ in range(length - len(password))
        )

        # Securely shuffle characters
        secrets.SystemRandom().shuffle(password)

        result = ''.join(password)

        # Display generated password
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, result)

        # Check password strength
        self.check_strength(length, len(selected))

        # ==================================
        # PASSWORD HISTORY - LAST 5 ONLY
        # ==================================

        self.history.insert(0, result)

        # Keep only the latest five passwords
        self.history = self.history[:5]

        # Clear previous history display
        self.history_box.delete(0, tk.END)

        # Display updated history
        for password in self.history:
            self.history_box.insert(tk.END, password)

        # Automatically copy generated password
        try:

            pyperclip.copy(result)

            self.status.config(
                text="Password generated and copied!"
            )

        except pyperclip.PyperclipException:

            self.status.config(
                text="Password generated. Clipboard unavailable."
            )

    def check_strength(self, length, diversity):

        if length >= 16 and diversity >= 4:
            level = "STRONG"

        elif length >= 12 and diversity >= 3:
            level = "MEDIUM"

        else:
            level = "WEAK"

        self.strength.config(
            text=f"Password Strength: {level}"
        )

    def copy_password(self):

        password = self.password_entry.get()

        if not password:

            messagebox.showwarning(
                "Warning",
                "Generate a password first."
            )

            return

        try:

            pyperclip.copy(password)

            self.status.config(
                text="Password copied successfully!"
            )

        except pyperclip.PyperclipException:

            messagebox.showerror(
                "Clipboard Error",
                "Unable to access clipboard."
            )


# Main application
if __name__ == "__main__":

    root = tk.Tk()

    app = PasswordGenerator(root)

    root.mainloop()