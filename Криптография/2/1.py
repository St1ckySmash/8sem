import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from tkinter import ttk
from sympy import isprime, primefactors
import random
import math
import asyncio
import alphabet


def is_prime(n, k=5):
    """Тест Соловея-Штрассена для проверки простоты числа."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    def jacobi_symbol(a, n):
        """Функция для вычисления символа Якоби."""
        if a == 0:
            return 0
        if a == 1:
            return 1
        if a % 2 == 0:
            if ((n % 8) == 3) or ((n % 8) == 5):
                return -jacobi_symbol(a // 2, n)
            else:
                return jacobi_symbol(a // 2, n)
        if a % n == 0:
            return 0
        if (a % 4 == 3) and (n % 4 == 3):
            return -jacobi_symbol(n % a, a)
        else:
            return jacobi_symbol(n % a, a)

    for _ in range(k):
        a = random.randint(2, n - 1)
        if math.gcd(a, n) > 1:
            return False
        jacobi = jacobi_symbol(a, n)
        if jacobi == 0 or pow(a, (n - 1) // 2, n) != (jacobi % n):
            return False
    return True


async def is_primitive_root(g, p, factors, phi):
    return all(pow(g, phi // factor, p) != 1 for factor in factors)


async def check_root(g, p, factors, phi):
    result = await is_primitive_root(g, p, factors, phi)
    if result:
        return g
    return None


async def find_primitive_root(p):
    phi = p - 1
    # factors = primefactors(phi)
    factors = prime_factors(phi)

    tasks = [
        asyncio.create_task(check_root(g, p, factors, phi))
        for g in range(2, min(50, p))
    ]

    for task in asyncio.as_completed(tasks):
        result = await task
        if result:
            for t in tasks:
                t.cancel()
            return result

    raise Exception("Примитивный корень не найден.")


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def generate_keys(p):
    g = asyncio.run(find_primitive_root(p))
    x = random.randint(2, p - 2)
    y = pow(g, x, p)

    print(f"Сгенерированные ключи:\n p = {p}\n g = {g}\n y = {y}\n x = {x}")

    return (p, g, y), x


def encrypt_block(num_block, p, g, y):
    k = random.randint(1, p - 2)
    a = pow(g, k, p)
    b = (num_block * pow(y, k, p)) % p
    return a, b


def encrypt(message, public_key):
    print(f"открытый текст [{len(message)}]:{message}")

    p, g, y = public_key
    print(f"ключ: p = {public_key[0]} g = {public_key[1]} y = {public_key[2]}\n")

    nums = alphabet.string_to_numbers(message)
    print(f"сопоставленные коды [{len(nums)}]: {nums}\n")

    blocks = alphabet.split_to_blocks(nums, p)
    print(f"блоки[{len(blocks)}]: {blocks}\n")

    blocks_encrypted = []
    for el in blocks:
        blocks_encrypted.append(encrypt_block(el, p, g, y))
    print(f"блоки шифртекста [{len(blocks_encrypted)}]: {blocks_encrypted}")

    return blocks_encrypted


def decrypt_block(ciphertext, p, x):
    a, b = ciphertext
    m = (b * pow(a, p - 1 - x, p)) % p
    return m


def decrypt(ciphertext, private_key, public_key):
    print(f"шифртекст[{len(ciphertext)}]: {ciphertext}")
    print(f"ключ: p = {public_key[0]} x = {private_key}\n")

    blocks = []
    for el in ciphertext:
        blocks.append(decrypt_block(el, public_key[0], private_key))
    print(f"блоки[{len(blocks)}]: {blocks}\n")

    nums = alphabet.split_to_two_digits(blocks)
    print(f"сопоставленные коды [{len(nums)}]: {nums}\n")

    text = alphabet.numbers_to_string(nums)
    print(f"расшифрованный текст [{len(text)}]:{text}")

    return text


##########################################################################################
def select_file(path_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        path_label.config(text=file_path)
    update_button_states()
    return file_path


def update_button_states():
    open_text_path = open_text_path_label.cget("text")
    key_path_open = key_path_open_label.cget("text")
    key_path_private = key_path_private_label.cget("text")
    cipher_text_path = cipher_text_path_label.cget("text")

    encrypt_button.config(
        state=(
            tk.NORMAL
            if os.path.exists(key_path_open) and os.path.exists(open_text_path)
            else tk.DISABLED
        )
    )
    decrypt_button.config(
        state=(
            tk.NORMAL
            if os.path.exists(key_path_open)
            and os.path.exists(key_path_private)
            and os.path.exists(cipher_text_path)
            else tk.DISABLED
        )
    )
    generate_keys_button.config(
        state=(
            tk.NORMAL
            if os.path.exists(key_path_open) and os.path.exists(key_path_private)
            else tk.DISABLED
        )
    )


def encrypt_text():
    log_text.delete(1.0, tk.END)
    path_to_open_text = open_text_path_label.cget("text")
    path_to_key_public = key_path_open_label.cget("text")
    path_to_save_encrypt_file = save_encrypt_path_label.cget("text")

    if not os.path.exists(path_to_open_text) or not os.path.isfile(path_to_open_text):
        messagebox.showerror("Ошибка", "Файл с текстом не существует")
        return
    if not os.path.exists(path_to_key_public) or not os.path.isfile(path_to_key_public):
        messagebox.showerror("Ошибка", "Файл с открытым ключом не существует")
        return
    try:
        with open(path_to_open_text, "rb") as f:
            open_text = f.read().decode("utf-8").lower()
            open_text = "".join(i for i in open_text if i in alphabet.ALL_CHARACTERS)
        if len(open_text) < 1:
            messagebox.showerror("Ошибка", "Файл с текстом пуст")
            return

    except ValueError as e:
        messagebox.showerror(
            "Ошибка", f"Некорректный формат данных в файле с открытым текстом: {e}"
        )
        return
    try:
        with open(path_to_key_public, "r", encoding="utf-8") as f:
            p, g, y = map(int, f.read().strip().split())
            public_key = (p, g, y)
    except ValueError as e:
        messagebox.showerror(
            "Ошибка", f"Некорректный формат данных в файле открытого ключа: {e}"
        )
        return

    if not open_text:
        messagebox.showerror("Ошибка", "Файл с текстом пуст")
        return
    if not public_key:
        messagebox.showerror("Ошибка", "Файл с открытым ключом пуст")
        return

    encrypted_text = encrypt(open_text, public_key)
    if path_to_save_encrypt_file:
        with open(path_to_save_encrypt_file, "w", encoding="utf-8") as f:
            for i in range(len(encrypted_text)):
                f.write(f"{encrypted_text[i][0]} {encrypted_text[i][1]}\n")
        messagebox.showinfo(
            "Успех", f"Зашифрованный текст сохранён в: {path_to_save_encrypt_file}"
        )
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"{encrypted_text[0]}\n{encrypted_text[1]}")


def decrypt_text():
    log_text.delete(1.0, tk.END)
    path_to_cipher_text = cipher_text_path_label.cget("text")
    path_to_key_public = key_path_open_label.cget("text")
    path_to_key_private = key_path_private_label.cget("text")
    path_to_save_decrypt_file = save_decrypt_path_label.cget("text")

    if not os.path.exists(path_to_cipher_text) or not os.path.isfile(
        path_to_cipher_text
    ):
        messagebox.showerror("Ошибка", "Файл с шифротекстом не существует")
        return
    if not os.path.exists(path_to_key_public) or not os.path.isfile(path_to_key_public):
        messagebox.showerror("Ошибка", "Файл с открытым ключом не существует")
        return
    if not os.path.exists(path_to_key_private) or not os.path.isfile(
        path_to_key_private
    ):
        messagebox.showerror("Ошибка", "Файл с приватным ключом не существует")
        return

    try:
        cipher_text = []
        with open(path_to_cipher_text, "r", encoding="utf-8") as f:
            for line in f:
                a, b = map(int, line.strip().split())
                cipher_text.append((a, b))
    except ValueError as e:
        messagebox.showerror(
            "Ошибка", f"Некорректный формат данных в файле с шифртекстом: {e}"
        )
        return

    try:
        with open(path_to_key_public, "r", encoding="utf-8") as f:
            p, g, y = map(int, f.read().strip().split())
            public_key = (p, g, y)
        with open(path_to_key_private, "r", encoding="utf-8") as f:
            private_key = int(f.read().strip())
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректный формат данных в файле ключа: {e}")
        return

    if not cipher_text:
        messagebox.showerror("Ошибка", "Файл с текстом пуст")
        return
    if not public_key:
        messagebox.showerror("Ошибка", "Файл с ключом пуст")
        return

    decrypted_text = decrypt(cipher_text, private_key, public_key)
    if path_to_save_decrypt_file:
        with open(path_to_save_decrypt_file, "wb") as f:
            f.write(decrypted_text)
        messagebox.showinfo(
            "Успех", f"Расшифрованный текст сохранён в: {path_to_save_decrypt_file}"
        )
    else:
        result_text.delete(1.0, tk.END)
        try:
            result_text.insert(tk.END, decrypted_text)
        except UnicodeDecodeError:
            messagebox.showerror(
                "Ошибка", "Не удалось декодировать расшифрованный текст"
            )


def generate_keys_action():
    log_text.delete(1.0, tk.END)
    path_to_key_public = key_path_open_label.cget("text")
    path_to_key_private = key_path_private_label.cget("text")

    if not os.path.exists(path_to_key_public) or not os.path.isfile(path_to_key_public):
        messagebox.showerror("Ошибка", "Файл с открытым ключом не существует")
        return
    if not os.path.exists(path_to_key_private) or not os.path.isfile(
        path_to_key_private
    ):
        messagebox.showerror("Ошибка", "Файл с приватным ключом не существует")
        return

    p = int(simpledialog.askstring("Введите p", "Введите простое число p:"))
    if p < 11:
        messagebox.showerror("Ошибка", "Число должно быть больше 7")
        return
    if not is_prime(p):
        messagebox.showerror("Ошибка", "Число p не является простым")
        return

    public_key, private_key = generate_keys(p)

    with open(path_to_key_public, "w", encoding="utf-8") as f:
        f.write(f"{public_key[0]}\n{public_key[1]}\n{public_key[2]}")
    with open(path_to_key_private, "w", encoding="utf-8") as f:
        f.write(str(private_key))

    messagebox.showinfo(
        "Успех",
        f"Ключи сгенерированы и сохранены в файлы: '{path_to_key_public}' и '{path_to_key_private}'",
    )
    log_text.insert(tk.END, "Ключи сгенерированы и сохранены в файлы:\n")
    log_text.insert(tk.END, f"'{path_to_key_public}' и '{path_to_key_private}'\n")


if __name__ == "__main__":
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

    key_label_open = ttk.Label(left_frame, text="Выберите файл с открытым ключом")
    key_label_open.pack(anchor="w", pady=5)
    key_button_open = ttk.Button(
        left_frame,
        text="Выбрать файл",
        command=lambda: select_file(key_path_open_label),
    )
    key_button_open.pack(anchor="w")
    key_path_open_label = ttk.Label(left_frame, text="")
    key_path_open_label.pack(anchor="w", pady=2)

    # №№№№№№№№№№№№№№№№№№№№№№№№№№№№№
    key_label_private = ttk.Label(left_frame, text="Выберите файл с приватным ключом")
    key_label_private.pack(anchor="w", pady=5)
    key_button_private = ttk.Button(
        left_frame,
        text="Выбрать файл",
        command=lambda: select_file(key_path_private_label),
    )
    key_button_private.pack(anchor="w")
    key_path_private_label = ttk.Label(left_frame, text="")
    key_path_private_label.pack(anchor="w", pady=2)

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
        "<Button-3>",
        lambda event: log_text_context_menu.post(event.x_root, event.y_root),
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

    generate_keys_button = ttk.Button(
        buttons_frame,
        text="Сгенерировать ключи",
        command=generate_keys_action,
        state=tk.DISABLED,
    )
    generate_keys_button.pack(anchor="w", pady=10)

    encrypt_button = ttk.Button(
        buttons_frame, text="Зашифровать", command=encrypt_text, state=tk.DISABLED
    )
    encrypt_button.pack(anchor="w", pady=10)

    decrypt_button = ttk.Button(
        buttons_frame, text="Расшифровать", command=decrypt_text, state=tk.DISABLED
    )
    decrypt_button.pack(anchor="w", pady=10)

    root.mainloop()
