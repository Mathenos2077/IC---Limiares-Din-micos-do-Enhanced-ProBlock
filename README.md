# Modelo de Limiares Dinâmicos do Enhanced ProBlock

Este repositório contém o modelo matemático e de inferência fuzzy para a geração de Limiares Dinâmicos de moderação em sistemas de detecção de notícias falsas (como o Enhanced ProBlock).

A arquitetura principal define que para cada notícia avaliada, o sistema ajusta as faixas de limiares que ditam se a probabilidade daquela notícia (CDF) é considerada verdadeira, falsa ou inconclusiva, baseado no consenso dos avaliadores.

## Estrutura de Arquivos e Componentes

- **IC (Índice de Convicção):** Um número que reflete o quanto os avaliadores estão certos em relação à veracidade da notícia.
- **coScore (Collaboration Score):** Avalia se o julgamento do avaliador está coerente com os demais.
  - O sistema possui dois meios de cálculo de coScore: um baseado em lógica *Fuzzy* original e um cálculo de *Mapeamento Direto* otimizado (`calculo_coScore_direto.py`), que normaliza variáveis entre 0 e 1, baseando-se em `assertLevel` de 1 a 5 e `confidence` de 0.9, 1.0 e 1.1.
- **limiarScore:** Saída do segundo sistema fuzzy, que utiliza o `IC` e o `CoScoreTotal` (média global) para determinar o tamanho numérico da zona "Inconclusiva".
- **Limiares Dinâmicos:** As quatro partições (`limDownEx`, `limDown`, `limUp`, `limUpEx`) na CDF de 0 a 1, baseadas no valor de `limiarScore`.

## Requisitos e Instalação

Para executar este sistema, instale as dependências:

```bash
pip install numpy scikit-fuzzy matplotlib
```

## Como executar o modelo (Interface Principal)

O arquivo `src/ic_data_models/main.py` atua como o ponto de entrada. Ele recebe uma lista de avaliadores em formato JSON.

Para rodar o exemplo de teste do pipeline principal, execute na raiz do projeto:

```bash
python src/ic_data_models/main.py
```

### Exemplo de Entrada e Saída (JSON)

A estrutura esperada pela função `pipeline_principal` é um Objeto JSON contendo a lista de `checadores` e campos extras opcionais como a probabilidade atual da notícia (`cdf`), e configurações paramétricas do IC (`IC_N` e `IC_Square`):

```json
{
    "cdf": 0.85,
    "IC_N": 5,
    "IC_Square": true,
    "checadores": [
        {"newsVote": 2, "subjectScore": 1, "coScoreMedio": 0.8},
        {"newsVote": -2, "subjectScore": 5, "coScoreMedio": 0.2}
    ]
}
```

Caso o campo `"cdf"` seja enviado no payload, o script fará as checagens com as partições dinâmicas geradas a partir do `limiarScore` e incluirá na resposta o campo `"conclusao"` avaliando onde esse CDF caiu, devolvendo um número numa escala de 5 níveis (`-2, -1, 0, 1, 2`). 

A saída retornada pela função `pipeline_principal` será uma string JSON formatada como o exemplo abaixo:

```json
{
    "limDownEx": 0.16995761857922081,
    "limDown": 0.33991523715844163,
    "limUp": 0.6600847628415584,
    "limUpEx": 0.8300423814207791,
    "conclusao": 2
}
```
> *Nota: a interface possui retrocompatibilidade. Se você enviar apenas a lista crua de checadores (sem estar num dicionário), o código continuará executando e calculando os limiares normalmente, apenas ignorará o cálculo da "conclusão".*

## Base de Regras Fuzzy (Transparência do Modelo)

O modelo possui duas inferências lógicas baseadas em pertinência Gaussiana.

### 1. Sistema Fuzzy de CoScore

Mapeia o Nível de Acerto (`assertLevel`, 5 níveis) e Nível de Confiança (`confidenceScore`, 3 níveis) para o Nível de Coerência (`coEscore`).

| Nível de Acerto / Confiança | Não Confiante (0.9) | Neutro (1.0) | Confiante (1.1) |
|-----------------------------|---------------------|--------------|-----------------|
| **Erro Gravíssimo (1)**     | Incoerente (0.25)   | Muito Incoerente (0.00)| Muito Incoerente (0.00)|
| **Erro Grave (2)**          | Incoerente (0.25)   | Incoerente (0.25)      | Muito Incoerente (0.00)|
| **Erro Razoável (3)**       | Neutro (0.50)       | Neutro (0.50)          | Incoerente (0.25)      |
| **Acerto Razoável (4)**     | Coerente (0.75)     | Coerente (0.75)        | Coerente (0.75)        |
| **Acerto Completo (5)**     | Coerente (0.75)     | Muito Coerente (1.00)  | Muito Coerente (1.00)  |

*Nota: Esta tabela original foi otimizada para ser executada O(1) na versão `calculo_coScore_direto.py`.*

### 2. Sistema Fuzzy de LimiarScore

Mapeia o Índice de Convicção (`IC`, 3 conjuntos) e a Coerência Total da Rede (`coEscore`, 5 conjuntos) em um intervalo numérico do Limiar de Inconclusividade (`limiarScore`, 9 conjuntos).

> Regras resumidas: Quanto maior a convicção, menor o tamanho do limiar inconclusivo.

## Referências e Notas de Implementação

> **TODO:**
> - [ ] Preencher informações extras sobre o paper acadêmico original (se houver link ou DOI).
> - [ ] Preencher detalhes de banco de dados se for conectar à API no futuro.
> - [ ] Listar como as métricas serão salvas para a construção dos gráficos.
