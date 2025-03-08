import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cipher


def select_file(path_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        path_label.config(text=file_path)
    update_button_states()
    return file_path


def update_button_states():
    open_text_path = open_text_path_label.cget("text")
    cipher_text_path = cipher_text_path_label.cget("text")

    # if os.path.exists(key_path) and key_path:
    encrypt_button.config(
        state=(
            tk.NORMAL
            if os.path.exists(open_text_path) and open_text_path
            else tk.DISABLED
        )
    )
    decrypt_button.config(
        state=(
            tk.NORMAL
            if os.path.exists(cipher_text_path) and cipher_text_path
            else tk.DISABLED
        )
    )
    # else:
    # encrypt_button.config(state=tk.DISABLED)
    # decrypt_button.config(state=tk.DISABLED)


def encrypt_text():
    log_text.delete(1.0, tk.END)
    path_to_open_text = open_text_path_label.cget("text")
    path_to_key = key_path_label.cget("text")
    path_to_save_encrypt_file = save_encrypt_path_label.cget("text")

    if not os.path.exists(path_to_open_text) or not os.path.isfile(path_to_open_text):
        messagebox.showerror("Ошибка", "Файл с текстом не существует")
        return
    if not os.path.exists(path_to_key) or not os.path.isfile(path_to_key):
        messagebox.showerror("Ошибка", "Файл с ключом не существует")
        return

    with open(path_to_open_text, encoding="utf-8") as f:
        open_text = f.read().lower()
        open_text = "".join(i for i in open_text if i in cipher.ALL_CHARACTERS)
    with open(path_to_key, encoding="utf-8") as f:
        key = f.read().lower()
        key = "".join(i for i in key if i in cipher.ALL_CHARACTERS)

    if open_text == "":
        messagebox.showerror("Ошибка", "Файл с текстом пуст")
        return
    if key == "":
        messagebox.showerror("Ошибка", "Файл с ключом пуст")
        return

    encrypted_text = cipher.encrypt(open_text, key)
    if path_to_save_encrypt_file:
        with open(path_to_save_encrypt_file, "w", encoding="utf-8") as f:
            f.write(encrypted_text)
        messagebox.showinfo(
            "Успех", f"Зашифрованный текст сохранён в: {path_to_save_encrypt_file}"
        )
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, encrypted_text)
    log_text.insert(tk.END, f"Зашифрованный текст: {encrypted_text}\n")


def decrypt_text():
    log_text.delete(1.0, tk.END)
    path_to_cipher_text = cipher_text_path_label.cget("text")
    path_to_key = key_path_label.cget("text")
    path_to_save_decrypt_file = save_decrypt_path_label.cget("text")

    if not os.path.exists(path_to_cipher_text) or not os.path.isfile(
        path_to_cipher_text
    ):
        messagebox.showerror("Ошибка", "Файл с шифротекстом не существует")
        return
    if not os.path.exists(path_to_key) or not os.path.isfile(path_to_key):
        messagebox.showerror("Ошибка", "Файл с ключом не существует")
        return

    with open(path_to_cipher_text, encoding="utf-8") as f:
        cipher_text = f.read().lower()
        cipher_text = "".join(i for i in cipher_text if i in cipher.ALL_CHARACTERS)
    with open(path_to_key, encoding="utf-8") as f:
        key = f.read().lower()
        key = "".join(i for i in key if i in cipher.ALL_CHARACTERS)

    if cipher_text == "":
        messagebox.showerror("Ошибка", "Файл с текстом пуст")
        return
    if key == "":
        messagebox.showerror("Ошибка", "Файл с ключом пуст")
        return

    decrypted_text = cipher.decrypt(cipher_text, key)
    if path_to_save_decrypt_file:
        with open(path_to_save_decrypt_file, "w", encoding="utf-8") as f:
            f.write(decrypted_text)
        messagebox.showinfo(
            "Успех", f"Расшифрованный текст сохранён в: {path_to_save_decrypt_file}"
        )
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, decrypted_text)
    log_text.insert(tk.END, f"Расшифрованный текст: {decrypted_text}\n")


root = tk.Tk()
root.title("Шифрование и Расшифровка")
root.geometry("1300x560")

style = ttk.Style()
style.configure(
    "TButton",
    padding=6,
    relief="flat",
    background="#005f73",
    foreground="blue",
    font=("Helvetica", 10, "bold"),
)
style.map(
    "TButton",
    foreground=[("disabled", "#aaaaaa"), ("active", "white")],
    background=[("disabled", "#d3d3d3"), ("active", "#002f3d")],
)
style.configure(
    "TLabel",
    padding=6,
    relief="flat",
    background="#0a9396",
    foreground="white",
    font=("Helvetica", 10),
)
style.configure("TFrame", padding=6, relief="flat", background="#94d2bd")

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = ttk.Frame(frame)
left_frame.grid(row=0, column=0, sticky="nw")

