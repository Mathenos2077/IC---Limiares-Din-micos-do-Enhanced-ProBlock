from ic_data_models.saida import limiarScore_podado
from ic_data_models.saida import limiarScore_nao_podado
from ic_data_models.saida import limiarScore_podado_v2
from ic_data_models.saida import limiarScore_nao_podado_v2
from ic_data_models.entradas.IC import ic_calculo as icCalc

def add_fact_checker(fact_checkers, coScore:float, subjectScore:float, avaliacao:float):
    """
    Adiciona as informações necessárias sobre a avaliação sobre uma notócia de um fact-checker em um array de fact-checkers
    relacionado a mesma notícia
    
    :param fact_checkers: array de avaliações de fact-checkers
    :param coScore: pontuação coEscore do fact-checker no momento da avaliação
    :type coScore: float
    :param subjectScore: pontuação subjectScore do fact-checker para a avaliação em questão
    :type subjectScore: float
    :param avaliacao: avaliação do fact-checker para a avaliação em questão.
        -2 =  Conteúdo notoriamente inverídico;
        -1 =  Conteúdo sugestivamente inverídico;
        0 =  Inconclusivo;   
        1 =  Conteúdo sugestivamente verídico;
        2 =  Conteúdo notoriamente verídico
    :type avaliacao: float
    """
    fact_checker = {
        "coScore":     coScore, # coScore, 0 a 1
        "subjectScore": subjectScore, # subjectScore, 0 a 1
        "avaliacao":         avaliacao 
    }
    fact_checkers.append(fact_checker)

def get_limiarScore(fact_checkers, model="podado"):
    """
    Calcula e exibe o limiarScore final com base nas avaliações fornecidas e no modelo escolhido.

    :param fact_checkers: Lista contendo os dicionários de avaliação de cada fact-checker.
    :param model: String que determina qual modelo de cálculo será utilizado.
                  Valores aceitos:
                  - 'podado': Modelo original com regras podadas (padrão).
                  - 'nao_podado': Modelo original completo.
                  - 'podado_v2': Versão 2 do modelo com regras podadas.
                  - 'nao_podado_v2': Versão 2 do modelo completo.
    """
    quantidadeAval = [
        0, # Quantidade de avaliações "conteúdo notoriamente inverídico" (-2)
        0, # Quantidade de avaliações "conteúdo sugestivamente inverídico" (-1)
        0, # Quantidade de avaliações "inconclusiva" (0)
        0, # Quantidade de avaliações "conteúdo sugestivamente verídico" (1)
        0  # Quantidade de avaliações "conteúdo notoriamente verídico" (2)
    ]

    sumCoScores = 0
    sumSubjectScores = 0

    for item in fact_checkers:
        avaliacao = item["avaliacao"]
        match avaliacao:
            case -2:
                quantidadeAval[0] +=1
            case -1:
                quantidadeAval[1] +=1
            case 0:
                quantidadeAval[2] +=1
            case 1:
                quantidadeAval[3] +=1
            case 2:
                quantidadeAval[4] +=1

        sumCoScores += item["coScore"]
        sumSubjectScores += item["subjectScore"]
    
    ic = abs(icCalc.getIC(quantidadeAval))
    coScore = sumCoScores/len(fact_checkers)
    subjectScore = sumSubjectScores/len(fact_checkers)

    if model == "podado":
        limiarScore = limiarScore_podado.getLimiarScore_Podado(coScore, ic, subjectScore)
    elif model == "nao_podado":
        limiarScore = limiarScore_nao_podado.getLimiarScore_Nao_Podado(coScore, ic, subjectScore)
    elif model == "podado_v2":
        limiarScore = limiarScore_podado_v2.getLimiarScore_Podado_v2(coScore, ic, subjectScore)
    elif model == "nao_podado_v2":
        limiarScore = limiarScore_nao_podado_v2.getLimiarScore_Nao_Podado_v2(coScore, ic, subjectScore)
    else:
        raise ValueError(f"Modelo '{model}' desconhecido. Use: 'podado', 'nao_podado', 'podado_v2' ou 'nao_podado_v2'.")

    print("índice de Convicção (IC) final: ", round(ic, 3))
    print("coScore final: ", round(coScore, 3))
    print("subjectScore final: ", round(subjectScore, 3))
    print("--------------------------------------------------")
    print("limiarScore final: ", limiarScore)

