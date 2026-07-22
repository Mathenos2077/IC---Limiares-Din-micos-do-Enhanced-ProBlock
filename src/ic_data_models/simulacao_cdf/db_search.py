import duckdb
from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap


def _formatar_avaliacao(conn, avaliacao_numero):
    """
    Função auxiliar para buscar e formatar os detalhes de uma única avaliação.
    """
    # Buscar dados da avaliação principal
    avaliacao = conn.execute("SELECT CDF, IC, coScoreTotal FROM AVALIACAO WHERE numero = ?", (avaliacao_numero,)).fetchone()
    if not avaliacao:
        return f"Avaliação com número {avaliacao_numero} não encontrada."

    cdf, ic, co_score_total = avaliacao

    # Buscar avaliadores (fact-checkers) e seus dados
    avaliadores_query = """
    SELECT fc.yrsScore, fc.orgScore, fc.freqScore, fc.subjectScore, f.newsVote, f.confidenceScore, fc.coScoreMedio, f.weightedVote, fc.totalVote, fc.correctVote
    FROM FAZ f
    JOIN FACT_CHECKER fc ON f.fact_checker_id = fc.ID
    WHERE f.avaliacao_numero = ?
    ORDER BY fc.ID
    """
    avaliadores = conn.execute(avaliadores_query, (avaliacao_numero,)).fetchall()

    # Buscar conclusões dos modelos
    conclusoes = conn.execute("SELECT modelo_nome, conclusao FROM INTERPRETA WHERE avaliacao_numero = ? ORDER BY modelo_nome", (avaliacao_numero,)).fetchall()

    # Montar o texto de saída
    output = []
    output.append(f"\n--- Avaliação {avaliacao_numero} ---")

    for i, av in enumerate(avaliadores):
        yrs_score, org_score, freq_score, subject_score, news_vote, conf_score, co_medio, weighted_vote, total_vote, correct_vote = av
        
        # Calcula o accScore a partir dos dados do banco
        acc_score = (correct_vote / total_vote) * 8 if total_vote > 0 else 0

        output.append(f"  Avaliador {i+1}: Yrs={yrs_score}, Org={org_score}, Freq={freq_score:.2f}, Acc={acc_score:.2f}, Subj={subject_score:.2f}, Vote={int(news_vote)}, Conf={conf_score:.2f}, Co={co_medio:.2f}, WeightedVote={weighted_vote:.2f}")

    output.append(f"  -> CDF: {cdf}")
    output.append(f"  -> IC: {ic}")
    output.append(f"  -> coScoreTotal: {co_score_total}")

    for modelo, conclusao in conclusoes:
        output.append(f"  -> Conclusão {modelo}: {conclusao}")

    return "\n".join(output)

def buscar_por_conclusao_convergente(modelos, db_path='simulacoes.duckdb'):
    """
    Busca e exibe avaliações onde um conjunto de modelos teve a mesma conclusão.

    :param modelos: Lista de nomes de modelos a serem comparados.
    :param db_path: Caminho para o arquivo do banco de dados DuckDB.
    """
    if not modelos or len(modelos) < 2:
        print("Erro: Forneça uma lista com pelo menos dois modelos.")
        return

    conn = duckdb.connect(db_path, read_only=True)
    total_avaliacoes = conn.execute("SELECT COUNT(*) FROM AVALIACAO").fetchone()[0]
    
    placeholders = ', '.join(['?'] * len(modelos))
    query = f"""
    SELECT avaliacao_numero
    FROM INTERPRETA
    WHERE modelo_nome IN ({placeholders})
    GROUP BY avaliacao_numero
    HAVING COUNT(DISTINCT conclusao) = 1 AND COUNT(modelo_nome) = ?
    """
    
    params = modelos + [len(modelos)]
    numeros_filtrados = conn.execute(query, params).fetchall()
    
    print(f"--- BUSCA POR CONVERGÊNCIA NOS MODELOS: {', '.join(modelos)} ---")
    for (numero,) in numeros_filtrados:
        print(_formatar_avaliacao(conn, numero))

    print("\n" + "="*40)
    print("     RELATÓRIO ESTATÍSTICO DA BUSCA")
    print("="*40)
    print(f"Total de Avaliações no Banco: {total_avaliacoes}")
    print(f"Avaliações com Conclusão Convergente: {len(numeros_filtrados)}")
    print("="*40)
    
    conn.close()

