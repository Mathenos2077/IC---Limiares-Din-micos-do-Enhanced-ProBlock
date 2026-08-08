import numpy as np
import matplotlib.pyplot as plt

### Calcula o IC - Índice de Convicção (Seu código original)
def getIC_v4(newsVoteArray, subjectScoreArray, min=0.5, max=1.5, square=True):
    pontuacaoAval = [0, 0, 0, 0, 0]
    
    def calcular_valor(subjectScore, min, max):
        return min + ((subjectScore - 1) / 4) * (max - min)

    for i in range(len(newsVoteArray)):
        if newsVoteArray[i] == -2:
            pontuacaoAval[0] += calcular_valor(subjectScoreArray[i], min, max)
        elif newsVoteArray[i] == -1:
            pontuacaoAval[1] += calcular_valor(subjectScoreArray[i], min, max)
        elif newsVoteArray[i] == 0:
            pontuacaoAval[2] += calcular_valor(subjectScoreArray[i], min, max)
        elif newsVoteArray[i] == 1:
            pontuacaoAval[3] += calcular_valor(subjectScoreArray[i], min, max)
        elif newsVoteArray[i] == 2:
            pontuacaoAval[4] += calcular_valor(subjectScoreArray[i], min, max)

    valores = [
        -2, 
        -1, 
        0, 
        1, 
        2, 
    ]

    votosFinal = []

    if square == True:
        for i in range(5):
            votosFinal.append(np.square(pontuacaoAval[i]) * valores[i])

        n = 0
        for i in range(len(pontuacaoAval)):
            n += np.square(pontuacaoAval[i])
        
        # Evita divisão por zero caso todos os pesos se anulem
        if n == 0:
            return 0
        ic = sum(votosFinal) / n
    else:
        for i in range(5):
            votosFinal.append(pontuacaoAval[i] * valores[i])
        
        soma_pontuacao = sum(pontuacaoAval)
        if soma_pontuacao == 0:
            return 0
        ic = sum(votosFinal) / soma_pontuacao
     
    return ic/2

### Nova Função de Teste e Gráfico
def plot_ic_sensibilidade(newsVoteArray, subjectScoreArray, range=[0, 1], passos=20, square=True):
    """
    Testa o algoritmo variando os limites 'min' e 'max' de forma simétrica.
    Parte do modelo antigo (1 e 1) até limites extremos (0 e 2).
    """
    # Cria os deltas variando de 0.0 até 1.0
    deltas = np.linspace(range[0], range[1], passos + 1)
    
    eixo_x_labels = [] 
    valores_ic = []
    
    for delta in deltas:
        min_val = 1.0 - delta
        max_val = 1.0 + delta
        
        # Calcula o IC para o cenário atual
        ic = getIC_v4(newsVoteArray, subjectScoreArray, min=min_val, max=max_val, square=square)
        valores_ic.append(ic)
        
        # Salva o par [min, max] como texto para o eixo X do gráfico
        eixo_x_labels.append(f"{min_val:.2f} | {max_val:.2f}")

    # Plotagem
    plt.figure(figsize=(9, 6))
    plt.plot(deltas, valores_ic, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=6)
    plt.plot(deltas[0], valores_ic[0], marker='o', color='red', markersize=10, label='Modelo Antigo (1.0 | 1.0)')
    plt.xticks(deltas, eixo_x_labels, rotation=45, ha='right')
    plt.title('Sensibilidade do IC em Relação aos Limites [Min | Max]', fontsize=14, pad=15)
    plt.xlabel('Variação Simétrica dos Limites [Mínimo | Máximo]', fontsize=12)
    plt.ylabel('Resultado do IC Calculado', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Cenário de teste
    cenario_votos = np.array([2, 2, 2, -2, -2, -2])
    cenario_scores = np.array([1, 1, 1, 2, 2, 2])
    
    print("Gerando gráfico de sensibilidade...")
    plot_ic_sensibilidade(cenario_votos, cenario_scores, range=[0, 0.5], passos=10, square=True)