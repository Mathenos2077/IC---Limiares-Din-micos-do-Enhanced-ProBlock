import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

confidenceScore = np.linspace(0, 1, 101)

sigma = np.abs(0.50 - 0.00) / (2 * np.sqrt(2 * np.log(2)))
print("sigma: ", sigma)
naoConfiavel = fuzz.gaussmf(confidenceScore, 0.00, sigma)
neutro = fuzz.gaussmf(confidenceScore, 0.50, sigma)
confiavel = fuzz.gaussmf(confidenceScore, 1.00, sigma)

plt.figure(figsize=(8, 5))
plt.plot(confidenceScore, naoConfiavel, "r", label="Não Confiável")
plt.plot(confidenceScore, neutro, "y", label="Confiável")
plt.plot(confidenceScore, confiavel, "g", label="Muito Confiável")
plt.title("Funções de pertinência do confidenceScore (entrada)")
plt.xlabel("confidenceScore")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.show()