import os
import sys

# Garante a resolução correta dos módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import duckdb
import db_insert as db
import utils
from utils import FactChecker

# Configurações do Modelo a ser adicionado
NOVO_MODELO_NOME = "v4_IC_057_143"  # Nome do modelo a ser adicionado (ex: "nao_podado_v3", "podado_v1", "fixo_05_05", etc.)
NOVO_MODELO_TIPO = "fixo" if "fixo" in NOVO_MODELO_NOME else "dinamico"
NOVO_MODELO_DESCRICAO = f"Modelo {NOVO_MODELO_NOME} inserido via simulacao_extendida_database_addModelo"

# Localização do banco de dados DuckDB
db_filename = 'simulacoes.duckdb'
repo_root_db = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..', db_filename))

if os.path.exists(db_filename):
    DB_PATH = db_filename
elif os.path.exists(repo_root_db):
    DB_PATH = repo_root_db
else:
    DB_PATH = db_filename

print(f"Conectando ao banco de dados: {DB_PATH}")
conn = duckdb.connect(DB_PATH)

try:
    # 1. Verifica se o modelo já existe no banco de dados para evitar duplicação
    resultado = conn.execute("SELECT COUNT(*) FROM MODELO WHERE nome = ?", (NOVO_MODELO_NOME,)).fetchone()
    if resultado and resultado[0] > 0:
        print(f"[!] O modelo '{NOVO_MODELO_NOME}' já existe no banco de dados! Operação abortada para evitar duplicatas.")
        conn.close()
        sys.exit(0)

    # 2. Insere o novo modelo na tabela MODELO
    db.inserir_modelo(conn, NOVO_MODELO_NOME, NOVO_MODELO_TIPO, NOVO_MODELO_DESCRICAO)
    print(f"-> Modelo '{NOVO_MODELO_NOME}' inserido com sucesso na tabela MODELO.")

    # 3. Busca todas as avaliações já existentes no banco de dados
    avaliacoes = conn.execute("SELECT numero, CDF FROM AVALIACAO ORDER BY numero").fetchall()
    total_avaliacoes = len(avaliacoes)
    print(f"-> Avaliando {total_avaliacoes} avaliações existentes no banco com o novo modelo '{NOVO_MODELO_NOME}'...")

    relatorio_conclusoes = {
        "Conteúdo Notoriamente Inverídico": 0,
        "Conteúdo Sugestivamente Inverídico": 0,
        "Inconclusivo": 0,
        "Conteúdo Sugestivamente Verídico": 0,
        "Conteúdo Notoriamente Verídico": 0
    }

    conn.begin() # Inicia transação para lote de inserções

    for idx, (avaliacao_numero, cdf) in enumerate(avaliacoes):
        # Imprime progresso a cada 1000 itens ou no final
        if (idx + 1) % 1000 == 0 or (idx + 1) == total_avaliacoes:
            print(f"Processando avaliação {idx + 1}/{total_avaliacoes}...", end='\r', flush=True)

        # Buscar avaliadores (fact-checkers) associados a esta avaliação
        query_avaliadores = """
        SELECT fc.yrsScore, fc.orgScore, fc.freqScore, fc.subjectScore, f.newsVote, f.confidenceScore, fc.coScoreMedio, fc.totalVote, fc.correctVote
        FROM FAZ f
        JOIN FACT_CHECKER fc ON f.fact_checker_id = fc.ID
        WHERE f.avaliacao_numero = ?
        ORDER BY fc.ID
        """
        avaliadores_rows = conn.execute(query_avaliadores, (avaliacao_numero,)).fetchall()

        factCheckers = []
        for row in avaliadores_rows:
            yrsScore, orgScore, freqScore, subjectScore, newsVote, confidenceScore, coScoreMedio, totalVote, correctVote = row
            accScore = (correctVote / totalVote) * 8 if totalVote > 0 else 0.0

            checker = FactChecker(
                yrsScore=yrsScore,
                orgScore=orgScore,
                freqScore=freqScore,
                accScore=accScore,
                subjectScore=subjectScore,
                newsVote=int(newsVote),
                confidenceScore=confidenceScore,
                coScoreMedio=coScoreMedio
            )
            factCheckers.append(checker)

        # Calcular limiarScore e Conclusão com o novo modelo
        limiarScore = round(utils.getLimiarScore(factCheckers, model=NOVO_MODELO_NOME), 4)

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

        if conclusao_modelo:
            relatorio_conclusoes[conclusao_modelo] += 1
            db.inserir_relacionamento_interpreta(conn, avaliacao_numero, NOVO_MODELO_NOME, conclusao_modelo, limiarScore)

    conn.commit()
    print(f"\n[+] Sucesso! {total_avaliacoes} avaliações foram processadas e salvas na tabela INTERPRETA para o modelo '{NOVO_MODELO_NOME}'.")

    print("\n--- RESUMO DE CONCLUSÕES DO NOVO MODELO ---")
    for k, v in relatorio_conclusoes.items():
        print(f"  {k}: {v}")

except Exception as e:
    conn.rollback()
    print(f"\n[!] Erro durante o processamento: {e}")

finally:
    conn.close()
