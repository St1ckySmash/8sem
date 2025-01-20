import math


def encrypt(key, msg):
    key_unique = "".join(sorted(set(key), key=lambda x: key.index(x)))
    # make matrix
    num_rows = math.ceil(len(msg) / len(key_unique))
    num_columns = len(key_unique)

    matrix = [""] * num_rows
    for i in range(len(msg)):
        row = i // num_columns
        matrix[row] += msg[i]
    print(matrix)


encrypt("зелень", "зашифрованныйтекст")
