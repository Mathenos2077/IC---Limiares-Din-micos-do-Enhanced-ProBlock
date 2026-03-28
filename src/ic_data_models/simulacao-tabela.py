import json
import pandas as pd
import saida.calculo_limiarScore as limiarScoreFunc

ic =            []
coScore =       []
subjectScore =  []

limiarScore =   []
limiarScoreP =  []

for i in range(10):
    j = (i+1)/10
    ic.append(j)
    coScore.append(j)
    subjectScore.append(j)

for i in range(len(ic)):
    ls = limiarScoreFunc.getLimiarScore_NaoPodado(ic[i], coScore[i], subjectScore[i])
    limiarScore.append(ls)

    lsp = limiarScoreFunc.getLimiarScore_Podado(ic[i], coScore[i], subjectScore[i])
    limiarScoreP.append(lsp)

variaveisDic = {
    "IC":           ic,
    "CoEscore":     coScore,
    "SubjectScore": subjectScore,
    "LimiarScore:": limiarScore,
    "LimiarScore (Podado)": limiarScoreP
}
    
texto_json = json.dumps(variaveisDic, indent=4)
print(texto_json)