def buscar_por_conclusao_divergente(modelos, db_path='simulacoes.duckdb'):
    """
    Busca e exibe avaliações onde um conjunto de modelos teve conclusões diferentes.

    :param modelos: Lista de nomes de modelos a serem comparados.
    :param db_path: Caminho para o arquivo do banco de dados DuckDB.
    """
    if not modelos or len(modelos) < 2:
        print("Erro: Forneça uma lista com pelo menos dois modelos.")
        return

    conn = duckdb.connect(db_path, read_only=True)
    total_avaliacoes = conn.execute("SELECT COUNT(*) FROM AVALIACAO").fetchone()[0]
    
    placeholders = ', '.join(['?'] * len(modelos))
    query = f"""
    SELECT avaliacao_numero
    FROM INTERPRETA
    WHERE modelo_nome IN ({placeholders})
    GROUP BY avaliacao_numero
    HAVING COUNT(DISTINCT conclusao) > 1 AND COUNT(modelo_nome) = ?
    """
    
    params = modelos + [len(modelos)]
    numeros_filtrados = conn.execute(query, params).fetchall()

    print(f"--- BUSCA POR DIVERGÊNCIA NOS MODELOS: {', '.join(modelos)} ---")
    for (numero,) in numeros_filtrados:
        print(_formatar_avaliacao(conn, numero))

    print("\n" + "="*40)
    print("     RELATÓRIO ESTATÍSTICO DA BUSCA")
    print("="*40)
    print(f"Total de Avaliações no Banco: {total_avaliacoes}")
    print(f"Avaliações com Conclusão Divergente: {len(numeros_filtrados)}")
    print("="*40)

    conn.close()

def buscar_por_divergencia_unanime_entre_grupos(grupo_modelos_1, grupo_modelos_2, db_path='simulacoes.duckdb'):
    """
    Busca avaliações onde a conclusão unânime do grupo 1 é diferente da conclusão unânime do grupo 2.

    :param grupo_modelos_1: Lista de nomes de modelos do primeiro grupo.
    :param grupo_modelos_2: Lista de nomes de modelos do segundo grupo.
    :param db_path: Caminho para o arquivo do banco de dados DuckDB.
    """
    if not grupo_modelos_1 or not grupo_modelos_2:
        print("Erro: Ambos os grupos de modelos devem ser fornecidos.")
        return

    conn = duckdb.connect(db_path, read_only=True)
    total_avaliacoes = conn.execute("SELECT COUNT(*) FROM AVALIACAO").fetchone()[0]

    # Query para encontrar avaliações onde o grupo 1 tem uma conclusão unânime
    q1_placeholders = ', '.join(['?'] * len(grupo_modelos_1))
    query1 = f"""
    SELECT avaliacao_numero, MIN(conclusao) as conclusao_g1
    FROM INTERPRETA
    WHERE modelo_nome IN ({q1_placeholders})
    GROUP BY avaliacao_numero
    HAVING COUNT(DISTINCT conclusao) = 1 AND COUNT(modelo_nome) = ?
    """
    params1 = grupo_modelos_1 + [len(grupo_modelos_1)]
    
    # Query para encontrar avaliações onde o grupo 2 tem uma conclusão unânime
    q2_placeholders = ', '.join(['?'] * len(grupo_modelos_2))
    query2 = f"""
    SELECT avaliacao_numero, MIN(conclusao) as conclusao_g2
    FROM INTERPRETA
    WHERE modelo_nome IN ({q2_placeholders})
    GROUP BY avaliacao_numero
    HAVING COUNT(DISTINCT conclusao) = 1 AND COUNT(modelo_nome) = ?
    """
    params2 = grupo_modelos_2 + [len(grupo_modelos_2)]

    # Junta os resultados e filtra por divergência
    final_query = """
    SELECT g1.avaliacao_numero FROM ({q1}) as g1 JOIN ({q2}) as g2 ON g1.avaliacao_numero = g2.avaliacao_numero
    WHERE g1.conclusao_g1 != g2.conclusao_g2
    """.format(q1=query1, q2=query2)

    numeros_filtrados = conn.execute(final_query, params1 + params2).fetchall()

    print(f"--- BUSCA POR DIVERGÊNCIA ENTRE GRUPOS ---")
    print(f"Grupo 1: {', '.join(grupo_modelos_1)}")
    print(f"Grupo 2: {', '.join(grupo_modelos_2)}")
    print("-" * 20)

    for (numero,) in numeros_filtrados:
        print(_formatar_avaliacao(conn, numero))

    print("\n" + "="*40)
    print("     RELATÓRIO ESTATÍSTICO DA BUSCA")
    print("="*40)
    print(f"Total de Avaliações no Banco: {total_avaliacoes}")
    print(f"Avaliações com Divergência entre os Grupos: {len(numeros_filtrados)}")
    print("="*40)

    conn.close()

