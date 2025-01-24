import math
import random
import string

# Удалить английские символы, не добивать таблицу случайными значениями
ALL_CHARACTERS = (
    "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    + "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower()
    + string.digits
    + string.punctuation
)


def random_char_or_digit():
    russian_letters_upper = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    russian_letters_lower = russian_letters_upper.lower()
    all_characters = (
        russian_letters_upper
        + russian_letters_lower
        + string.digits
        + string.punctuation
    )
    return random.choice(all_characters)


def create_matrix(text, key, num_columns, num_rows, logger=print):
    matrix = [""] * num_rows
    for i in range(len(text)):
        row = i // num_columns
        matrix[row] += text[i]
    while len(matrix[-1]) < num_columns:
        matrix[-1] += random_char_or_digit()
    logger("Созданная матрица:")
    for s in matrix:
        logger(s)
    return matrix


def encrypt(text, key, logger=print):
    text = text.replace(" ", "")
    key = key.replace(" ", "")

    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(text) / num_columns)

    matrix = create_matrix(text, key, num_columns, num_rows, logger)

    transposed = sorted(zip(key_unique, range(num_columns)))
    logger("Сортировка ключа и индексы столбцов:")
    logger(transposed)

    encrypted_text = ""
    for _, col in transposed:
        for row in matrix:
            encrypted_text += row[col]
    return encrypted_text


def decrypt(cipher, key, logger=print):
    key = key.replace(" ", "")
    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(cipher) / num_columns)

    transposed = sorted(zip(key_unique, range(num_columns)))
    logger("Сортировка ключа и индексы столбцов:")
    logger(transposed)

    matrix = [["" for _ in range(num_columns)] for _ in range(num_rows)]

    for i in range(num_columns):
        _, col = transposed[i]
        for j in range(num_rows):
            matrix[j][col] = cipher[j + i * num_rows]

    decrypted_text = ""
    logger("Созданная матрица:")
    for i in range(len(matrix)):
        s = ""
        for el in matrix[i]:
            s += el
        logger(s)
        decrypted_text += s

    return decrypted_text
