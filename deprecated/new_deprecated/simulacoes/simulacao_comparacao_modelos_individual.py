import sys
import os
import random
import numpy as np

# Adiciona o diretório 'src' ao sys.path para permitir importações absolutas
# Assume que este arquivo está em src/ic_data_models/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from ic_data_models.simulacao_cdf.utils import FactChecker
import ic_data_models.simulacao_cdf.utils as utils

# --- Configurações ---
#MODELS_TO_COMPARE = ["podado_v1", "nao_podado_v1", "podado_v2", "nao_podado_v2"] # Modelos a serem comparados
MODELS_TO_COMPARE = ["podado_v1", "podado_v2"] # Modelos a serem comparados

print("=== Simulação de Comparação de Modelos ===")
print(f"Número de Fact-Checkers: {5}")
print(f"Modelos selecionados: {', '.join(MODELS_TO_COMPARE)}")
print("-" * 60)

# --- Geração de Avaliadores e Votos ---
factCheckers = []
weightedVotes = []

'''
expScoreEstaticoArray =  [2, 6, 1, 7, 1] # 2 a 8 (int)
freqScoreArray =         [2, 2, 2, 0, 0] # 0 a 2 (float)
accScoreArray =          [8, 8, 8, 8, 8] # 0 a 8 (float)
subjectScoreArray =      [1, 1, 1, 1, 1] # 1 a 5 (float)
newsVoteArray =          [-1, 2, 2, 2, -2] # -2 a 2 (int)
confidenceScoreArray =   [2, 2, 1, 1, 2] # 1 a 3 (int)
coScoreMedioArray =      [1, 1, 1, 1, 1] # 0 a 1 (float)
'''

expScoreEstaticoArray =  [6, 6, 1, 0, 0] # 2 a 8 (int)
freqScoreArray =         [2, 2, 2, 1, 1] # 0 a 2 (float)
accScoreArray =          [8, 8, 8, 8, 8] # 0 a 8 (float)
subjectScoreArray =      [1, 1, 1, 1, 1] # 1 a 5 (float)
newsVoteArray =          [-1, 0, 2, -1, 1] # -2 a 2 (int)
confidenceScoreArray =   [1, 2, 3, 2, 3] # 1 a 3 (int)
coScoreMedioArray =      [1, 1, 1, 1, 1] # 0 a 1 (float)


for i in range(len(expScoreEstaticoArray)):
    # Parâmetros aleatórios conforme simulacao_extendida.py
    expScoreEstatico = expScoreEstaticoArray[i]
    freqScore = freqScoreArray[i]
    accScore = accScoreArray[i]
    subjectScore = subjectScoreArray[i]
    newsVote = newsVoteArray[i]
    confidenceScore = confidenceScoreArray[i]
    coScoreMedio = coScoreMedioArray[i]

    checker = FactChecker(
        expScoreEstatico,
        freqScore,
        accScore,
        subjectScore,
        newsVote,
        confidenceScore,
        coScoreMedio
    )
    factCheckers.append(checker)
    weightedVotes.append(checker.getWeightedVote())
    
    print(f"  Avaliador {i+1}: Vote={newsVote}, Conf={confidenceScore}, Exp={expScoreEstatico}, Acc={accScore:.2f}, Subj={subjectScore:.2f}, Co={coScoreMedio:.2f} => WeightedVote={checker.getWeightedVote():.4f}")

# --- Cálculo do CDF ---
if len(weightedVotes) > 0 and np.std(weightedVotes) > 0:
    cdf = round(utils.getCDF(weightedVotes), 4)
    print("-" * 60)
    print(f"CDF: {cdf}")
    print(f"IC: {utils.getIC(newsVoteArray)}")
    print(f"coScoreTotal: {utils.getCoScore(coScoreMedioArray)}")
    print(f"subjectScoreTotal: {utils.getSubjectScore(subjectScoreArray)}")
    print("-" * 60)

    # --- Comparação dos Modelos ---
    print(f"{'MODELO':<20} | {'LIMIAR SCORE':<12} | {'CONCLUSÃO'}")
    print("-" * 70)

    for model in MODELS_TO_COMPARE:
        try:
            limiarScore = round(utils.getLimiarScore(factCheckers, model=model), 4)
            
            # Cálculo dos intervalos (Limiares)
            limDown = round(limiarScore / 2, 2)
            limDownEx = round(limDown / 2, 2)
            limUp = round(1 - (limiarScore / 2), 2)
            limUpEx = round((1 + limUp) / 2, 2)

            conclusao = "Indefinido"
            if 0 <= cdf <= limDownEx:
                conclusao = "Conteúdo Notoriamente Inverídico"
            elif limDownEx < cdf <= limDown:
                conclusao = "Conteúdo Sugestivamente Inverídico"
            elif limDown < cdf <= limUp:
                conclusao = "Inconclusivo"
            elif limUp < cdf <= limUpEx:
                conclusao = "Conteúdo Sugestivamente Verídico"
            elif limUpEx < cdf <= 1:
                conclusao = "Conteúdo Notoriamente Verídico"
            
            print(f"{model:<20} | {limiarScore:<12} | {conclusao}")

        except Exception as e:
            print(f"{model:<20} | {'Erro':<12} | {e}")

else:
    print("\n[!] Não foi possível calcular o CDF (desvio padrão zero ou sem votos).")
    print("Tente rodar novamente.")

print("-" * 70)