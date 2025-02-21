import string

ALL_CHARACTERS = (
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + string.digits + string.punctuation
)

# Создаем константы для соответствия символов и чисел
CHAR_TO_NUM = {
    **{
        char: index
        for index, char in enumerate("абвгдеёжзийклмнопрстуфхцчшщъыьэюя", start=11)
    },
    **{char: index for index, char in enumerate(string.digits, start=50)},
    **{char: index for index, char in enumerate(string.punctuation, start=60)},
}

NUM_TO_CHAR = {v: k for k, v in CHAR_TO_NUM.items()}


# Функции для преобразования символов и чисел
def char_to_number(char):
    return CHAR_TO_NUM.get(char)


def number_to_char(number):
    return NUM_TO_CHAR.get(number)


for i in range(11, 93):
    print(i, number_to_char(i))