def gerar_relatorio_modelos(db_path='simulacoes.duckdb'):
    """
    Gera e exibe um relatório estatístico para cada modelo no banco de dados,
    mostrando a contagem de cada tipo de conclusão e a taxa de conclusão.

    :param db_path: Caminho para o arquivo do banco de dados DuckDB.
    """
    conn = duckdb.connect(db_path, read_only=True)

    # Tipos de conclusão para garantir a ordem e a presença de todos no relatório
    tipos_conclusao = [
        "Conteúdo Notoriamente Inverídico",
        "Conteúdo Sugestivamente Inverídico",
        "Inconclusivo",
        "Conteúdo Sugestivamente Verídico",
        "Conteúdo Notoriamente Verídico"
    ]

    # Busca a contagem de cada conclusão para cada modelo
    query = """
    SELECT modelo_nome, conclusao, COUNT(*) as contagem
    FROM INTERPRETA
    GROUP BY modelo_nome, conclusao
    ORDER BY modelo_nome
    """
    resultados = conn.execute(query).fetchall()
    conn.close()

    # Organiza os dados em um dicionário
    relatorio_dados = {}
    for modelo, conclusao, contagem in resultados:
        if modelo not in relatorio_dados:
            relatorio_dados[modelo] = {tipo: 0 for tipo in tipos_conclusao}
        relatorio_dados[modelo][conclusao] = contagem

    # Imprime o relatório no formato solicitado
    for modelo, contagens in relatorio_dados.items():
        print(f"\n---------------   MODELO: {modelo.upper()}   -----------------------")
        total_avaliacoes = sum(contagens.values())
        inconclusivos = contagens.get("Inconclusivo", 0)

        for tipo in tipos_conclusao:
            print(f"{tipo}: {contagens.get(tipo, 0)}")

        taxa_conclusao = (total_avaliacoes - inconclusivos) / total_avaliacoes if total_avaliacoes > 0 else 0
        print(f"Taxa de Conclusão: {taxa_conclusao:.2f}")

    print("--------------------------------------------------------------")

def gerar_matriz_confusao(modelo1_nome, modelo2_nome, db_path='simulacoes.duckdb', visual=True):
    """
    Gera e exibe uma matriz de confusão comparando as conclusões de dois modelos.

    :param modelo1_nome: Nome do primeiro modelo (linhas da matriz).
    :param modelo2_nome: Nome do segundo modelo (colunas da matriz).
    :param db_path: Caminho para o arquivo do banco de dados DuckDB.
    :param visual: Se True, exibe um mapa de calor gráfico da matriz. Requer seaborn e matplotlib.
    """
    conn = duckdb.connect(db_path, read_only=True)

    # Query para buscar os pares de conclusões para cada avaliação
    query = """
    SELECT
        i1.conclusao AS conclusao1,
        i2.conclusao AS conclusao2
    FROM INTERPRETA i1
    JOIN INTERPRETA i2 ON i1.avaliacao_numero = i2.avaliacao_numero
    WHERE i1.modelo_nome = ? AND i2.modelo_nome = ?
    """
    
    pares_conclusoes = conn.execute(query, (modelo1_nome, modelo2_nome)).fetchall()
    conn.close()

    if not pares_conclusoes:
        print(f"Não foram encontradas avaliações em comum para os modelos '{modelo1_nome}' e '{modelo2_nome}'.")
        return

    # Ordem das conclusões para os eixos da matriz
    tipos_conclusao = [
        "Conteúdo Notoriamente Inverídico",
        "Conteúdo Sugestivamente Inverídico",
        "Inconclusivo",
        "Conteúdo Sugestivamente Verídico",
        "Conteúdo Notoriamente Verídico"
    ]

    # Cria a matriz de confusão usando pandas
    matriz = pd.crosstab(
        pd.Series([p[0] for p in pares_conclusoes], name=modelo1_nome),
        pd.Series([p[1] for p in pares_conclusoes], name=modelo2_nome),
        rownames=[modelo1_nome],
        colnames=[modelo2_nome]
    )

    # Reordena o índice e as colunas para seguir a ordem padrão
    matriz = matriz.reindex(index=tipos_conclusao, columns=tipos_conclusao, fill_value=0)

    if not visual:
        print(f"\n--- MATRIZ DE CONFUSÃO: {modelo1_nome.upper()} vs {modelo2_nome.upper()} ---")
        print(f"Total de Avaliações Comparadas: {len(pares_conclusoes)}\n")
        print(matriz)
        print("\n" + "-"*80)

    if visual:
        plt.figure(figsize=(10, 8))
        heatmap = sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues", cbar=True, linewidths=.5)
        
        # Quebra de linha para os rótulos dos eixos para melhor visualização
        labels = [textwrap.fill(label, 15) for label in tipos_conclusao]
        heatmap.set_xticklabels(labels, rotation=45, ha='right')
        heatmap.set_yticklabels(labels, rotation=0)
        
        plt.title(f'Matriz de Confusão: {modelo1_nome.upper()} vs {modelo2_nome.upper()}\nTotal: {len(pares_conclusoes)} avaliações', fontsize=16)
        plt.ylabel(modelo1_nome, fontsize=12)
        plt.xlabel(modelo2_nome, fontsize=12)
        plt.tight_layout()
        plt.show()

