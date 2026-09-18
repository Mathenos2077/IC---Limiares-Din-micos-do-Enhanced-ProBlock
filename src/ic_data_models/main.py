import sys
import os
import json

# Ajusta o sys.path para garantir as importações corretas a partir de src/ic_data_models
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from entradas.IC.ic_v4 import getIC_v4
from entradas.coScore.coScoreTotal import getCoScoreTotal
from saida.limiarScore_v4 import getLimiarScore_v4
from saida.getLimiarDinamico import getLimiaresDinamicos

def pipeline_principal(avaliadores_json_str):
    """
    Executa o pipeline principal para calcular os limiares dinâmicos a partir
    das entradas dos avaliadores.
    
    :param avaliadores_json_str: String JSON com a lista de avaliadores.
    """
    try:
        payload = json.loads(avaliadores_json_str)
    except json.JSONDecodeError as e:
        print(f"Erro ao ler JSON: {e}")
        return None

    # Verifica se enviou o novo formato de payload em dicionário
    if isinstance(payload, dict):
        avaliadores = payload.get("checadores", [])
        cdf_valor = payload.get("cdf", None)
        ic_n_custom = payload.get("IC_N", None)
        ic_square_custom = payload.get("IC_Square", None)
    elif isinstance(payload, list):
        # Compatibilidade com o formato antigo de lista direta
        avaliadores = payload
        cdf_valor = None
        ic_n_custom = None
        ic_square_custom = None
    else:
        print("Formato de entrada inválido.")
        return None

    if not avaliadores:
        print("Nenhum dado de checador fornecido.")
        return None

    newsVoteArray = []
    subjectScoreArray = []
    coScoreMedioArray = []
    
    for avaliador in avaliadores:
        newsVoteArray.append(avaliador.get("newsVote", 0))
        subjectScoreArray.append(avaliador.get("subjectScore", 1))
        coScoreMedioArray.append(avaliador.get("coScoreMedio", 0.5))
        
    # Calcula IC
    N = len(avaliadores) if ic_n_custom is None else float(ic_n_custom)
    ic_square = True if ic_square_custom is None else bool(ic_square_custom)
    ic = getIC_v4(newsVoteArray, subjectScoreArray, N, square=ic_square)
    
    # Calcula CoScoreTotal
    coScoreTotal = getCoScoreTotal(coScoreMedioArray)
    
    # Calcula LimiarScore
    limiarScore = getLimiarScore_v4(coScoreTotal, ic, isNormalizado=True)
    
    # Obtem Limiares Dinâmicos
    limDownEx, limDown, limUp, limUpEx = getLimiaresDinamicos(limiarScore)
    

    resultado = {
        "limDownEx": limDownEx,
        "limDown": limDown,
        "limUp": limUp,
        "limUpEx": limUpEx
    }
    
    # Se um CDF for fornecido (opcional), calcula a conclusão
    if cdf_valor is not None:
        try:
            cdf = float(cdf_valor)
            if cdf < limDownEx:
                conclusao = -2 # Notoriamente Inverídico
            elif cdf < limDown:
                conclusao = -1 # Sugestivamente Inverídico
            elif cdf <= limUp:
                conclusao = 0  # Inconclusivo
            elif cdf <= limUpEx:
                conclusao = 1  # Sugestivamente Verídico
            else:
                conclusao = 2  # Notoriamente Verídico
                
            resultado["conclusao"] = conclusao
        except ValueError:
            pass # Ignora se o CDF não for um número válido
            
    return json.dumps(resultado, indent=4)

if __name__ == "__main__":
    # Exemplo de uso para teste local
    exemplo_json = '''
    {
        "cdf": 0.85,
        "IC_N": 5,
        "IC_Square": true,
        "checadores": [
            {"newsVote": 2, "subjectScore": 1, "coScoreMedio": 0.8},
            {"newsVote": 2, "subjectScore": 1, "coScoreMedio": 0.9},
            {"newsVote": 2, "subjectScore": 1, "coScoreMedio": 0.85},
            {"newsVote": 2, "subjectScore": 1, "coScoreMedio": 0.7},
            {"newsVote": -2, "subjectScore": 5, "coScoreMedio": 0.2}
        ]
    }
    '''
    resultado = pipeline_principal(exemplo_json)
    print(resultado)
