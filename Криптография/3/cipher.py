import math
import string

ALL_CHARACTERS = (
    "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    + "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower()
    + string.digits
    + string.punctuation
    + " "
    + "—"
)


def encrypt(text_arr):
    print(text_arr)
    new_arr = [[] for _ in range(4)]

    for i, text in enumerate(text_arr):
        new_arr[i % 4].append(text)

    result = []
    result.extend(new_arr[2])
    result.extend(new_arr[3])
    result.extend(new_arr[0])
    result.extend(new_arr[1])

    return result


def decrypt(encrypted_arr):
    n = len(encrypted_arr)
    group_sizes = [(n + 3 - k) // 4 for k in range(4)]

    group2 = encrypted_arr[: group_sizes[2]]
    group3 = encrypted_arr[group_sizes[2] : group_sizes[2] + group_sizes[3]]
    group0 = encrypted_arr[
        group_sizes[2]
        + group_sizes[3] : group_sizes[2]
        + group_sizes[3]
        + group_sizes[0]
    ]
    group1 = encrypted_arr[group_sizes[2] + group_sizes[3] + group_sizes[0] :]

    result = []
    for i in range(n):
        remainder = i % 4
        group_idx = i // 4

        if remainder == 0:
            result.append(group0[group_idx])
        elif remainder == 1:
            result.append(group1[group_idx])
        elif remainder == 2:
            result.append(group2[group_idx])
        else:  # remainder == 3
            result.append(group3[group_idx])

    return result
