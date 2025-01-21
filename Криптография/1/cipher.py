import math


def create_matrix(text, key, num_columns, num_rows, logger=print):
    matrix = [""] * num_rows
    for i in range(len(text)):
        row = i // num_columns
        matrix[row] += text[i]
    while len(matrix[-1]) < num_columns:
        matrix[
            -1
        ] += "а"  # добавить рандом буквы тут и вообще ограничить алфавит, убирать пробелы
    logger("МАТРИЦА:\n" + "=" * len(matrix[0]))
    for s in matrix:
        logger(s)
    logger("=" * len(matrix[0]))
    return matrix


def encrypt(text, key, logger=print):
    text = text.replace(" ", "")
    key = key.replace(" ", "")

    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    num_columns = len(key_unique)
    num_rows = math.ceil(len(text) / num_columns)

    matrix = create_matrix(text, key, num_columns, num_rows, logger)

    transposed = sorted(zip(key_unique, range(num_columns)))
    logger(transposed)

    encrypted_text = ""
    for _, col in transposed:
        for row in matrix:
            if col < len(row):
                encrypted_text += row[col]
    return encrypted_text


def decrypt(cipher, key, logger=print):
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
