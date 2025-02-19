from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random
import string

ALL_CHARACTERS = (
    +"АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + string.digits + string.punctuation
)


def generate_keys(bit_length=2048):
    p = getPrime(bit_length)
    g = random.randint(2, p - 2)
    x = random.randint(1, p - 2)
    y = pow(g, x, p)
    return (p, g, y), x


def encrypt(message, public_key):
    p, g, y = public_key
    k = random.randint(1, p - 2)
    a = pow(g, k, p)
    b = (bytes_to_long(message) * pow(y, k, p)) % p
    return a, b


def decrypt(ciphertext, private_key, public_key):
    p, g, y = public_key
    a, b = ciphertext
    x = private_key
    m = (b * pow(a, p - 1 - x, p)) % p
    return long_to_bytes(m)


# Генерация ключей
public_key, private_key = generate_keys(100)

print(f"public {public_key}")
print(f"private {private_key}")

# Чтение файла и шифрование
with open("opentext.txt", "rb") as file:
    message = file.read()
ciphertext = encrypt(message, public_key)


# Расшифровка сообщения
decrypted_message = decrypt(ciphertext, private_key, public_key)


print("Зашифрованное сообщение:", ciphertext)
print("Расшифрованное сообщение:", decrypted_message)

decrypted_message_text = decrypted_message.decode("utf-8")
print("Расшифрованное сообщение (текст):", decrypted_message_text)
