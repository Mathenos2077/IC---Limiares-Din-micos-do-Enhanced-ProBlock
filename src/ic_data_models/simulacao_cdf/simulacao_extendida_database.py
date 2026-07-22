from utils import FactChecker
import utils
import numpy as np
import random
import duckdb
import db_insert as db

# Configurações da Simulação
N = 5  # Número de avaliadores por rodada
M = 10000 # Número de rodadas
DETALHAR_RODADAS = False # Se True, imprime os detalhes de cada avaliador em cada rodada
APENAS_DIVERGENTES = False # Se True, mostra apenas rodadas com divergência de conclusividade
SALVAR_NO_DB = True # Se True, salva os resultados no banco de dados DuckDB

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

if SALVAR_NO_DB:
    conn = duckdb.connect('simulacoes.duckdb')
    # Garante que os modelos existem no banco
    for modelo_nome in MODELOS_TOTAIS:
        # Verifica se o modelo já existe
        resultado = conn.execute("SELECT COUNT(*) FROM MODELO WHERE nome = ?", (modelo_nome,)).fetchone()
        if resultado and resultado[0] == 0:
            tipo = "fixo" if "fixo" in modelo_nome else "dinamico"
            db.inserir_modelo(conn, modelo_nome, tipo, f"Modelo {modelo_nome} inserido via simulação.")
            print(f"Modelo '{modelo_nome}' inserido no banco de dados.")
    conn.commit() # Comita a inserção dos modelos

print(f"Iniciando simulação com {M} rodadas e {N} avaliadores por rodada...")

# Pega o último 'numero' de avaliação para continuar a sequência
try:
    ultimo_numero_avaliacao = conn.execute("SELECT MAX(numero) FROM AVALIACAO").fetchone()[0]
    numero_avaliacao_atual = ultimo_numero_avaliacao + 1 if ultimo_numero_avaliacao is not None else 1
except (duckdb.CatalogException, IndexError):
    numero_avaliacao_atual = 1


for i in range(M):
    # Inicia uma transação para a rodada atual.
    if SALVAR_NO_DB:
        conn.begin()

    log_buffer = []
    
    def log(msg):
        log_buffer.append(msg)
        if not APENAS_DIVERGENTES and DETALHAR_RODADAS:
            print(msg)

    if not DETALHAR_RODADAS:
        print(f"Rodada {i+1}/{M}", end='\r', flush=True)
    else:
        log(f"\n--- Rodada {i+1}/{M} ---")

    factCheckers = []
    weightedVotes = []

    fact_checker_ids = []
    # Gerar avaliadores aleatórios
    for j in range(N):
        yrsScore = random.randint(1, 3)
        orgScore = random.randint(1, 5)
        freqScore = random.uniform(0, 2)
        accScore = random.uniform(0, 8)
        subjectScore = random.uniform(1, 5)
        newsVote = random.randint(-2, 2)
        confidenceScore = random.randint(1, 3)
        coScoreMedio = random.uniform(0, 1)

        # Normaliza o confidenceScore entre 0.9 e 1.1
        confidenceScore = 0.9 + ((confidenceScore - 1) / 2) * 0.2

        checker = FactChecker(
            yrsScore,
            orgScore,
            freqScore,
            accScore,
            subjectScore,
            newsVote,
            confidenceScore,
            coScoreMedio
        )
        factCheckers.append(checker)
        weightedVotes.append(checker.getWeightedVote())

        if SALVAR_NO_DB:
            totalVote = random.randint(50, 200)  # Gera um número total de votos para simular o histórico
            correctVote = round((accScore / 8) * totalVote) # Calcula os votos corretos para corresponder ao accScore
            # Insere o fact-checker e obtém o ID
            last_id = db.inserir_fact_checker(conn, checker.yrsScore, checker.orgScore, checker.freqScore, checker.coScoreMedio, checker.subjectScore, totalVote, correctVote)
            fact_checker_ids.append(last_id)

        log(f"  Avaliador {j+1}: Yrs={yrsScore}, Org={orgScore}, Freq={freqScore:.2f}, Acc={accScore:.2f}, Subj={subjectScore:.2f}, Vote={newsVote}, Conf={confidenceScore:.2f}, Co={coScoreMedio:.2f}, WeightedVote={weightedVotes[-1]:.2f}")

    # Calcular CDF, Parâmetros e Limiares
    if np.std(weightedVotes) == 0:
        log("  [!] Desvio padrão zero. Rodada ignorada.")
        # Como a avaliação é ignorada, fazemos rollback das inserções de fact-checkers desta rodada
        # A transação iniciada no começo do loop será revertida.
        if SALVAR_NO_DB:
            conn.rollback()
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
    limiar_score_base = 0.0

    for modelo in MODELOS_TOTAIS:
        limiarScore = round(utils.getLimiarScore(factCheckers, model=modelo), 4)
        
        if modelo == MODELO_BASE:
            limiar_score_base = limiarScore

        if SALVAR_NO_DB:
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
    
    if SALVAR_NO_DB:
        try:
            # Inserir a avaliação principal
            db.inserir_avaliacao(conn, numero_avaliacao_atual, cdf, limiar_score_base, IC, coScoreTotal, subjectScoreTotal)

            # Inserir relacionamentos FAZ
            for idx, checker_id in enumerate(fact_checker_ids):
                checker = factCheckers[idx]
                db.inserir_relacionamento_faz(conn, checker_id, numero_avaliacao_atual, checker.confidenceScore, checker.newsVote, checker.getWeightedVote())

            # Inserir relacionamentos INTERPRETA
            for modelo, conclusao in conclusoes_modelos.items():
                db.inserir_relacionamento_interpreta(conn, numero_avaliacao_atual, modelo, conclusao)
            
            conn.commit() # Confirma a transação da rodada
        except Exception as e:
            print(f"\nErro ao salvar no banco na rodada {i+1}: {e}")
            conn.rollback() # Reverte a transação da rodada em caso de erro

    if APENAS_DIVERGENTES and houve_divergencia:
        for linha in log_buffer:
            print(linha)
    numero_avaliacao_atual += 1

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

if SALVAR_NO_DB:
    with open("relatorio_final.txt", "w", encoding="utf-8") as f_relatorio:
        f_relatorio.write(texto_final + "\n")
    conn.close()
    print("\nSimulação concluída e dados salvos no banco. Conexão fechada.")
