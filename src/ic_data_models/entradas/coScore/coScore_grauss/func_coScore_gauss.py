import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

coScore = np.linspace(0, 1, 101)

sigma = np.abs(0.50 - 0.25) / (2 * np.sqrt(2 * np.log(2)))
print("sigma: ", sigma)
muitoIncoerente = fuzz.gaussmf(coScore, 0.00, sigma)
incoerente = fuzz.gaussmf(coScore, 0.25, sigma)
neutro = fuzz.gaussmf(coScore, 0.50, sigma)
coerente = fuzz.gaussmf(coScore, 0.75, sigma)
muitoCoerente = fuzz.gaussmf(coScore, 1.00, sigma)

plt.figure(figsize=(8, 5))
plt.plot(coScore, muitoIncoerente, "r", label="Muito incoerente")
plt.plot(coScore, incoerente, "y", label="Incoerente")
plt.plot(coScore, neutro, "b", label="Neutro")
plt.plot(coScore, coerente, "c", label="Coerente")
plt.plot(coScore, muitoCoerente, "g", label="Muito Coerente")
plt.title("Funções de pertinência do CoScore (saída)")
plt.xlabel("coScore")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()
