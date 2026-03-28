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
N = 5  # Número de fact-checkers (participantes)
MODELS_TO_COMPARE = ["podado_v1", "nao_podado_v1", "podado_v2", "nao_podado_v2"] # Modelos a serem comparados

print("=== Simulação de Comparação de Modelos ===")
print(f"Número de Fact-Checkers: {N}")
print(f"Modelos selecionados: {', '.join(MODELS_TO_COMPARE)}")
print("-" * 60)

# --- Geração de Avaliadores e Votos ---
factCheckers = []
weightedVotes = []

subjectScoreArray = []
coScoreArray = []
newsVoteArray = []

print("Gerando avaliadores aleatórios...")
for i in range(N):
    # Parâmetros aleatórios conforme simulacao_extendida.py
    expScoreEstatico = random.randint(2, 8)
    freqScore = random.uniform(0, 2)
    accScore = random.uniform(0, 8)
    subjectScore = random.uniform(1, 5)
    newsVote = random.randint(-2, 2)
    confidenceScore = random.randint(1, 3)
    coScoreMedio = random.uniform(0, 1)

    subjectScoreArray.append(subjectScore)
    coScoreArray.append(coScoreMedio)
    newsVoteArray.append(newsVote)

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
    print(f"CDF calculado da rodada: {cdf}")
    print(f"IC calculado na rodada: {utils.getIC(newsVoteArray)}")
    print(f"coScoreTotal calculado na rodada: {utils.getCoScore(coScoreArray)}")
    print(f"subjectScoreTotal calculado na rodada: {utils.getSubjectScore(subjectScoreArray)}")
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