import re
import math
import random
import tkinter as tk
from tkinter import messagebox

COMMON_PASSWORDS = {"123456", "password", "123456789", "qwerty", "abc123", "password1", "iloveyou"}
DICTIONARY_WORDS = {"love", "admin", "summer", "winter", "hello", "sun", "moon"}

def calculate_entropy(password):
    charset = 0
    if re.search("[a-z]", password): charset += 26
    if re.search("[A-Z]", password): charset += 26
    if re.search("[0-9]", password): charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): charset += 32
    if charset == 0: return 0
    return round(len(password) * math.log2(charset), 2)

def suggest_strong_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-={}[]:;<>?,."
    return ''.join(random.choices(chars, k=14))

def check_password_strength(password):
    feedback = []
    entropy = calculate_entropy(password)

    if password in COMMON_PASSWORDS:
        return ("Very Weak", "This is a very common password.", "red", entropy)

    if any(word in password.lower() for word in DICTIONARY_WORDS):
        feedback.append("Avoid dictionary words like 'love', 'admin'.")

    if len(password) < 8:
        feedback.append("Too short! Use at least 8 characters.")
    elif len(password) > 20:
        feedback.append("Too long! Aim for under 20 characters.")

    if not re.search("[a-z]", password):
        feedback.append("Add a lowercase letter.")
    if not re.search("[A-Z]", password):
        feedback.append("Add an uppercase letter.")
    if not re.search("[0-9]", password):
        feedback.append("Add a number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        feedback.append("Add a special character.")

    if entropy < 40:
        feedback.append(f"Very low entropy ({entropy} bits).")
        return ("Weak", "\n".join(feedback), "red", entropy)
    elif entropy < 60:
        feedback.append(f"Moderate entropy ({entropy} bits).")
        return ("Moderate", "\n".join(feedback), "orange", entropy)
    else:
        feedback.append(f"Great entropy ({entropy} bits)!")
        return ("Strong", "\n".join(feedback), "green", entropy)

def login_simulation():
    username = user_entry.get()
    password = pass_entry.get()

    if not username or not password:
        messagebox.showwarning("Missing Info", "Please enter both username and password.")
        return

    status, feedback, color, entropy = check_password_strength(password)
    if status == "Strong":
        messagebox.showinfo("Safe!", f"Well done, {username}! Your password is strong and secure. ✅")
    else:
        messagebox.showinfo("Hacked!", f"Ha ha, {username}! You've been hacked! \nLet's check how strong your password really is...")
    show_strength(password)

def show_strength(password):
    status, feedback, color, entropy = check_password_strength(password)
    result_label.config(text=f"{status} Password", fg=color)
    detail_label.config(text=feedback)
    if status == "Strong":
        suggestion_label.config(text="🎉 Congrats! Your password is strong and secure! 💪", fg="lightgreen")
    else:
        suggestion = suggest_strong_password()
        suggestion_label.config(text=f"Try this stronger password instead:\n👉 {suggestion}", fg="lime")

def toggle_password():
    current = pass_entry.cget('show')
    pass_entry.config(show="" if current == "*" else "*")
    toggle_btn.config(text="Hide" if current == "*" else "Show")

# yaha se gui ka code 
root = tk.Tk()
root.title("💻 Hacker Game - PASSO")
root.geometry("580x480")
root.configure(bg="#101820")
root.resizable(False, False)

header = tk.Label(root, text="😈 Login Terminal", font=("Courier New", 20, "bold"), bg="#101820", fg="#39ff14")
header.pack(pady=10)

user_frame = tk.Frame(root, bg="#101820")
user_frame.pack(pady=5)
tk.Label(user_frame, text="Username:", font=("Helvetica", 12), bg="#101820", fg="white").grid(row=0, column=0, padx=5)
user_entry = tk.Entry(user_frame, font=("Helvetica", 14), width=25)
user_entry.grid(row=0, column=1, padx=5)

pass_frame = tk.Frame(root, bg="#101820")
pass_frame.pack(pady=5)
tk.Label(pass_frame, text="Password:", font=("Helvetica", 12), bg="#101820", fg="white").grid(row=0, column=0, padx=5)
pass_entry = tk.Entry(pass_frame, font=("Helvetica", 14), width=25, show="*")
pass_entry.grid(row=0, column=1, padx=5)

toggle_btn = tk.Button(pass_frame, text="Show", font=("Helvetica", 10), command=toggle_password)
toggle_btn.grid(row=0, column=2, padx=5)

login_btn = tk.Button(root, text="🔓 Login", font=("Helvetica", 12, "bold"), bg="#39ff14", fg="black", command=login_simulation)
login_btn.pack(pady=15)

result_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), bg="#101820")
result_label.pack(pady=5)

detail_label = tk.Label(root, text="", font=("Helvetica", 12), wraplength=500, justify="left", bg="#101820", fg="white")
detail_label.pack(pady=5)

suggestion_label = tk.Label(root, text="", font=("Courier", 12), wraplength=500, justify="left", bg="#101820")
suggestion_label.pack(pady=10)

root.mainloop()