right_frame = ttk.Frame(frame)
right_frame.grid(row=0, column=1, sticky="nw")

buttons_frame = ttk.Frame(frame)
buttons_frame.grid(row=0, column=2, sticky="nw")

open_text_label = ttk.Label(left_frame, text="Выберите файл с открытым текстом")
open_text_label.pack(anchor="w", pady=5)
open_text_button = ttk.Button(
    left_frame,
    text="Выбрать файл",
    command=lambda: select_file(open_text_path_label),
)
open_text_button.pack(anchor="w")
open_text_path_label = ttk.Label(left_frame, text="")
open_text_path_label.pack(anchor="w", pady=2)

cipher_text_label = ttk.Label(left_frame, text="Выберите файл с шифротекстом")
cipher_text_label.pack(anchor="w", pady=5)
cipher_text_button = ttk.Button(
    left_frame,
    text="Выбрать файл",
    command=lambda: select_file(cipher_text_path_label),
)
cipher_text_button.pack(anchor="w")
cipher_text_path_label = ttk.Label(left_frame, text="")
cipher_text_path_label.pack(anchor="w", pady=2)

key_label = ttk.Label(left_frame, text="Выберите файл с ключом")
key_label.pack(anchor="w", pady=5)
key_button = ttk.Button(
    left_frame,
    text="Выбрать файл",
    command=lambda: select_file(key_path_label),
)
key_button.pack(anchor="w")
key_path_label = ttk.Label(left_frame, text="")
key_path_label.pack(anchor="w", pady=2)

save_encrypt_file_label = ttk.Label(
    right_frame, text="Выберите файл для сохранения зашифрованного текста"
)
save_encrypt_file_label.pack(anchor="w", pady=5)
save_encrypt_file_button = ttk.Button(
    right_frame,
    text="Выбрать файл",
    command=lambda: select_file(save_encrypt_path_label),
)
save_encrypt_file_button.pack(anchor="w")
save_encrypt_path_label = ttk.Label(right_frame, text="")
save_encrypt_path_label.pack(anchor="w", pady=2)

save_decrypt_file_label = ttk.Label(
    right_frame, text="Выберите файл для сохранения расшифрованного текста"
)
save_decrypt_file_label.pack(anchor="w", pady=5)
save_decrypt_file_button = ttk.Button(
    right_frame,
    text="Выбрать файл",
    command=lambda: select_file(save_decrypt_path_label),
)
save_decrypt_file_button.pack(anchor="w")
save_decrypt_path_label = ttk.Label(right_frame, text="")
save_decrypt_path_label.pack(anchor="w", pady=2)

result_label = ttk.Label(right_frame, text="Результат:")
result_label.pack(anchor="w", pady=5)
result_text = tk.Text(right_frame, height=2, width=50, bg="#e9d8a6", fg="#001219")
result_text.pack(anchor="w", padx=10, pady=10)

result_text_context_menu = tk.Menu(result_text, tearoff=0)
result_text_context_menu.add_command(
    label="Скопировать",
    command=lambda: root.clipboard_append(result_text.get(1.0, tk.END)),
)
result_text.bind(
    "<Button-3>",
    lambda event: result_text_context_menu.post(event.x_root, event.y_root),
)

log_text = tk.Text(right_frame, height=12, width=50, bg="#f0e68c", fg="#001219")
log_text.pack(anchor="w", padx=10, pady=10)

log_text_context_menu = tk.Menu(log_text, tearoff=0)
log_text_context_menu.add_command(
    label="Скопировать",
    command=lambda: root.clipboard_append(log_text.get(1.0, tk.END)),
)
log_text.bind(
    "<Button-3>", lambda event: log_text_context_menu.post(event.x_root, event.y_root)
)


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)

    def flush(self):
        pass


import sys

sys.stdout = TextRedirector(log_text)

encrypt_button = ttk.Button(
    buttons_frame, text="Зашифровать", command=encrypt_text, state=tk.DISABLED
)
encrypt_button.pack(anchor="w", pady=10)

decrypt_button = ttk.Button(
    buttons_frame, text="Расшифровать", command=decrypt_text, state=tk.DISABLED
)
decrypt_button.pack(anchor="w", pady=10)

root.mainloop()
