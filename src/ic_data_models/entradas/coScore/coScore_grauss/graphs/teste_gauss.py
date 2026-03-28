import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

accLevel = np.linspace(0, 1, 101)


sigma = 0.15
y = fuzz.gaussmf(accLevel, 0.5, sigma)


plt.figure(figsize=(8, 5))plt.plot(accLevel, y, "r", label="Curva Gaussiana")

plt.title("Exemplo de curva gaussiana")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()
