import os
import sys

# Garante a resolução correta dos módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import random
import numpy as np
import duckdb
import db_insert as db
import utils
from utils import FactChecker

# ==============================================================================
# CONFIGURAÇÃO DA ADIÇÃO DE AVALIAÇÃO MANUAL
# ==============================================================================
# Se MODO_INTERATIVO = True, o script vai solicitar os dados no terminal (prompt).
# Se MODO_INTERATIVO = False, o script utilizará a lista AVALIADORES_MANUAIS abaixo.
MODO_INTERATIVO = False

# Lista de avaliadores manuais (utilizada quando MODO_INTERATIVO = False):
# Você pode editar os valores abaixo ou adicionar/remover avaliadores da lista.
#
# Atributos de cada avaliador:
#   - yrsScore: Anos de experiência (1 a 3)
#   - orgScore: Reputação da organização (1 a 5)
#   - freqScore: Frequência de checagens (0.0 a 2.0)
#   - accScore: Acurácia histórica (0.0 a 8.0)
#   - subjectScore: Relevância no assunto (1.0 a 5.0)
#   - newsVote: Voto na notícia (-2 = Notoriamente Inverídico, -1 = Sugest. Inverídico, 
#                               0 = Inconclusivo, 1 = Sugest. Verídico, 2 = Notoriamente Verídico)
#   - confidenceScore: Nível de confiança (1 = Pouco, 2 = Confiante, 3 = Altamente Confiante 
#                       ou valor entre 0.9 e 1.1)
#   - coScoreMedio: Concordância média com a comunidade (0.0 a 1.0)
#   - totalVote (opcional): Total de checagens históricas (padrão: 100)
#   - correctVote (opcional): Total de acertos históricos (se omisso, calculado por accScore)
#
AVALIADORES_MANUAIS = [
   {
        "yrsScore": 3,
        "orgScore": 5,
        "freqScore": 2.0,
        "accScore": 8.0,
        "subjectScore": 1.0,
        "newsVote": 2,
        "confidenceScore": 1.1,
        "coScoreMedio": 1.0
    },
       {
        "yrsScore": 3,
        "orgScore": 5,
        "freqScore": 2.0,
        "accScore": 8.0,
        "subjectScore": 1.0,
        "newsVote": 2,
        "confidenceScore": 1.1,
        "coScoreMedio": 1.0
    },
       {
        "yrsScore": 3,
        "orgScore": 5,
        "freqScore": 2.0,
        "accScore": 8.0,
        "subjectScore": 1.0,
        "newsVote": 2,
        "confidenceScore": 1.1,
        "coScoreMedio": 1.0
    },
   {
        "yrsScore": 3,
        "orgScore": 5,
        "freqScore": 2.0,
        "accScore": 8.0,
        "subjectScore": 2.0,
        "newsVote": -2,
        "confidenceScore": 1.1,
        "coScoreMedio": 1.0
    }, 
    {
        "yrsScore": 3,
        "orgScore": 5,
        "freqScore": 2.0,
        "accScore": 8.0,
        "subjectScore": 2.0,
        "newsVote": -2,
        "confidenceScore": 1.1,
        "coScoreMedio": 1.0
    },
    {
        "yrsScore": 3,
        "orgScore": 5,
        "freqScore": 2.0,
        "accScore": 8.0,
        "subjectScore": 2.0,
        "newsVote": -2,
        "confidenceScore": 1.1,
        "coScoreMedio": 1.0
    }
]

# Localização do banco de dados DuckDB
db_filename = 'simulacoes.duckdb'
repo_root_db = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..', db_filename))

if os.path.exists(db_filename):
    DB_PATH = db_filename
elif os.path.exists(repo_root_db):
    DB_PATH = repo_root_db
else:
    DB_PATH = db_filename


