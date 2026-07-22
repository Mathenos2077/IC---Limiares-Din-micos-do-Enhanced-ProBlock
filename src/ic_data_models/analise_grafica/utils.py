import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import numpy as np
from scipy.stats import norm
import ic_data_models.entradas.coScore.coScoreTotal as coScore
import ic_data_models.entradas.subjectScore.getSubjectScoreTotal as subjectScore
import ic_data_models.entradas.IC.ic_calculo as icCalc
import ic_data_models.saida.limiarScore_podado    as limiarScorePodado
import ic_data_models.saida.limiarScore_nao_podado as limiarScoreNaoPodado
import ic_data_models.saida.limiarScore_podado_v2 as limiarScorePodadoV2
import ic_data_models.saida.limiarScore_nao_podado_v2 as limiarScoreNaoPodadoV2
import ic_data_models.saida.limiarScore_nao_podado_v3 as limiarScoreNaoPodadoV3

def getLimiarScore(IC, COSCORETOTAL):
    """
    Calcula o limiarScore final com base nos parâmetros IC e COSCORETOTAL, para o modelo v3

    :param IC: Valor de IC.
    :param COSCORETOTAL.
    :param model: String que determina qual modelo de cálculo será utilizado.
                  Valores aceitos:
                  - 'podado_v1': Modelo original com regras podadas (padrão).
                  - 'nao_podado_v1': Modelo original completo.
                  - 'podado_v2': Versão 2 do modelo com regras podadas.
                  - 'nao_podado_v2': Versão 2 do modelo completo.
                  - 'nao_podado_v3': Versão 3 do modelo completo.
    """

    return limiarScoreNaoPodadoV3.getLimiarScore_Nao_Podado_v3(COSCORETOTAL, IC, True)