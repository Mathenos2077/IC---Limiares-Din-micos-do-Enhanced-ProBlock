import duckdb

# FUNÇÕES DE INSERÇÃO - ENTIDADES PRINCIPAIS

def inserir_fact_checker(conn, yrs_score, org_score, freq_score, co_score_medio, subject_score, total_vote, correct_vote):
    cursor = conn.execute(""" 
        INSERT INTO FACT_CHECKER (yrsScore, orgScore, freqScore, coScoreMedio, subjectScore, totalVote, correctVote)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        RETURNING ID
    """, (yrs_score, org_score, freq_score, co_score_medio, subject_score, total_vote, correct_vote))
    return cursor.fetchone()[0]


def inserir_avaliacao(conn, numero, cdf, limiar_score, ic, co_score_total, subject_score_total):
    conn.execute("""
        INSERT INTO AVALIACAO (numero, CDF, limiarScore, IC, coScoreTotal, subjectScoreTotal)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (numero, cdf, limiar_score, ic, co_score_total, subject_score_total))


def inserir_modelo(conn, nome, tipo, descricao=None):
    conn.execute("""
        INSERT INTO MODELO (nome, tipo, descricao)
        VALUES (?, ?, ?)
    """, (nome, tipo, descricao))


# FUNÇÕES DE INSERÇÃO - RELACIONAMENTOS (M:N)

def inserir_relacionamento_faz(conn, fact_checker_id, avaliacao_numero, confidence_score, news_vote, weighted_vote):
    conn.execute("""
        INSERT INTO FAZ (fact_checker_id, avaliacao_numero, confidenceScore, newsVote, weightedVote)
        VALUES (?, ?, ?, ?, ?)
    """, (fact_checker_id, avaliacao_numero, confidence_score, news_vote, weighted_vote))


def inserir_relacionamento_interpreta(conn, avaliacao_numero, modelo_nome, conclusao):
    conn.execute("""
        INSERT INTO INTERPRETA (avaliacao_numero, modelo_nome, conclusao)
        VALUES (?, ?, ?)
    """, (avaliacao_numero, modelo_nome, conclusao))