import math


def encrypt(text, key):
    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(text) / num_columns)

    # Заполняем матрицу символами
    matrix = [""] * num_columns
    for i, char in enumerate(text):
        matrix[i % num_columns] += char

    # Создаем кортежи (буква ключа, соответствующий столбец)
    transposed = sorted(zip(key_unique, matrix))

    # Переставляем столбцы и объединяем их в зашифрованный текст
    encrypted_text = "".join("".join(col for _, col in transposed))
    return encrypted_text


def decrypt(cipher, key):
    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(cipher) / num_columns)
    shaded_boxes = (num_columns * num_rows) - len(cipher)

    # Длина каждого столбца
    col_lengths = [num_rows] * num_columns
    for i in range(shaded_boxes):
        col_lengths[-(i + 1)] -= 1

    # Заполняем матрицу символами
    columns = [""] * num_columns
    start = 0
    for i, length in enumerate(col_lengths):
        columns[i] = cipher[start : start + length]
        start += length

    # Создаем кортежи (буква ключа, соответствующий столбец) и сортируем их
    transposed = sorted(zip(key_unique, columns))

    # Читаем текст по строкам, чтобы расшифровать его
    plaintext = ""
    for i in range(num_rows):
        for _, col in transposed:
            if i < len(col):
                plaintext += col[i]
    return plaintext


# Пример использования
text = "Привет, мир! я тут надолго ало да да во во во "
key = "кляча"

encrypted_text = encrypt(text, key)
print(f"Зашифрованный текст: {encrypted_text}")

decrypted_text = decrypt(encrypted_text, key)
print(f"Расшифрованный текст: {decrypted_text}")