def gerar_histograma_comparativo(modelos, db_path='simulacoes.duckdb', agrupar_conclusoes=False):
    """
    Gera um histograma (gráfico de barras) comparando a distribuição de conclusões
    para uma lista de modelos.

    :param modelos: Lista de nomes de modelos a serem comparados.
    :param db_path: Caminho para o arquivo do banco de dados DuckDB.
    :param agrupar_conclusoes: Se True, agrupa as conclusões em 'Inverídico', 'Inconclusivo' e 'Verídico'.
    """
    if not modelos:
        print("Erro: Forneça uma lista com pelo menos um modelo.")
        return

    conn = duckdb.connect(db_path, read_only=True)

    # Query para buscar a contagem de cada conclusão para os modelos especificados
    placeholders = ', '.join(['?'] * len(modelos))
    query = f"""
    SELECT modelo_nome, conclusao, COUNT(*) as contagem
    FROM INTERPRETA
    WHERE modelo_nome IN ({placeholders})
    GROUP BY modelo_nome, conclusao
    """
    
    df = conn.execute(query, modelos).fetchdf()
    conn.close()

    if df.empty:
        print(f"Não foram encontradas avaliações para os modelos especificados: {', '.join(modelos)}.")
        return

    if agrupar_conclusoes:
        # Mapeia as conclusões detalhadas para as agrupadas
        mapeamento = {
            "Conteúdo Notoriamente Inverídico": "Inverídico",
            "Conteúdo Sugestivamente Inverídico": "Inverídico",
            "Inconclusivo": "Inconclusivo",
            "Conteúdo Sugestivamente Verídico": "Verídico",
            "Conteúdo Notoriamente Verídico": "Verídico"
        }
        df['conclusao'] = df['conclusao'].map(mapeamento)
        
        # Agrupa novamente após o mapeamento para somar as contagens
        df = df.groupby(['modelo_nome', 'conclusao'])['contagem'].sum().reset_index()

        # Define a ordem e as cores para a visualização agrupada
        tipos_conclusao = ["Inverídico", "Inconclusivo", "Verídico"]
        cores = {
            "Inverídico": '#d62728',  # Vermelho
            "Inconclusivo": '#ffcc00',  # Amarelo
            "Verídico": '#2ca02c'    # Verde
        }
    else:
        # Ordem e cores padrão (sem agrupamento)
        tipos_conclusao = ["Conteúdo Notoriamente Inverídico", "Conteúdo Sugestivamente Inverídico", "Inconclusivo", "Conteúdo Sugestivamente Verídico", "Conteúdo Notoriamente Verídico"]
        cores = {
            "Conteúdo Notoriamente Inverídico": '#d62728', "Conteúdo Sugestivamente Inverídico": '#ff9999',
            "Inconclusivo": '#ffcc00',
            "Conteúdo Sugestivamente Verídico": '#98df8a', "Conteúdo Notoriamente Verídico": '#2ca02c'
        }

    # Pivota o DataFrame para ter modelos como índice e conclusões como colunas
    df_pivot = df.pivot(index='modelo_nome', columns='conclusao', values='contagem').fillna(0)

    # Garante que os modelos (índice) e as conclusões (colunas) estejam na ordem correta
    df_pivot = df_pivot.reindex(index=modelos, fill_value=0)
    df_pivot = df_pivot.reindex(columns=tipos_conclusao, fill_value=0)

    # Cria a lista de cores na ordem correta das colunas do DataFrame
    cores_ordenadas = [cores[col] for col in df_pivot.columns]

    # Gera o gráfico de barras
    ax = df_pivot.plot(kind='bar', figsize=(10, 8), width=0.5, color=cores_ordenadas)
    
    plt.title('Comparativo de Conclusões por Modelo', fontsize=16)
    plt.ylabel('Quantidade de Avaliações', fontsize=12)
    plt.xlabel('Modelo', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Conclusão')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    """
    Este bloco é executado quando o script é chamado diretamente.
    Descomente as funções que deseja executar para testar as buscas no banco de dados.
    """
    # Exemplo de uso da nova função de histograma:
    modelos_para_comparar = ["fixo_01_09", "fixo_02_08", "fixo_0225_0775", "fixo_03_07", "fixo_04_06", "podado_v1", "nao_podado_v3"]
    # Para ver o gráfico com as conclusões agrupadas, mude para True
    gerar_histograma_comparativo(modelos_para_comparar, agrupar_conclusoes=True)
    
 