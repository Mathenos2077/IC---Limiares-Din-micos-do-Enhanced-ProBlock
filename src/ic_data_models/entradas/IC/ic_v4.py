import numpy as np
import matplotlib.pyplot as plt

### Calcula o IC - Índice de Convicção (Seu código original)
def getIC_v4(newsVoteArray, subjectScoreArray, N = 0.0, square=True):
    pontuacaoAval = [0, 0, 0, 0, 0]
    ps = (N-1)/(N + 1)
    min_val = 1 - ps
    max_val = 1 + ps

    def calcular_valor(subjectScore, min_val, max_val):
        return min_val + ((subjectScore - 1) / 4) * (max_val - min_val)

    for i in range(len(newsVoteArray)):
        if newsVoteArray[i] == -2:
            pontuacaoAval[0] += calcular_valor(subjectScoreArray[i], min_val, max_val)
        elif newsVoteArray[i] == -1:
            pontuacaoAval[1] += calcular_valor(subjectScoreArray[i], min_val, max_val)
        elif newsVoteArray[i] == 0:
            pontuacaoAval[2] += calcular_valor(subjectScoreArray[i], min_val, max_val)
        elif newsVoteArray[i] == 1:
            pontuacaoAval[3] += calcular_valor(subjectScoreArray[i], min_val, max_val)
        elif newsVoteArray[i] == 2:
            pontuacaoAval[4] += calcular_valor(subjectScoreArray[i], min_val, max_val)

    valores = [
        -2, 
        -1, 
        0, 
        1, 
        2, 
    ]

    votosFinal = []

    if square == True:
        for i in range(5):
            votosFinal.append(np.square(pontuacaoAval[i]) * valores[i])

        n = 0
        for i in range(len(pontuacaoAval)):
            n += np.square(pontuacaoAval[i])
        
        # Evita divisão por zero caso todos os pesos se anulem
        if n == 0:
            return 0
        ic = sum(votosFinal) / n
    else:
        for i in range(5):
            votosFinal.append(pontuacaoAval[i] * valores[i])
        
        soma_pontuacao = sum(pontuacaoAval)
        if soma_pontuacao == 0:
            return 0
        ic = sum(votosFinal) / soma_pontuacao
     
    return abs(ic/2)


if __name__ == "__main__":
    # Cenário de teste
    cenario_votos = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -2])
    cenario_scores = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5])
    
    print(getIC_v4(cenario_votos, cenario_scores, 20.0, square=True))