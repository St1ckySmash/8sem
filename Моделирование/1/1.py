import numpy as np
import matplotlib.pyplot as plt

# Определяем параметры
N = 100
b_values = [0.7, 1, 0.5]

# Исходное значение
x0 = 0.1

# Временной интервал
t = np.linspace(0, 2100, 1000)
dt = t[1] - t[0]


# Дифференциальное уравнение
def population_model(x, b):
    dxdt = (b * x * x) / (N + x)
    return dxdt


# Метод Эйлера
def euler_method(x0, t, b):
    x = np.zeros(len(t))
    x[0] = x0
    for i in range(1, len(t)):
        x[i] = x[i - 1] + population_model(x[i - 1], b) * dt
    return x


# Построение графика для разных значений b
plt.figure(figsize=(10, 6))

for b in b_values:
    sol = euler_method(x0, t, b)
    plt.plot(t, sol, label=f"b = {b}")

plt.ylim((-1, 100))
plt.xlabel("Время (t)")
plt.ylabel("Число особей (x)")
plt.title("Зависимость числа особей от времени (Метод Эйлера)")
plt.legend()
plt.grid(True)
plt.show()
