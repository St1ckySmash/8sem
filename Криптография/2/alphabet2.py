import string

ALL_CHARACTERS = (
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + string.digits + string.punctuation
)

CHAR_TO_NUM = {
    # Кириллица (11-49, последняя цифра ≠ 0)
    "а": 11,
    "б": 12,
    "в": 13,
    "г": 14,
    "д": 15,
    "е": 16,
    "ё": 17,
    "ж": 18,
    "з": 19,
    "и": 21,
    "й": 22,
    "к": 23,
    "л": 24,
    "м": 25,
    "н": 26,
    "о": 27,
    "п": 28,
    "р": 29,
    "с": 31,
    "т": 32,
    "у": 33,
    "ф": 34,
    "х": 35,
    "ц": 36,
    "ч": 37,
    "ш": 38,
    "щ": 39,
    "ъ": 41,
    "ы": 42,
    "ь": 43,
    "э": 44,
    "ю": 45,
    "я": 46,
    # Цифры (49, 51-59)
    "0": 49,
    "1": 51,
    "2": 52,
    "3": 53,
    "4": 54,
    "5": 55,
    "6": 56,
    "7": 57,
    "8": 58,
    "9": 59,
    # Пунктуация (61-98)
    "!": 61,
    '"': 62,
    "#": 63,
    "$": 64,
    "%": 65,
    "&": 66,
    "'": 67,
    "(": 68,
    ")": 69,
    "*": 71,
    "+": 72,
    ",": 73,
    "-": 74,
    ".": 75,
    "/": 76,
    ":": 77,
    ";": 78,
    "<": 79,
    "=": 81,
    ">": 82,
    "?": 83,
    "@": 84,
    "[": 85,
    "\\": 86,
    "]": 87,
    "^": 88,
    "_": 89,
    "`": 91,
    "{": 92,
    "|": 93,
    "}": 94,
}

NUM_TO_CHAR = {v: k for k, v in CHAR_TO_NUM.items()}


def char_to_number(char):
    return CHAR_TO_NUM.get(char)


def number_to_char(number):
    return NUM_TO_CHAR.get(number, "�")


def string_to_numbers(input_string):
    return [char_to_number(c) for c in input_string if c in CHAR_TO_NUM]


def numbers_to_string(input_numbers):
    return [number_to_char(n) for n in input_numbers if n in NUM_TO_CHAR]


def split_to_blocks(numbers, p):
    digits = "".join(str(n) for n in numbers)
    blocks = []
    current = ""

    for d in digits:
        current += d
        if int(current) >= p:
            blocks.append(int(current[:-1]))
            current = d

    if current:
        blocks.append(int(current))

    return blocks


def split_to_two_digits(numbers):
    # Объединяем все числа в одну строку
    combined = "".join(str(num) for num in numbers)
    # Разбиваем строку на двузначные блоки
    result = [int(combined[i : i + 2]) for i in range(0, len(combined), 2)]
    return result


# Пример использования
# numbers = [131, 316, 151, 626, 211, 613, 232, 921, 283, 227, 142, 911, 342, 145]
# blocks = split_to_two_digits(numbers)
# print(blocks)
# # Пример использования
# test_str = "введение012"
# nums = string_to_numbers(test_str)
# print("Коды символов:", nums)
# # [13, 16, 13, 16, 51, 32, 21, 16, 49, 51, 52]

# p = 11
# print("Блоки для p=200:", split_to_blocks(nums, p))
# # [131, 61, 31, 65, 13, 21, 64, 95, 13, 21, 64]

# p = 20000000
# print("Блоки для p=200:", split_to_blocks(nums, p))
