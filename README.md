# Modelo de Limiares Dinâmicos - Enhanced ProBlock

Este repositório contém o modelo matemático e de inferência fuzzy para a geração de Limiares Dinâmicos de moderação em sistemas de detecção de Fake News (como o Enhanced ProBlock).

## Estratégia de Branches
- **`main`**: Destinada a quem quiser usar e conhecer o modelo. Contém a versão estável e pronta para uso.
- **`develop`**: Destinada a desenvolvedores e pesquisadores que queiram se aprofundar, modificar e expandir a arquitetura do modelo.

---

## Visão Geral do Modelo e CDF

O objetivo principal deste modelo é definir dinamicamente os limites de classificação para uma variável chamada **CDF**, que dita a probabilidade de uma notícia ser verdadeira (variando de 0 a 1). 

A depender dessa probabilidade, a notícia pode ser classificada em 5 níveis de gradação:
1. **Conteúdo notoriamente inverídico**
2. **Conteúdo sugestivamente inverídico**
3. **Inconclusivo**
4. **Conteúdo sugestivamente verídico**
5. **Conteúdo notoriamente verídico**

Os **Limiares Dinâmicos** servem justamente para decidir onde cada um desses 5 intervalos vai estar no espectro de 0 a 1, adaptando-se a cada caso com base no consenso da rede de avaliadores.

---

## Arquitetura e Variáveis Principais

O cálculo dos limiares funciona em cascata e é dividido em duas variáveis de entrada principais que alimentam o sistema fuzzy central:

### 1. IC (Índice de Convicção)
- **Arquivo:** `src/ic_data_models/entradas/IC/ic_v4.py`
- É uma medida que indica o quão convictos os avaliadores estão sobre a veracidade da notícia. 
- Utiliza como base os parâmetros `newsVote` e `subjectScore`.

### 2. CoScoreTotal
- Para entender o `CoScoreTotal`, é necessário compreender a hierarquia do cálculo:
  - **coScore:** Calculado individualmente para cada avaliação de um checador. Utiliza as variáveis `assertLevel` (escala inteira normalizada) e `confidenceScore` (0.9, 1.0, ou 1.1). Ele pode ser gerado via inferência fuzzy (`calculo_coScore.py`) ou por meio de um mapeamento direto otimizado (`calculo_coScore_direto.py`), que simplifica e normaliza os valores diretamente entre 0 e 1.
  - **coScoreMedio:** Diferente do coScore que é por avaliação, o `coScoreMedio` é individual para cada fact-checker, sendo a média de todos os coScores que ele obteve em suas avaliações.
  - **CoScoreTotal:** É a variável final de entrada para o sistema principal. Representa a média do array contendo os `coScoreMedio` de todos os avaliadores.

### 3. LimiarScore
- **Arquivo:** `src/ic_data_models/saida/limiarScore_v4.py`
- Este é o **Sistema Fuzzy Principal**. Ele recebe as duas variáveis acima (`IC` e `CoScoreTotal`) e retorna um valor único chamado `limiarScore`.
- O valor do `limiarScore` representa matematicamente o **tamanho do intervalo de inconclusão** na CDF.

### 4. Limiares Dinâmicos (As Partições)
- **Arquivo:** `src/ic_data_models/saida/getLimiarDinamico.py`
- Com o `limiarScore` em mãos, esta função calcula os limites exatos que separam os 5 intervalos na CDF (`limDownEx`, `limDown`, `limUp`, `limUpEx`), seguindo a regra matemática:
  - `limDown = 0.5 - (limiarScore / 2)`
  - `limUp = 0.5 + (limiarScore / 2)`
  - Já os limites extremos (`limDownEx` e `limUpEx`) dividem exatamente ao meio o espaço restante nos extremos da distribuição.

---

## Como Utilizar (`main.py`)

O arquivo `src/ic_data_models/main.py` atua como o ponto de entrada. O usuário final deve rodar esse script enviando um Payload JSON contendo as métricas de seus avaliadores.

> **Atenção:** Os cálculos prévios para obter o `coScoreMedio` individual de cada avaliador NÃO são tratados na `main`. O usuário deve tratar deles antes e enviar o valor já pronto no JSON.

### Requisitos
```bash
pip install numpy scikit-fuzzy matplotlib
```

### Exemplo de Payload JSON (Entrada)

A estrutura esperada é um Objeto JSON contendo a lista de `checadores` (com `newsVote`, `subjectScore` e `coScoreMedio`) e campos extras opcionais como a probabilidade atual da notícia (`cdf`), e configurações paramétricas do IC (`IC_N` e `IC_Square`):

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

### Retorno Esperado (Saída)

Caso o campo opcional `"cdf"` seja enviado no payload, o script fará as checagens com as partições geradas e incluirá o campo `"conclusao"`, retornando em qual categoria a notícia caiu (`-2` a `2`).

```json
{
    "limDownEx": 0.16995761857922081,
    "limDown": 0.33991523715844163,
    "limUp": 0.6600847628415584,
    "limUpEx": 0.8300423814207791,
    "conclusao": 2
}
```
*Nota: a interface possui retrocompatibilidade. Se você enviar apenas a lista crua de checadores (Array direto), o código continuará calculando os limiares normalmente, apenas ignorará o cálculo da "conclusão".*

---

## Base de Regras Fuzzy (Transparência do Modelo)

### 1. Sistema Fuzzy de CoScore (`calculo_coScore.py`)
Mapeia o Nível de Acerto (`assertLevel`, 5 níveis) e Nível de Confiança (`confidenceScore`, 3 níveis) para o Nível de Coerência (`coEscore`, de 0.00 a 1.00). *A versão otimizada `calculo_coScore_direto.py` abstrai essa inferência pesada num mapeamento direto.*

### 2. Sistema Fuzzy Principal (`limiarScore_v4.py`)
Mapeia o Índice de Convicção (`IC`, 3 conjuntos) e a Coerência Total da Rede (`coEscore`, 5 conjuntos) em um intervalo numérico de tamanho do Inconclusivo (`limiarScore`, 9 conjuntos). 
> **Resumo da inferência:** Quanto maior a convicção (`IC`) e maior a coerência dos checadores (`CoScoreTotal`), menor será a margem de dúvida (tamanho do intervalo Inconclusivo).

---

## Referências e Próximos Passos

> **TODO:**
> - [ ] Adicionar link/DOI para o paper acadêmico original e publicações base.
> - [ ] Preencher detalhes de arquitetura de integração com o Banco de Dados (quando a API for ao ar).
> - [ ] Documentar como as métricas e arrays de saída serão utilizados para a plotagem dos gráficos de pertinência e resultados.
