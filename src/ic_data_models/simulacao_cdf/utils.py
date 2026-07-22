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






class FactChecker:
    '''
    Essa classe representa uma unidade de fact-checker, no momento da avaliação de uma notícia hipotética.
    Todos os cálculos para a obtenção das variáveis de entrada são abstraidos, requisitando somente os valores delas.
    
    '''
    def __init__(self, yrsScore, orgScore, freqScore, accScore, subjectScore, newsVote, confidenceScore, coScoreMedio):
        '''
        Cria um novo fact-checker com atributos pré-definidos
        
        :param self: self
        :param yrsScore: Anos de experiência do avaliador.
            Assume valores inteiros entre 1 e 3.
        :param orgScore: Reputação da organização do avaliador.
            Assume valores inteiros entre 1 e 5.
        :param freqScore: Quantidade média de avaliações do fact-checker. 
            Assume valores inteiros entre 0 e 2.
        :param accScore: Acurácia do fact-checker (numero de acertos / numero de avaliacoes).
            Assume valores inteiros 0 e 8.
        :param subjectScore: Especialidade do fact-checker na notícia analisada.
            Assume valores inteiros 1 e 5.
        :param newsVote: Voto do fact-checker em relação a veracidade da notícia analisada. 
            -2 = Conteúdo Notoriamente Inverídico; -1 = Conteúdo Sugestivamente Inverídico; 0  = Inconclusiva
             1 = Conteúdo Sugestivamente Verídico; 2 = Conteúdo Notoriamente Verídico; 
        :param confidenceScore: Confiança do fact-checker na notícia analisada. 
            1 - Não confiante; 2 - Confiante; 3 - Altamente Confiante
        '''
        self.yrsScore = yrsScore
        self.orgScore = orgScore
        self.freqScore = freqScore
        self.accScore = accScore
        self.subjectScore = subjectScore
        self.newsVote = newsVote
        self.confidenceScore = confidenceScore
        self.coScoreMedio = coScoreMedio

    def getExpScoreEstatico(self):
        return self.yrsScore + self.orgScore

    def getExpScoreDinamico(self):
        '''
        Retorna a componente dinâmica do expScore

        :param self: self
        '''
        return self.freqScore + self.accScore + self.subjectScore
    
    def getExpScore(self):
        '''
        Retorna o expScore total
        
        :param self: self
        '''
        return self.getExpScoreEstatico() + self.getExpScoreDinamico()
    
    def getCummVote(self):
        '''
        Retorna o cummVote do fact-checker
        
        :param self: self
        '''
        return self.newsVote * self.confidenceScore
    
    def getWeightedVote(self):
        '''
        Retorna o voto ponderado do fact-checker
        
        :param self: self
        '''
        weightedVote = self.getExpScore() * self.getCummVote()
        return weightedVote
    

def getCDF(weightedVotes):

    '''
    Calcula e retorna o CDF de um conjunto de weightedVotes
    
    :param weightedVotes: array contendo os weightedVotes
    '''
    media = np.average(weightedVotes)
    desvioPadrao = np.std(weightedVotes)

    if desvioPadrao == 0:
        if weightedVotes[0] < 0:
            return 0
        elif weightedVotes[0] > 0:
            return 1
        else:
            return 0.5

    componentesBetaX = []

    for item in weightedVotes:
        betaI = (1 / (desvioPadrao * np.sqrt(np.pi * 2))) * np.exp(-(np.square(item - media) / (4 * np.square(desvioPadrao))))
        componentesBetaX.append(betaI * item)
    
    betaX = sum(componentesBetaX)
    cdf = norm.cdf(betaX)
    return cdf

def getLimiarScore(factCheckers, model="podado_v1"):
    """
    Calcula o limiarScore final com base nas avaliações fornecidas e no modelo escolhido.

    :param factCheckers: Lista contendo os objetos FactChecker.
    :param model: String que determina qual modelo de cálculo será utilizado.
                  Valores aceitos:
                  - 'podado_v1': Modelo original com regras podadas (padrão).
                  - 'nao_podado_v1': Modelo original completo.
                  - 'podado_v2': Versão 2 do modelo com regras podadas.
                  - 'nao_podado_v2': Versão 2 do modelo completo.
                  - 'nao_podado_v3': Versão 3 do modelo completo.
    """
    ICArray = [0, 0, 0, 0, 0] # Indica, respectivamente, a quantidade de votos -2, -1, 0, 1 e 2
    coScoreArray = []
    subjectScoreArray = []

    for x in factCheckers:
        match x.newsVote:
            case -2:
                ICArray[0] += 1
            case -1:
                ICArray[1] += 1
            case 0:
                ICArray[2] += 1
            case 1:
                ICArray[3] += 1
            case 2:
                ICArray[4] += 1 
        
        coScoreArray.append(x.coScoreMedio)
        subjectScoreArray.append(x.subjectScore)

    coScoreTotal = coScore.getCoScoreTotal(coScoreArray)
    subjectScoreTotal = subjectScore.getSubjectScoreTotal(subjectScoreArray)
    
    # Normaliza o subjectScore de 1-5 para 0-1 para o sistema fuzzy
    subjectScoreTotal = (subjectScoreTotal - 1) / 4
    
    IC = icCalc.getIC(ICArray, True)

    if model == "podado_v1":
        return limiarScorePodado.getLimiarScore_Podado(coScoreTotal, IC, subjectScoreTotal, True)
    elif model == "nao_podado_v1":
        return limiarScoreNaoPodado.getLimiarScore_Nao_Podado(coScoreTotal, IC, subjectScoreTotal, True)
    elif model == "podado_v2":
        return limiarScorePodadoV2.getLimiarScore_Podado_v2(coScoreTotal, IC, subjectScoreTotal, True)
    elif model == "nao_podado_v2":
        return limiarScoreNaoPodadoV2.getLimiarScore_Nao_Podado_v2(coScoreTotal, IC, subjectScoreTotal, True)
    elif model == "nao_podado_v3":
        return limiarScoreNaoPodadoV3.getLimiarScore_Nao_Podado_v3(coScoreTotal, IC, True)
    elif model == "fixo_01_09":
        return 0.2
    elif model == "fixo_02_08":
        return 0.4
    elif model == "fixo_03_07":
        return 0.6
    elif model == "fixo_04_06":
        return 0.8
    elif model == "fixo_05_05":
        return 1.0
    elif model == "fixo_0225_0775":
        return 0.45

    else:
        raise ValueError(f"Modelo '{model}' desconhecido.")

def getIC(newsVoteArray):
    ICArray = [0, 0, 0, 0, 0]

    for x in newsVoteArray:
        match x:
                case -2:
                    ICArray[0] += 1
                case -1:
                    ICArray[1] += 1
                case 0:
                    ICArray[2] += 1
                case 1:
                    ICArray[3] += 1
                case 2:
                    ICArray[4] += 1 
        
    return icCalc.getIC(ICArray, True)


def getCoScore(coScoreArray):
    return coScore.getCoScoreTotal(coScoreArray)

def getSubjectScore(subjectScoreArray):
    subjectScoreTotal = subjectScore.getSubjectScoreTotal(subjectScoreArray)
    
    # Normaliza o subjectScore de 1-5 para 0-1 para o sistema fuzzy
    subjectScoreTotal = (subjectScoreTotal - 1) / 4

    return subjectScoreTotal