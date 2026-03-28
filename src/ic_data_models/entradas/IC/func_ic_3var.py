import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

ic = np.linspace(0, 1, 101)

g = 0.250
sigma = np.abs(2*g) / (2 * np.sqrt(2 * np.log(2)))
inconvicto = fuzz.gaussmf(ic, 0*g, sigma)
intermediario = fuzz.gaussmf(ic, 2*g, sigma)
convicto = fuzz.gaussmf(ic, 4*g, sigma)


plt.figure(figsize=(8, 5))
plt.plot(ic, inconvicto, "r", label="Inconvicto")
plt.plot(ic, intermediario, "y", label="Intermediario")
plt.plot(ic, convicto, "g", label="Convicto")
plt.title("Funções de pertinência do índice de convicção (entrada)")
plt.xlabel("ic")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()
