def getCoScoreDireto(assertLevel, confidence):
    """
    Calcula o coScore substituindo o modelo fuzzy por um mapeamento direto (look-up table).
    As saídas mapeiam as mesmas regras baseadas em consequentes de 0.00 a 1.00 do modelo fuzzy original.
    
    :param assertLevel: Nível de acerto do avaliador (1, 2, 3, 4, 5)
                        1 = erroGravíssimo, 2 = erroGrave, 3 = erroRazoável, 
                        4 = acertoRazoável, 5 = acertoCompleto
    :param confidence: Nível de confiança do avaliador (0.9, 1.0, 1.1)
                       0.9 = naoConfiante, 1.0 = neutro, 1.1 = confiante
    :return: coScore normalizado (entre 0 e 1)
    """
    
    # Tabela de regras baseada nas regras fuzzy originais do calculo_coScore.py
    # (assertLevel_idx, confidence_idx) -> coScore
    # CoScores: c0 = 0.00, c1 = 0.25, c2 = 0.50, c3 = 0.75, c4 = 1.00
    
    regras = {
        # assertLevel 1 (erroGravíssimo)
        (1, 0.9): 0.25, # coEscoreC[1]
        (1, 1.0): 0.00, # coEscoreC[0]
        (1, 1.1): 0.00, # coEscoreC[0]
        
        # assertLevel 2 (erroGrave)
        (2, 0.9): 0.25, # coEscoreC[1]
        (2, 1.0): 0.25, # coEscoreC[1]
        (2, 1.1): 0.00, # coEscoreC[0]
        
        # assertLevel 3 (erroRazoável / intermediário)
        (3, 0.9): 0.50, # coEscoreC[2]
        (3, 1.0): 0.50, # coEscoreC[2]
        (3, 1.1): 0.25, # coEscoreC[1]
        
        # assertLevel 4 (acertoRazoável)
        (4, 0.9): 0.75, # coEscoreC[3]
        (4, 1.0): 0.75, # coEscoreC[3]
        (4, 1.1): 0.75, # coEscoreC[3]
        
        # assertLevel 5 (acertoCompleto)
        (5, 0.9): 0.75, # coEscoreC[3]
        (5, 1.0): 1.00, # coEscoreC[4]
        (5, 1.1): 1.00, # coEscoreC[4]
    }
    
    # Validação e correção (clamp) para garantir que a entrada seja segura
    a_level = int(round(assertLevel))
    a_level = max(1, min(5, a_level))
    
    # Tratamento de precisão de ponto flutuante para a chave de confidence
    conf = float(confidence)
    if conf < 0.95: 
        conf_key = 0.9
    elif conf < 1.05: 
        conf_key = 1.0
    else: 
        conf_key = 1.1
        
    return regras.get((a_level, conf_key), 0.5)

if __name__ == "__main__":
    # Teste rápido
    print("Testando cálculo de coScore direto (Tabela Base):")
    for a in [1, 2, 3, 4, 5]:
        for c in [0.9, 1.0, 1.1]:
            print(f"Assert={a}, Conf={c} -> coScore={getCoScoreDireto(a, c)}")
