import tkinter as tk
from tkinter import messagebox


# BMI Calculation
def calculate_bmi():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if height <= 0 or weight <= 0:
            messagebox.showerror("Invalid Input", "Enter positive values.")
            return

        if not 50 <= height <= 250:
            messagebox.showerror(
                "Invalid Height",
                "Height must be between 50 and 250 cm."
            )
            return

        if not 10 <= weight <= 500:
            messagebox.showerror(
                "Invalid Weight",
                "Weight must be between 10 and 500 kg."
            )
            return

        height_m = height / 100
        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            category = "Underweight"
            color = "#60A5FA"

        elif bmi < 25:
            category = "Normal Weight"
            color = "#34D399"

        elif bmi < 30:
            category = "Overweight"
            color = "#FBBF24"

        else:
            category = "Obese"
            color = "#F87171"

        result_value.config(text=f"{bmi:.2f}", fg=color)
        category_label.config(text=category, fg=color)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numeric values."
        )


# Reset Function
def reset_fields():
    height_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)

    result_value.config(text="--", fg="white")
    category_label.config(
        text="Enter your details",
        fg="#94A3B8"
    )


# Main Window
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("450x760")
root.resizable(True, True)
root.configure(bg="#0F172A")


# Header
title = tk.Label(
    root,
    text="BMI CALCULATOR",
    font=("Segoe UI", 23, "bold"),
    bg="#0F172A",
    fg="white"
)
title.pack(pady=(20, 5))


subtitle = tk.Label(
    root,
    text="Know your Body Mass Index",
    font=("Segoe UI", 11),
    bg="#0F172A",
    fg="#94A3B8"
)
subtitle.pack(pady=(0, 15))


# Input Card
card = tk.Frame(
    root,
    bg="#1E293B",
    padx=30,
    pady=20
)
card.pack(padx=25, fill="x")


# Height Input
tk.Label(
    card,
    text="Height (cm)",
    font=("Segoe UI", 11, "bold"),
    bg="#1E293B",
    fg="white"
).pack(anchor="w")


height_entry = tk.Entry(
    card,
    font=("Segoe UI", 13),
    bg="#334155",
    fg="white",
    insertbackground="white",
    relief="flat"
)
height_entry.pack(fill="x", ipady=10, pady=(6, 14))


# Weight Input
tk.Label(
    card,
    text="Weight (kg)",
    font=("Segoe UI", 11, "bold"),
    bg="#1E293B",
    fg="white"
).pack(anchor="w")


weight_entry = tk.Entry(
    card,
    font=("Segoe UI", 13),
    bg="#334155",
    fg="white",
    insertbackground="white",
    relief="flat"
)
weight_entry.pack(fill="x", ipady=10, pady=(6, 18))


# Calculate Button
calculate_button = tk.Button(
    card,
    text="Calculate BMI",
    font=("Segoe UI", 12, "bold"),
    bg="#6366F1",
    fg="white",
    activebackground="#4F46E5",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=calculate_bmi
)
calculate_button.pack(fill="x", ipady=10)


# Reset Button
reset_button = tk.Button(
    card,
    text="Reset",
    font=("Segoe UI", 11),
    bg="#334155",
    fg="white",
    activebackground="#475569",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=reset_fields
)
reset_button.pack(fill="x", ipady=8, pady=(10, 0))


# Result Section
result_frame = tk.Frame(
    root,
    bg="#1E293B",
    padx=20,
    pady=20
)
result_frame.pack(fill="x", padx=25, pady=12)


tk.Label(
    result_frame,
    text="YOUR BMI RESULT",
    font=("Segoe UI", 11, "bold"),
    bg="#1E293B",
    fg="#94A3B8"
).pack()


result_value = tk.Label(
    result_frame,
    text="--",
    font=("Segoe UI", 38, "bold"),
    bg="#1E293B",
    fg="white"
)
result_value.pack(pady=5)


category_label = tk.Label(
    result_frame,
    text="Enter your details",
    font=("Segoe UI", 13, "bold"),
    bg="#1E293B",
    fg="#94A3B8"
)
category_label.pack()


# BMI Categories
footer = tk.Label(
    root,
    text="Underweight  <18.5  |  Normal  18.5–24.9\n"
         "Overweight  25–29.9  |  Obese  ≥30",
    font=("Segoe UI", 9),
    bg="#0F172A",
    fg="#94A3B8",
    justify="center"
)
footer.pack(pady=2)


# Disclaimer
tk.Label(
    root,
    text="BMI is a screening measure, not a medical diagnosis.",
    font=("Segoe UI", 8),
    bg="#0F172A",
    fg="#64748B"
).pack(pady=5)


# Keyboard Support
root.bind("<Return>", lambda event: calculate_bmi())


# Run Application
root.mainloop()