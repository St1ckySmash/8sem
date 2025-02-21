import random
from sympy import isprime, primefactors
from Crypto.Util.number import getPrime
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

msg = "вв"
print(bytes_to_long(msg.encode("utf-8")))
print(msg)
print(msg.encode("utf-8"))

msg = "вв"
encoded_msg = msg.encode("utf-8")

# Вывод байтового представления строки в виде битов
bits = "".join(f"{byte:08b}" for byte in encoded_msg)
print(bits)
