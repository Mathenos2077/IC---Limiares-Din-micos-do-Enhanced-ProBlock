import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

confidenceScoreL = np.linspace(0, 1, 101)

naoConfiavel = fuzz.trimf(confidenceScoreL, [-0.5, 0, 0.5])
neutro = fuzz.trimf(confidenceScoreL, [0.0, 0.5, 1])
confiavel = fuzz.trimf(confidenceScoreL, [0.5, 1, 1.5])

plt.figure(figsize=(8, 5))
plt.plot(confidenceScoreL, naoConfiavel, "r", label="Não Confiável")
plt.plot(confidenceScoreL, neutro, "y", label="Confiável")
plt.plot(confidenceScoreL, confiavel, "g", label="Muito Confiável")
plt.title("Funções de pertinência do confidenceScore (antecedente)")
plt.xlabel("confidenceScore")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.show()