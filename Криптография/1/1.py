import math


def create_matrix(text, key, num_columns, num_rows):
    matrix = [""] * num_rows
    for i in range(len(text)):
        row = i // num_columns
        col = i % num_columns
        matrix[row] += text[i]
    return matrix


def encrypt(text, key):
    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(text) / num_columns)

    matrix = create_matrix(text, key, num_columns, num_rows)

    transposed = sorted(zip(key_unique, range(num_columns)))

    encrypted_text = ""
    for _, col in transposed:
        for row in matrix:
            if col < len(row):
                encrypted_text += row[col]
    return encrypted_text


def decrypt(cipher, key):
    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(cipher) / num_columns)
    shaded_boxes = (num_columns * num_rows) - len(cipher)

    col_lengths = [num_rows] * num_columns
    for i in range(shaded_boxes):
        col_lengths[-(i + 1)] -= 1

    columns = [""] * num_columns
    start = 0
    for i, length in enumerate(col_lengths):
        columns[i] = cipher[start : start + length]
        start += length

    sorted_key_indices = sorted(range(len(key_unique)), key=lambda k: key_unique[k])
    transposed = [""] * num_columns
    for i, idx in enumerate(sorted_key_indices):
        transposed[idx] = columns[i]

    plaintext = ""
    for r in range(num_rows):
        for col in transposed:
            if r < len(col):
                plaintext += col[r]
    return plaintext


# Пример использования
text = "Привет, мир! я тут надолго ало да да во во во "
key = "ключ"

encrypted_text = encrypt(text, key)
print(f"Зашифрованный текст: {encrypted_text}")

decrypted_text = decrypt(encrypted_text, key)
print(f"Расшифрованный текст: {decrypted_text}")
