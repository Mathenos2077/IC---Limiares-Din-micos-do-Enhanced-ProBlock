from utils import FactChecker
import utils
import numpy as np
from scipy.stats import norm
import random
import matplotlib.pyplot as plt

# Configurações da Simulação
N = 5  # Número de avaliadores por rodada
M = 100 # Número de rodadas
DETALHAR_RODADAS = True # Se True, imprime os detalhes de cada avaliador em cada rodada
APENAS_DIVERGENTES = True # Se True, mostra apenas rodadas com divergência de conclusividade
SALVAR_RESULTADOS = True # Se True, salva os resultados das avaliações e divergências em .txt
MODELO_BASE = "nao_podado_v3" # Modelo base para comparação
MODELOS_PARA_TESTAR = ["fixo_01_09", "fixo_02_08", "fixo_0225_0775", "fixo_03_07", "fixo_04_06", "podado_v1"] # Modelos a serem testados e comparados ao base

MODELOS_TOTAIS = [MODELO_BASE] + [m for m in MODELOS_PARA_TESTAR if m != MODELO_BASE]

relatorios_modelos = {
    modelo: {
        "Conteúdo Notoriamente Inverídico": 0,
        "Conteúdo Sugestivamente Inverídico": 0,
        "Inconclusivo": 0,
        "Conteúdo Sugestivamente Verídico": 0,
        "Conteúdo Notoriamente Verídico": 0
    } for modelo in MODELOS_TOTAIS
}

if SALVAR_RESULTADOS:
    arquivo_avaliacoes = open("avaliacoes.txt", "w", encoding="utf-8")
    arquivos_divergencias = {}
    for modelo in MODELOS_PARA_TESTAR:
        if modelo != MODELO_BASE:
            arquivos_divergencias[modelo] = open(f"divergencias_{MODELO_BASE}_vs_{modelo}.txt", "w", encoding="utf-8")

print(f"Iniciando simulação com {M} rodadas e {N} avaliadores por rodada...")

for i in range(M):
    log_buffer = []
    
    def log(msg):
        log_buffer.append(msg)
        if not APENAS_DIVERGENTES and DETALHAR_RODADAS:
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

        # Normaliza o confidenceScore entre 0.9 e 1.1
        confidenceScore = 0.9 + ((confidenceScore - 1) / 2) * 0.2

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
        
        log(f"  Avaliador {j+1}: ExpEst={expScoreEstatico}, Freq={freqScore:.2f}, Acc={accScore:.2f}, Subj={subjectScore:.2f}, Vote={newsVote}, Conf={confidenceScore:.2f}, Co={coScoreMedio:.2f}, WeightedVote={weightedVotes[-1]:.2f}")

    # Calcular CDF, Parâmetros e Limiares
    if np.std(weightedVotes) == 0:
        log("  [!] Desvio padrão zero. Rodada ignorada.")
        if SALVAR_RESULTADOS:
            arquivo_avaliacoes.write("\n".join(log_buffer) + "\n\n")
        continue

    cdf = round(utils.getCDF(weightedVotes), 4)
    
    # Calcular IC, coScoreTotal e subjectScoreTotal para a rodada
    newsVoteArray = [checker.newsVote for checker in factCheckers]
    coScoreArray = [checker.coScoreMedio for checker in factCheckers]
    subjectScoreArray = [checker.subjectScore for checker in factCheckers]
    
    IC = round(utils.getIC(newsVoteArray), 4)
    coScoreTotal = round(utils.getCoScore(coScoreArray), 4)
    subjectScoreTotal = round(utils.getSubjectScore(subjectScoreArray), 4)

    log(f"  -> CDF: {cdf}")
    log(f"  -> IC: {IC}")
    log(f"  -> coScoreTotal: {coScoreTotal}")
    #   log(f"  -> subjectScoreTotal: {subjectScoreTotal}")

    conclusoes_modelos = {}

    for modelo in MODELOS_TOTAIS:
        limiarScore = round(utils.getLimiarScore(factCheckers, model=modelo), 4)
        
       # if DETALHAR_RODADAS or APENAS_DIVERGENTES:
        #    log(f"  -> LimiarScore ({modelo}): {limiarScore}")
        
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

    # Determina se houve divergência na conclusividade *entre o modelo base e os testados*
    # para decidir se a rodada deve ser exibida quando APENAS_DIVERGENTES=True.
    houve_divergencia = False
    for modelo in MODELOS_PARA_TESTAR:
        if modelo != MODELO_BASE and conclusoes_modelos[modelo] != conclusoes_modelos[MODELO_BASE]:
            houve_divergencia = True
            break
            
    for modelo in MODELOS_TOTAIS:
        log(f"  -> Conclusão {modelo}: {conclusoes_modelos[modelo]}")

    texto_rodada = "\n".join(log_buffer) + "\n"
    
    if SALVAR_RESULTADOS:
        arquivo_avaliacoes.write(texto_rodada + "\n")
        for modelo in MODELOS_PARA_TESTAR:
            if modelo != MODELO_BASE:
                if conclusoes_modelos[MODELO_BASE] != conclusoes_modelos[modelo]:
                    arquivos_divergencias[modelo].write(texto_rodada)
                    arquivos_divergencias[modelo].write(f"  -> DIVERGÊNCIA IDENTIFICADA: {MODELO_BASE} ({conclusoes_modelos[MODELO_BASE]}) vs {modelo} ({conclusoes_modelos[modelo]})\n")
                    arquivos_divergencias[modelo].write("-" * 60 + "\n\n")

    if APENAS_DIVERGENTES and houve_divergencia:
        for linha in log_buffer:
            print(linha)

# Imprimir Relatório Final
relatorio_texto = []
relatorio_texto.append("\n" + "="*40)
relatorio_texto.append("     RELATÓRIO FINAL DA SIMULAÇÃO")
relatorio_texto.append("="*40)

relatorio_texto.append(f"\nTotal de Rodadas: {M}")
relatorio_texto.append(f"Avaliadores por Rodada: {N}")

for modelo in MODELOS_TOTAIS:
    relatorio_texto.append(f"\n---------------   MODELO: {modelo.upper()}   -----------------------")
    for k, v in relatorios_modelos[modelo].items():
        relatorio_texto.append(f"{k}: {v}")

    conclusivas_novo = sum(v for k, v in relatorios_modelos[modelo].items() if k != "Inconclusivo")
    total_novo = sum(relatorios_modelos[modelo].values())
    taxa_novo = conclusivas_novo / total_novo if total_novo > 0 else 0
    relatorio_texto.append(f"Taxa de Conclusão: {taxa_novo:.2f}")

relatorio_texto.append("--------------------------------------------------------------")

texto_final = "\n".join(relatorio_texto)
print(texto_final)

if SALVAR_RESULTADOS:
    with open("relatorio_final.txt", "w", encoding="utf-8") as f_relatorio:
        f_relatorio.write(texto_final + "\n")

    arquivo_avaliacoes.close()
    for f in arquivos_divergencias.values():
        f.close()
