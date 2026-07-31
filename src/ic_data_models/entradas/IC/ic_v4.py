import numpy as np
### Calcula o IC - Índice de Convicção

def getIC_v4(newsVoteArray, subjectScoreArray, min=0.5, max=1.5, square=True):
    pontuacaoAval = [0, 0, 0, 0, 0]
    
    def calcular_valor(subjectScore, min, max):
        return min + ((subjectScore - 1) / 4) * (max - min)

    for i in range(len(newsVoteArray)):
        if newsVoteArray[i] == -2:
            pontuacaoAval[0] += calcular_valor(subjectScoreArray[i], min, max)
        elif newsVoteArray[i] == -1:
            pontuacaoAval[1] += calcular_valor(subjectScoreArray[i], min, max)
        elif newsVoteArray[i] == 0:
            pontuacaoAval[2] += calcular_valor(subjectScoreArray[i], min, max)
        elif newsVoteArray[i] == 1:
            pontuacaoAval[3] += calcular_valor(subjectScoreArray[i], min, max)
        elif newsVoteArray[i] == 2:
            pontuacaoAval[4] += calcular_valor(subjectScoreArray[i], min, max)

    valores = [
        -2,      ### Conteúdo Notoriamente Verídico (-2)
        -1,   ### Conteúdo Sugestivamente Verídico (-1)
        0,       ### Inconclusivo (0)
        1,    ### Conteúdo Sugestivamente Inverídico (1)
        2,       ### Conteúdo Notoriamente Inverídico (2)
    ]

    ### Calcula uma média ponderada, usando a qtdVotos como peso
    votosFinal = []

    if square == True:
        for i in range(5):
            votosFinal.append(np.square(pontuacaoAval[i]) * valores[i])

        n = 0
        for i in range(len(pontuacaoAval)):
            n += np.square(pontuacaoAval[i])
        
        ic = sum(votosFinal) / n
    else:
        for i in range(5):
            votosFinal.append(pontuacaoAval[i] * valores[i])

        ic = sum(votosFinal) / sum(pontuacaoAval)
     
    return abs(ic/2)



if __name__ == "__main__":

    newsVoteArray = np.array([2, 2, 2, 2, -2, -2])
    subjectScoreArray = np.array([1, 1, 1, 1, 5, 5])
    IC = getIC_v4(newsVoteArray, subjectScoreArray, min=0.9, max=1.1, square=True)

    print("IC: ", IC)
        