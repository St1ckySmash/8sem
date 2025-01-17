import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# Дифференциальное уравнение
def population_growth(t, x, b, N):
    return (b * x**2) / (N + x)


# Параметры
N = 100
b_values = [1, 2]
x0 = 2  # начальное условие

# Время для решения
t_span = (0, 30)
t_eval = np.linspace(t_span[0], t_span[1], 400)

# Решение уравнения и построение графиков
plt.figure(figsize=(10, 6))

for b in b_values:
    sol = solve_ivp(population_growth, t_span, [x0], args=(b, N), t_eval=t_eval)
    plt.plot(sol.t, sol.y[0], label=f"b = {b}")

plt.title("График зависимости x от времени t при различных значениях b")
plt.xlabel("Время t")
plt.ylabel("Число особей x")
plt.legend()
plt.grid(True)
plt.show()
