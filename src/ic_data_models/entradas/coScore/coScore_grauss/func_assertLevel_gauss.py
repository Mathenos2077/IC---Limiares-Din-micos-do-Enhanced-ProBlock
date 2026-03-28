import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

accLevel = np.linspace(0, 1, 101)

sigma = np.abs(0.50 - 0.25) / (2 * np.sqrt(2 * np.log(2)))
print("sigma: ", sigma)
accLevel0 = fuzz.gaussmf(accLevel, 0.00, sigma)
accLevel1 = fuzz.gaussmf(accLevel, 0.25, sigma)
accLevel2 = fuzz.gaussmf(accLevel, 0.50, sigma)
accLevel3 = fuzz.gaussmf(accLevel, 0.75, sigma)
accLevel4 = fuzz.gaussmf(accLevel, 1.00, sigma)

plt.figure(figsize=(8, 5))
plt.plot(accLevel, accLevel0, "r", label="Erro Gravíssimo")
plt.plot(accLevel, accLevel1, "y", label="Erro Grave")
plt.plot(accLevel, accLevel2, "b", label="Erro Razoável")
plt.plot(accLevel, accLevel3, "c", label="Acerto Razoável")
plt.plot(accLevel, accLevel4, "g", label="Acerto Completo")
plt.title("Funções de pertinência do assertLevel (entrada)")
plt.xlabel("assertLevel")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()
