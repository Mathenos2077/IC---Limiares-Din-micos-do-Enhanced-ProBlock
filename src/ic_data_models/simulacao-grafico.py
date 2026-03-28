import saida.calculo_limiarScore as limiarScore
import matplotlib.pyplot as plt
import numpy as np


limiarScoreFinal_np = []
limiarScoreFinal_p = []

x = np.arange(0, 1, 0.01)

for i in range(101):
    print(i)
    j = i/100
    limiarScoreFinal_np.append(limiarScore.getLimiarScore_NaoPodado(j, 0, 0))
    limiarScoreFinal_p.append(limiarScore.getLimiarScore_Podado(j, 0, 0))
    

plt.figure(figsize=(8, 5))
plt.plot(limiarScoreFinal_np, x, "r", label="ls")
plt.plot(limiarScoreFinal_p, x, "g", label="lsP")
plt.title("LimiarScore")
plt.xlabel("j")
plt.ylabel("LimiarScore")
plt.legend()
plt.grid(True)
plt.xticks(np.arange(0.0, 1.01, 0.25))
plt.yticks(np.arange(0.0, 1.01, 0.25))
plt.legend(loc="best")
plt.show()