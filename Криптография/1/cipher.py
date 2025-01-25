import math
import random
import string

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


def create_matrix(text, num_columns, num_rows, logger=print):
    matrix = [""] * num_rows
    for i in range(len(text)):
        row = i // num_columns
        matrix[row] += text[i]
    logger("Созданная матрица:")
    for s in matrix:
        logger(s)
    return matrix


def encrypt(text, key, logger=print):
    logger("Ключ:")
    logger(key)

    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(text) / num_columns)

    transposed = sorted(zip(key_unique, range(num_columns)))
    logger("Сортировка ключа и индексы столбцов:")
    logger(transposed)

    matrix = create_matrix(text, num_columns, num_rows, logger)

    encrypted_text = ""
    for row in matrix:
        for _, col in transposed:
            if col < len(row):
                encrypted_text += row[col]

    return encrypted_text


def decrypt(cipher, key, logger=print):
    logger("Ключ:")
    logger(key)

    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(cipher) / num_columns)

    transposed = sorted(zip(key_unique, range(num_columns)))
    logger("Сортировка ключа и индексы столбцов:")
    logger(transposed)

    matrix = [["" for _ in range(num_columns)] for _ in range(num_rows)]

    num_readed = 0
    for i in range(num_rows):
        for j in range(num_columns):
            if num_readed < len(cipher):
                _, col = transposed[j]
                matrix[i][col] = cipher[num_readed]
                num_readed += 1

    logger("Созданная матрица:")
    for s in matrix:
        logger("".join(s))

    decrypted_text = ""
    for row in matrix:
        for j in range(num_columns):
            if row[j] != "":
                decrypted_text += row[j]

    return decrypted_text
