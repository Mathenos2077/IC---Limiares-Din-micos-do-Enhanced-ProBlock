def getLimiaresDinamicos(limiarScore):
    """
    Calcula os 4 limites dinâmicos para a variável CDF baseados no limiarScore.
    
    :param limiarScore: Valor do limiar (entre 0 e 1) que define o tamanho do intervalo "inconclusivo".
    :return: Tupla com (limDownEx, limDown, limUp, limUpEx)
    """
    # O centro do intervalo "inconclusivo" é 0.5
    limDown = 0.5 - (limiarScore / 2)
    limUp = 0.5 + (limiarScore / 2)
    
    # Metade do intervalo inferior restante
    limDownEx = limDown / 2
    
    # Metade do intervalo superior restante
    limUpEx = limUp + ((1 - limUp) / 2)
    
    return limDownEx, limDown, limUp, limUpEx

if __name__ == "__main__":
    # Teste rápido
    ls = 0.2
    print(f"Limiar Score: {ls}")
    print(f"Limites gerados: {getLimiaresDinamicos(ls)}")
