import duckdb

# db para simulações com novos fact-checkers gerados aleatoriamente a cada rodada
#conn = duckdb.connect('simulacoes.duckdb')

# db para simulações com preservação e gerenciamento de fact-checkers (votos gerados aleatoriamente)

# Cria a sequência (contador) que começa em 1
conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_fact_checker_id START 1;")

# Criando a Tabela FACT_CHECKER
conn.execute("""
    CREATE TABLE IF NOT EXISTS FACT_CHECKER (
        ID INTEGER PRIMARY KEY DEFAULT nextval('seq_fact_checker_id'),
        yrsScore DOUBLE NOT NULL,
        orgScore DOUBLE,
        freqScore DOUBLE NOT NULL,
        coScoreMedio DOUBLE NOT NULL,
        subjectScore DOUBLE NOT NULL,
        totalVote DOUBLE NOT NULL,
        correctVote DOUBLE NOT NULL
    )
""")

# Tabela AVALIACAO
conn.execute("""
    CREATE TABLE IF NOT EXISTS AVALIACAO (
        numero INTEGER PRIMARY KEY,
        CDF DOUBLE NOT NULL,
        limiarScore DOUBLE NOT NULL,
        IC DOUBLE NOT NULL,
        coScoreTotal DOUBLE NOT NULL,
        subjectScoreTotal DOUBLE NOT NULL
    )
""")

# Tabela MODELO
conn.execute("""
    CREATE TABLE IF NOT EXISTS MODELO (
        nome VARCHAR PRIMARY KEY,
        tipo VARCHAR NOT NULL,
        descricao VARCHAR
    )
""")

# Tabela do Relacionamento FAZ (M:N entre FACT_CHECKER e AVALIACAO)
conn.execute("""
    CREATE TABLE IF NOT EXISTS FAZ (
        fact_checker_id INTEGER,
        avaliacao_numero INTEGER,
        confidenceScore DOUBLE NOT NULL,
        newsVote DOUBLE NOT NULL,
        weightedVote DOUBLE NOT NULL,
        PRIMARY KEY (fact_checker_id, avaliacao_numero),
        FOREIGN KEY (fact_checker_id) REFERENCES FACT_CHECKER(ID),
        FOREIGN KEY (avaliacao_numero) REFERENCES AVALIACAO(numero)
    )
""")

# Tabela do Relacionamento INTERPRETA (M:N entre AVALIACAO e MODELO)
conn.execute("""
    CREATE TABLE IF NOT EXISTS INTERPRETA (
        avaliacao_numero INTEGER,
        modelo_nome VARCHAR,
        conclusao VARCHAR NOT NULL,
        PRIMARY KEY (avaliacao_numero, modelo_nome),
        FOREIGN KEY (avaliacao_numero) REFERENCES AVALIACAO(numero),
        FOREIGN KEY (modelo_nome) REFERENCES MODELO(nome)
    )
""")

print("Tabelas criadas com sucesso no DuckDB!")

tabelas = conn.execute("SHOW TABLES").df()
print("\nTabelas existentes no banco:")
print(tabelas)

print(duckdb.__version__)

conn.close()