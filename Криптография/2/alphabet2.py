import string

ALL_CHARACTERS = (
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + string.digits + string.punctuation
)

CHAR_TO_NUM = {
    "а": 11,
    "б": 12,
    "в": 13,
    "г": 14,
    "д": 15,
    "е": 16,
    "ё": 17,
    "ж": 18,
    "з": 19,
    "и": 20,
    "й": 21,
    "к": 22,
    "л": 23,
    "м": 24,
    "н": 25,
    "о": 26,
    "п": 27,
    "р": 28,
    "с": 29,
    "т": 30,
    "у": 31,
    "ф": 32,
    "х": 33,
    "ц": 34,
    "ч": 35,
    "ш": 36,
    "щ": 37,
    "ъ": 38,
    "ы": 39,
    "ь": 40,
    "э": 41,
    "ю": 42,
    "я": 43,
    "0": 50,
    "1": 51,
    "2": 52,
    "3": 53,
    "4": 54,
    "5": 55,
    "6": 56,
    "7": 57,
    "8": 58,
    "9": 59,
    "!": 60,
    '"': 61,
    "#": 62,
    "$": 63,
    "%": 64,
    "&": 65,
    "'": 66,
    "(": 67,
    ")": 68,
    "*": 69,
    "+": 70,
    ",": 71,
    "-": 72,
    ".": 73,
    "/": 74,
    ":": 75,
    ";": 76,
    "<": 77,
    "=": 78,
    ">": 79,
    "?": 80,
    "@": 81,
    "[": 82,
    "\\": 83,
    "]": 84,
    "^": 85,
    "_": 86,
    "`": 87,
    "{": 88,
    "|": 89,
    "}": 90,
    "~": 91,
}

NUM_TO_CHAR = {v: k for k, v in CHAR_TO_NUM.items()}


def char_to_number(char):
    return CHAR_TO_NUM.get(char)


def number_to_char(number):
    return NUM_TO_CHAR.get(number)


def string_to_numbers(input_string):
    return [
        char_to_number(char)
        for char in input_string
        if char_to_number(char) is not None
    ]


def split_to_blocks(numbers, p):
    blocks = []
    current_block = []

    for num in numbers:
        if num >= p:
            if current_block:
                blocks.extend(current_block)
                current_block = []
            blocks.append(num)
        else:
            current_block.append(num)
            if int("".join(map(str, current_block))) >= p:
                current_block.pop()
                blocks.extend(current_block)
                current_block = [num]

    if current_block:
        blocks.extend(current_block)

    return blocks


# Пример использования
input_string = "введение"
numbers = string_to_numbers(input_string)
p = 17
blocks = split_to_blocks(numbers, p)
print(blocks)  # Ожидаемый вывод: [13, 13, 16, 15, 16, 2, 2, 2, 5, 16]
