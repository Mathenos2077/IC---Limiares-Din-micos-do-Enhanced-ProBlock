import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

ic = np.linspace(0, 1, 101)

g = 0.125
sigma = np.abs(0.50 - 0.25) / (2 * np.sqrt(2 * np.log(2)))
muitoInconvicto = fuzz.gaussmf(ic, 0*g, sigma)
inconvicto = fuzz.gaussmf(ic, 2*g, sigma)
intermediario = fuzz.gaussmf(ic, 4*g, sigma)
convicto = fuzz.gaussmf(ic, 6*g, sigma)
muitoConvicto = fuzz.gaussmf(ic, 8*g, sigma)


plt.figure(figsize=(8, 5))
plt.plot(ic, muitoInconvicto, "r", label="Muito inconvicto")
plt.plot(ic, inconvicto, "y", label="Inconvicto")
plt.plot(ic, intermediario, "b", label="Intermediário")
plt.plot(ic, convicto, "c", label="Convicto")
plt.plot(ic, muitoConvicto, "g", label="Muito convicto")
plt.title("Funções de pertinência do índice de convicção (entrada)")
plt.xlabel("IC")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()