def solicitar_input(prompt, tipo=float, valor_padrao=None, min_val=None, max_val=None):
    """Auxiliar para leitura interativa de dados no terminal."""
    while True:
        try:
            texto_padrao = f" [{valor_padrao}]" if valor_padrao is not None else ""
            entrada = input(f"{prompt}{texto_padrao}: ").strip()
            if not entrada and valor_padrao is not None:
                return valor_padrao
            val = tipo(entrada)
            if min_val is not None and val < min_val:
                print(f"  [!] Valor deve ser >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"  [!] Valor deve ser <= {max_val}")
                continue
            return val
        except ValueError:
            print(f"  [!] Entrada inválida. Digite um valor do tipo {tipo.__name__}.")


def obter_dados_avaliadores():
    """Retorna a lista de dicionários dos avaliadores (seja interativo ou manual)."""
    if MODO_INTERATIVO:
        print("\n--- MODO INTERATIVO: Inserção Manual de Avaliação ---")
        num_avaliadores = solicitar_input("Número de avaliadores para esta avaliação", tipo=int, valor_padrao=5, min_val=1)
        avaliadores = []
        for i in range(num_avaliadores):
            print(f"\n-> Dados do Avaliador #{i+1}:")
            yrs = solicitar_input("  Anos de experiência (yrsScore, 1 a 3)", tipo=int, valor_padrao=2, min_val=1, max_val=3)
            org = solicitar_input("  Reputação da organização (orgScore, 1 a 5)", tipo=int, valor_padrao=3, min_val=1, max_val=5)
            freq = solicitar_input("  Frequência de checagens (freqScore, 0.0 a 2.0)", tipo=float, valor_padrao=1.0, min_val=0.0, max_val=2.0)
            acc = solicitar_input("  Acurácia (accScore, 0.0 a 8.0)", tipo=float, valor_padrao=6.0, min_val=0.0, max_val=8.0)
            subj = solicitar_input("  Relevância no assunto (subjectScore, 1.0 a 5.0)", tipo=float, valor_padrao=3.0, min_val=1.0, max_val=5.0)
            vote = solicitar_input("  Voto na notícia (newsVote: -2, -1, 0, 1, 2)", tipo=int, valor_padrao=0, min_val=-2, max_val=2)
            conf = solicitar_input("  Confiança (confidenceScore: 1=Pouco, 2=Médio, 3=Alto ou 0.9 a 1.1)", tipo=float, valor_padrao=2.0)
            co = solicitar_input("  Concordância média (coScoreMedio, 0.0 a 1.0)", tipo=float, valor_padrao=0.5, min_val=0.0, max_val=1.0)
            
            avaliadores.append({
                "yrsScore": yrs,
                "orgScore": org,
                "freqScore": freq,
                "accScore": acc,
                "subjectScore": subj,
                "newsVote": vote,
                "confidenceScore": conf,
                "coScoreMedio": co
            })
        return avaliadores
    else:
        return AVALIADORES_MANUAIS


print(f"Conectando ao banco de dados: {DB_PATH}")
conn = duckdb.connect(DB_PATH)

try:
    # 1. Busca todos os modelos cadastrados no banco de dados
    modelos_rows = conn.execute("SELECT nome FROM MODELO ORDER BY nome").fetchall()
    modelos_existentes = [row[0] for row in modelos_rows]

    if not modelos_existentes:
        print("[!] Nenhum modelo encontrado na tabela MODELO! Por favor, insira ao menos um modelo no banco antes de adicionar avaliações.")
        conn.close()
        sys.exit(0)

    print(f"-> Modelos existentes registrados no banco ({len(modelos_existentes)}): {modelos_existentes}")

    # 2. Determina o número inicial da próxima avaliação
    try:
        ultimo_numero = conn.execute("SELECT MAX(numero) FROM AVALIACAO").fetchone()[0]
        numero_avaliacao_atual = ultimo_numero + 1 if ultimo_numero is not None else 1
    except (duckdb.CatalogException, IndexError):
        numero_avaliacao_atual = 1

    dados_avaliadores = obter_dados_avaliadores()
    
    if not dados_avaliadores:
        print("[!] Nenhum avaliador fornecido. Operação cancelada.")
        conn.close()
        sys.exit(0)

    MODELO_BASE = "nao_podado_v3" if "nao_podado_v3" in modelos_existentes else modelos_existentes[0]

    conn.begin()

    factCheckers = []
    weightedVotes = []
    fact_checker_ids = []

    log_lines = []
    log_lines.append(f"\n==================================================")
    log_lines.append(f" INSERINDO AVALIAÇÃO MANUAL (Número #{numero_avaliacao_atual})")
    log_lines.append(f"==================================================")

    for j, dad in enumerate(dados_avaliadores):
        yrsScore = int(dad["yrsScore"])
        orgScore = int(dad["orgScore"])
        freqScore = float(dad["freqScore"])
        accScore = float(dad["accScore"])
        subjectScore = float(dad["subjectScore"])
        newsVote = int(dad["newsVote"])
        confidenceScore = float(dad["confidenceScore"])
        coScoreMedio = float(dad["coScoreMedio"])

        # Normaliza o confidenceScore se tiver sido informado como 1, 2 ou 3
        if confidenceScore in [1, 2, 3]:
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

        totalVote = int(dad.get("totalVote", 100))
        if "correctVote" in dad and dad["correctVote"] is not None:
            correctVote = int(dad["correctVote"])
        else:
            correctVote = round((accScore / 8.0) * totalVote)

        fc_id = db.inserir_fact_checker(
            conn,
            checker.yrsScore,
            checker.orgScore,
            checker.freqScore,
            checker.coScoreMedio,
            checker.subjectScore,
            totalVote,
            correctVote
        )
        fact_checker_ids.append(fc_id)

        log_lines.append(
            f"  Avaliador {j+1} (ID {fc_id}): Yrs={yrsScore}, Org={orgScore}, Freq={freqScore:.2f}, "
            f"Acc={accScore:.2f}, Subj={subjectScore:.2f}, Vote={newsVote}, Conf={confidenceScore:.2f}, "
            f"Co={coScoreMedio:.2f}, WeightedVote={weightedVotes[-1]:.2f}"
        )

    if np.std(weightedVotes) == 0:
        print("[!] Alerta: O desvio padrão dos votos ponderados é zero nesta avaliação.")

    cdf = round(utils.getCDF(weightedVotes), 4)

    newsVoteArray = [checker.newsVote for checker in factCheckers]
    coScoreArray = [checker.coScoreMedio for checker in factCheckers]
    subjectScoreArray = [checker.subjectScore for checker in factCheckers]

    IC = round(utils.getIC(newsVoteArray), 4)
    coScoreTotal = round(utils.getCoScore(coScoreArray), 4)
    subjectScoreTotal = round(utils.getSubjectScore(subjectScoreArray), 4)

    log_lines.append(f"\n--- MÉTRICAS DA AVALIAÇÃO ---")
    log_lines.append(f"  -> CDF: {cdf}")
    log_lines.append(f"  -> IC: {IC}")
    log_lines.append(f"  -> coScoreTotal: {coScoreTotal}")
    log_lines.append(f"  -> subjectScoreTotal: {subjectScoreTotal}")

    limiar_score_base = round(utils.getLimiarScore(factCheckers, model=MODELO_BASE), 4)

    # Inserir avaliação na tabela AVALIACAO
    db.inserir_avaliacao(conn, numero_avaliacao_atual, cdf, limiar_score_base, IC, coScoreTotal, subjectScoreTotal)

    # Inserir relacionamentos FAZ
    for idx, fc_id in enumerate(fact_checker_ids):
        checker = factCheckers[idx]
        db.inserir_relacionamento_faz(conn, fc_id, numero_avaliacao_atual, checker.confidenceScore, checker.newsVote, checker.getWeightedVote())

    # Avaliar e inserir na tabela INTERPRETA para TODOS os modelos existentes
    log_lines.append(f"\n--- CONCLUSÕES DOS MODELOS ---")
    for modelo_nome in modelos_existentes:
        limiarScore = round(utils.getLimiarScore(factCheckers, model=modelo_nome), 4)

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

        db.inserir_relacionamento_interpreta(conn, numero_avaliacao_atual, modelo_nome, conclusao_modelo)
        log_lines.append(f"  -> Conclusão ({modelo_nome}): {conclusao_modelo}")

    conn.commit()

    print("\n".join(log_lines))
    print(f"\n[+] Sucesso! Avaliação #{numero_avaliacao_atual} inserida manualmente e avaliada por {len(modelos_existentes)} modelo(s).")

except Exception as e:
    conn.rollback()
    print(f"\n[!] Erro durante a adição manual da avaliação: {e}")

finally:
    conn.close()
