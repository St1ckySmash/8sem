import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Определяем параметры
N = 10
b_values = [0.1, 0.5, 1.0]

# Исходное значение
x0 = 0.01


# Дифференциальное уравнение
def population_model(x, t, b):
    dxdt = (b * x**2) / (N + x)
    return dxdt


# Временной интервал
t = np.linspace(0, 50, 500)

# Построение графика для разных значений b
plt.figure(figsize=(10, 6))

for b in b_values:
    sol = odeint(population_model, x0, t, args=(b,))
    plt.plot(t, sol, label=f"b = {b}")

plt.xlabel("Время (t)")
plt.ylabel("Число особей (x)")
plt.title("Зависимость числа особей от времени")
plt.legend()
plt.grid(True)
plt.show()
