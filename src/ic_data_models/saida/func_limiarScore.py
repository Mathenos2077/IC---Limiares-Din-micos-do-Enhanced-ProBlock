import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


limiarScore = np.linspace(0, 1, 1001)

'''
# Funções de pertinência abrangentes
MuitoBaixo = fuzz.trimf(limiarScore, [0, 0, 25])
Baixo = fuzz.trimf(limiarScore, [0, 25, 50])
Intermediario = fuzz.trimf(limiarScore, [25, 50, 75])
Alto = fuzz.trimf(limiarScore, [50, 75, 100])
MuitoAlto = fuzz.trimf(limiarScore, [75, 100, 100])
'''

'''
# Funções de pertinência equilibradas
MuitoBaixo = fuzz.trimf(limiarScore, [0, 0, 18.75])
Baixo = fuzz.trimf(limiarScore, [6.25, 25, 44])
Intermediario = fuzz.trimf(limiarScore, [31.5, 50, 68.75])
Alto = fuzz.trimf(limiarScore, [56.25, 75, 93.75])
MuitoAlto = fuzz.trimf(limiarScore, [81.25, 100, 100])
'''
limiarScoreC = ["extr. baixo", "muito baixo", "baixo", "levemente baixo", "intermediario", "levemente alto", "alto", "muito alto", "extr. alto"]


# Funções de pertinência restritas
g = 0.0625
sigma = np.abs(2*g) / (2 * np.sqrt(2 * np.log(2)))
print(sigma)
extrBaixo = fuzz.gaussmf(limiarScore, 0*g, sigma)
muitoBaixo = fuzz.gaussmf(limiarScore, 2*g, sigma)
baixo = fuzz.gaussmf(limiarScore, 4*g, sigma)
levBaixo = fuzz.gaussmf(limiarScore, 6*g, sigma)
inter = fuzz.gaussmf(limiarScore, 8*g, sigma)
leveAlto = fuzz.gaussmf(limiarScore, 10*g, sigma)
alto = fuzz.gaussmf(limiarScore, 12*g, sigma)
muitoAlto = fuzz.gaussmf(limiarScore, 14*g, sigma)
extrAlto = fuzz.gaussmf(limiarScore, 16*g, sigma)


plt.figure(figsize=(8, 5))
plt.plot(limiarScore, extrBaixo, "r", label="extrBaixo")
plt.plot(limiarScore, muitoBaixo, "m", label="muitoBaixo")
plt.plot(limiarScore, baixo, "y", label="baixo")
plt.plot(limiarScore, levBaixo, "b", label="levBaixo")
plt.plot(limiarScore, inter, "g", label="inter")
plt.plot(limiarScore, leveAlto, "r", label="leveAlto")
plt.plot(limiarScore, alto, "m", label="alto")
plt.plot(limiarScore, muitoAlto, "y", label="muitoAlto")
plt.plot(limiarScore, extrAlto, "b", label="extrAlto")
plt.title("Funções de pertinência do limiarScore (saída)")
plt.xlabel("limiarScore")
plt.ylabel("Grau de Pertinência")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0, 1.1, 0.1))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()