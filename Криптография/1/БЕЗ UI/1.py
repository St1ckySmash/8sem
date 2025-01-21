import os
import cipher


def check_encrypt_files():
    while True:
        path_to_open_text = input("Путь к файлу с открытым текстом:")
        if os.path.exists(path_to_open_text) and os.path.isfile(path_to_open_text):
            break
        else:
            print("Такой директории не существует")

    while True:
        path_to_key = input("Путь к файлу с ключом:")
        if os.path.exists(path_to_key) and os.path.isfile(path_to_key):
            break
        else:
            print("Такого файла не существует")

    return path_to_open_text, path_to_key


def check_decrypt_files():
    while True:
        path_to_cipher_text = input("Путь к файлу с шифртекстом:")
        if os.path.exists(path_to_cipher_text) and os.path.isfile(path_to_cipher_text):
            break
        else:
            print("Такой директории не существует")

    while True:
        path_to_key = input("Путь к файлу с ключом:")
        if os.path.exists(path_to_key) and os.path.isfile(path_to_key):
            break
        else:
            print("Такого файла не существует")

    return path_to_cipher_text, path_to_key


def start_program():
    mode = input("Зашифровать/Расшифровать 1/2:").replace(" ", "")

    if mode == "1":
        path_to_open_text, path_to_key = check_encrypt_files()
        with open(path_to_open_text, encoding="utf-8") as f:
            open_text = f.read()
        with open(path_to_key, encoding="utf-8") as f:
            key = f.read()

        open_text = open_text.replace(" ", "")
        if open_text == "":
            print("файл с текстом пуст")
            return

        key = key.replace(" ", "")
        if key == "":
            print("файл с ключом пуст")
            return

        encrypted_text = cipher.encrypt(open_text, key)
        print(f"Зашифрованный текст: {encrypted_text}")

    elif mode == "2":
        path_to_cipher_text, path_to_key = check_decrypt_files()
        with open(path_to_cipher_text, encoding="utf-8") as f:
            cipher_text = f.read()
        with open(path_to_key, encoding="utf-8") as f:
            key = f.read()

        cipher_text = cipher_text.replace(" ", "")
        if cipher_text == "":
            print("файл с текстом пуст")
            return

        key = key.replace(" ", "")
        if key == "":
            print("файл с ключом пуст")
            return

        decrypted_text = cipher.decrypt(cipher_text, key)
        print(f"Зашифрованный текст: {decrypted_text}")


start_program()
