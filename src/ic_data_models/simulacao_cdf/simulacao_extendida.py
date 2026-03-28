from utils import FactChecker
import utils
import numpy as np
from scipy.stats import norm
import random

# Configurações da Simulação
N = 5  # Número de avaliadores por rodada
M = 200 # Número de rodadas
DETALHAR_RODADAS = True # Se True, imprime os detalhes de cada avaliador em cada rodada
APENAS_DIVERGENTES = True # Se True, mostra apenas rodadas com divergência de conclusividade
MODELOS_PARA_TESTAR = ["podado_v1", "podado_v2"] # Modelos a serem avaliados

# Contadores para os relatórios
relatorio_antigo = {
    "Conteúdo Notoriamente Inverídico": 0,
    "Inconclusivo": 0,
    "Conteúdo Notoriamente Verídico": 0
}

relatorios_modelos = {
    modelo: {
        "Conteúdo Notoriamente Inverídico": 0,
        "Conteúdo Sugestivamente Inverídico": 0,
        "Inconclusivo": 0,
        "Conteúdo Sugestivamente Verídico": 0,
        "Conteúdo Notoriamente Verídico": 0
    } for modelo in MODELOS_PARA_TESTAR
}

divergencias_modelos = {
    modelo: {
        "antigo_conclusivo_novo_inconclusivo": 0,
        "antigo_inconclusivo_novo_conclusivo": 0
    } for modelo in MODELOS_PARA_TESTAR
}

print(f"Iniciando simulação com {M} rodadas e {N} avaliadores por rodada...")

for i in range(M):
    log_buffer = []
    def log(msg):
        if APENAS_DIVERGENTES:
            log_buffer.append(msg)
        elif DETALHAR_RODADAS:
            print(msg)

    if not DETALHAR_RODADAS and not APENAS_DIVERGENTES:
        print(f"Rodada {i+1}/{M}", end='\r', flush=True)
    else:
        log(f"\n--- Rodada {i+1}/{M} ---")

    factCheckers = []
    weightedVotes = []

    # Gerar avaliadores aleatórios
    for j in range(N):
        expScoreEstatico = random.randint(2, 8)
        freqScore = random.uniform(0, 2)
        accScore = random.uniform(0, 8)
        subjectScore = random.uniform(1, 5)
        newsVote = random.randint(-2, 2)
        confidenceScore = random.randint(1, 3)
        coScoreMedio = random.uniform(0, 1)

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
        
        if DETALHAR_RODADAS or APENAS_DIVERGENTES:
            log(f"  Avaliador {j+1}: ExpEst={expScoreEstatico}, Freq={freqScore:.2f}, Acc={accScore:.2f}, Subj={subjectScore:.2f}, Vote={newsVote}, Conf={confidenceScore}, Co={coScoreMedio:.2f}, WeightedVote={weightedVotes[-1]:.2f}")

    # Calcular CDF e Limiares
    if np.std(weightedVotes) == 0:
        if DETALHAR_RODADAS or APENAS_DIVERGENTES:
            log("  [!] Desvio padrão zero. Rodada ignorada.")
        continue

    cdf = round(utils.getCDF(weightedVotes), 4)
    
    if DETALHAR_RODADAS or APENAS_DIVERGENTES:
        log(f"  -> CDF: {cdf}")

    # Classificação Modelo Antigo
    limDownAntigo = 0.225
    limUpAntigo = 0.775

    conclusao_antigo = ""
    if 0 <= cdf <= limDownAntigo:
        conclusao_antigo = "Conteúdo Notoriamente Inverídico"
    elif limDownAntigo < cdf <= limUpAntigo:
        conclusao_antigo = "Inconclusivo"
    elif limUpAntigo < cdf <= 1:
        conclusao_antigo = "Conteúdo Notoriamente Verídico"
    
    if conclusao_antigo:
        relatorio_antigo[conclusao_antigo] += 1

    conclusoes_modelos = {}

    for modelo in MODELOS_PARA_TESTAR:
        limiarScore = round(utils.getLimiarScore(factCheckers, model=modelo), 4)
        
        if DETALHAR_RODADAS or APENAS_DIVERGENTES:
            log(f"  -> LimiarScore ({modelo}): {limiarScore}")

        limDown = round(limiarScore / 2, 2)
        limDownEx = round(limDown / 2, 2)
        limUp = round(1 - (limiarScore / 2), 2)
        limUpEx = round((1 + limUp) / 2, 2)

        conclusao_modelo = ""
        if 0 <= cdf <= limDownEx:
            conclusao_modelo = "Conteúdo Notoriamente Inverídico"
        elif limDownEx < cdf <= limDown:
            conclusao_modelo = "Conteúdo Sugestivamente Inverídico"
        elif limDown < cdf <= limUp:
            conclusao_modelo = "Inconclusivo"
        elif limUp < cdf <= limUpEx:
            conclusao_modelo = "Conteúdo Sugestivamente Verídico"
        elif limUpEx < cdf <= 1:
            conclusao_modelo = "Conteúdo Notoriamente Verídico"
            
        conclusoes_modelos[modelo] = conclusao_modelo

        if conclusao_modelo:
            relatorios_modelos[modelo][conclusao_modelo] += 1

        if conclusao_antigo != "Inconclusivo" and conclusao_modelo == "Inconclusivo":
            divergencias_modelos[modelo]["antigo_conclusivo_novo_inconclusivo"] += 1
        elif conclusao_antigo == "Inconclusivo" and conclusao_modelo != "Inconclusivo":
            divergencias_modelos[modelo]["antigo_inconclusivo_novo_conclusivo"] += 1

    # Determina se houve divergência na conclusividade *entre os modelos testados*
    # para decidir se a rodada deve ser exibida quando APENAS_DIVERGENTES=True.
    # A rodada é exibida se houver tanto modelos conclusivos quanto inconclusivos.
    houve_divergencia = False
    if len(conclusoes_modelos) > 1:
        conclusividades = {c == "Inconclusivo" for c in conclusoes_modelos.values()}
        if len(conclusividades) > 1:
            houve_divergencia = True
            
    if DETALHAR_RODADAS or APENAS_DIVERGENTES:
        log(f"  -> Conclusão Antigo: {conclusao_antigo}")
        for modelo, conclusao in conclusoes_modelos.items():
            log(f"  -> Conclusão {modelo}: {conclusao}")

    if APENAS_DIVERGENTES and houve_divergencia:
        for linha in log_buffer:
            print(linha)

