import duckdb

conn = duckdb.connect('simulacoes.duckdb')

conn.execute(""" DROP TABLE IF EXISTS FAZ """)
conn.execute(""" DROP TABLE IF EXISTS  INTERPRETA """)
conn.execute(""" DROP TABLE IF EXISTS  AVALIACAO """)
conn.execute(""" DROP TABLE IF EXISTS  FACT_CHECKER """)
conn.execute(""" DROP TABLE IF EXISTS  MODELO """)

conn.close()