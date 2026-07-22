import numpy as np
### Calcula o IC - Índice de Convicção

def getIC(quantidadeAval, square=True):
    """
    Retorna o índice de convicção (IC) calculado a partir da quantidade de cada um dos tipos de votos na avaliação
    
    :param quantidadeAval: array com a quantidade de cada tipo de avaliação, mapeados da seguinte forma:
        quantidadeAval[0] - Quantidade de avaliações "conteúdo notoriamente inverídico" (-2)
        quantidadeAval[1] - Quantidade de avaliações "conteúdo sugestivamente inverídico" (-1)
        quantidadeAval[2] - Quantidade de avaliações "inconclusiva" (0)
        quantidadeAval[3] - Quantidade de avaliações "conteúdo sugestivamente verídico" (1)
        quantidadeAval[4] - Quantidade de avaliações "conteúdo notoriamente verídico" (2)
    """

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
            votosFinal.append(np.square(quantidadeAval[i]) * valores[i])

        n = 0
        for i in range(len(quantidadeAval)):
            n += np.square(quantidadeAval[i])
        
        ic = sum(votosFinal) / n
    else:
        for i in range(5):
            votosFinal.append(quantidadeAval[i] * valores[i])

        ic = sum(votosFinal) / sum(quantidadeAval)
     
    return abs(ic/2)



if __name__ == "__main__":
    print(abs(getIC([
        0,     ###  (-2) Quantidade de avaliações "conteúdo notoriamente inverídico"
        0,      ### (-1) Quantidade de avaliações "conteúdo sugestivamente inverídico"
        0,      ### (0) Quantidade de avaliações "inconclusiva"
        0,      ### (1) Quantidade de avaliações "conteúdo sugestivamente verídico"
        0       ### (2) Quantidade de avaliações "conteúdo notoriamente verídico"
        ], True)))