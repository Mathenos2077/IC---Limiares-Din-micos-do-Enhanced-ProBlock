import os

def calcular_taxa_divergencia(caminho_arquivo_divergencia, numero_avaliacoes_total):
    """
    Lê o arquivo de divergências salvo e calcula a taxa de divergência.
    Retorna a proporção (número de divergências / avaliações totais).
    """
    if not os.path.exists(caminho_arquivo_divergencia):
        print(f"Arquivo {caminho_arquivo_divergencia} não encontrado.")
        return 0.0
        
    numero_divergencias = 0
    with open(caminho_arquivo_divergencia, "r", encoding="utf-8") as f:
        for linha in f:
            # Identifica a tag única salva nos arquivos de divergência
            if "-> DIVERGÊNCIA IDENTIFICADA:" in linha:
                numero_divergencias += 1
                
    if numero_avaliacoes_total == 0:
        return 0.0
        
    taxa_divergencia = numero_divergencias / numero_avaliacoes_total
    return taxa_divergencia

def calcular_taxa_conclusao(caminho_arquivo_divergencia, numero_avaliacoes_total):
    """
    Calcula a taxa complementar da função de divergência (taxa de concordância).
    """
    taxa_div = calcular_taxa_divergencia(caminho_arquivo_divergencia, numero_avaliacoes_total)
    return 1.0 - taxa_div


if __name__ == "__main__":

    def calcular_exibir(name):
        taxa_conclusao = calcular_taxa_divergencia(name, 10000)
        print(f"{name}: {taxa_conclusao:.2f}")

    calcular_exibir("divergencias_nao_podado_v3_vs_fixo_01_09.txt")
    calcular_exibir("divergencias_nao_podado_v3_vs_fixo_02_08.txt")
    calcular_exibir("divergencias_nao_podado_v3_vs_fixo_0225_0775.txt")
    calcular_exibir("divergencias_nao_podado_v3_vs_fixo_03_07.txt")
    calcular_exibir("divergencias_nao_podado_v3_vs_fixo_04_06.txt")
    calcular_exibir("divergencias_nao_podado_v3_vs_podado_v1.txt")

    
