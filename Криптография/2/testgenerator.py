import random
from sympy import isprime, primefactors
from Crypto.Util.number import getPrime


def is_primitive_root(g, p, factors, phi):
    return all(pow(g, phi // factor, p) != 1 for factor in factors)


def find_primitive_root(p):
    phi = p - 1
    factors = primefactors(phi)

    # Проверяем ограниченное количество кандидатов, чтобы избежать долгих вычислений
    for g in range(2, min(50, p)):  # Ограничиваем до 5000 кандидатов
        if is_primitive_root(g, p, factors, phi):
            return g
    return 0
    raise Exception("Примитивный корень не найден.")


def generate_keys(bit_length=2048):
    while True:
        q = getPrime(bit_length - 1)
        p = 2 * q + 1
        if isprime(p):
            break

    g = find_primitive_root(p)
    x = random.randint(2, p - 2)
    y = pow(g, x, p)

    print(f"Сгенерированные ключи:\n p = {p}\n g = {g}\n y = {y}\n x = {x}")

    return (p, g, y), x


if __name__ == "__main__":
    bit_length = 337  # Задайте нужную длину бит
    public_key, private_key = generate_keys(bit_length)
    print("Открытый ключ:", public_key)
    print("Закрытый ключ:", private_key)