# Imprimir Relatório Final
print("\n" + "="*40)
print("     RELATÓRIO FINAL DA SIMULAÇÃO")
print("="*40)

print(f"\nTotal de Rodadas: {M}")
print(f"Avaliadores por Rodada: {N}")

print("\n---------------   LIMIARES ANTIGOS   -----------------------")
for k, v in relatorio_antigo.items():
    print(f"{k}: {v}")

conclusivas_antigo = sum(v for k, v in relatorio_antigo.items() if k != "Inconclusivo")
total_antigo = sum(relatorio_antigo.values())
taxa_antigo = conclusivas_antigo / total_antigo if total_antigo > 0 else 0
print(f"Taxa de Conclusão: {taxa_antigo:.2f}")

for modelo in MODELOS_PARA_TESTAR:
    print(f"\n---------------   MODELO: {modelo.upper()}   -----------------------")
    for k, v in relatorios_modelos[modelo].items():
        print(f"{k}: {v}")

    conclusivas_novo = sum(v for k, v in relatorios_modelos[modelo].items() if k != "Inconclusivo")
    total_novo = sum(relatorios_modelos[modelo].values())
    taxa_novo = conclusivas_novo / total_novo if total_novo > 0 else 0
    print(f"Taxa de Conclusão: {taxa_novo:.2f}")
    print(f"Antigo Conclusivo / Novo Inconclusivo: {divergencias_modelos[modelo]['antigo_conclusivo_novo_inconclusivo']}")
    print(f"Antigo Inconclusivo / Novo Conclusivo: {divergencias_modelos[modelo]['antigo_inconclusivo_novo_conclusivo']}")

print("--------------------------------------------------------------")
