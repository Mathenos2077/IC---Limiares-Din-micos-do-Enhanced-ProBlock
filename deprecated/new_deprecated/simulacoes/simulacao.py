import saida.calculo_limiarScore as limiarScore

icFinal = 1.00
coScoreFinal = 0.65
subjectScoreFinal = 1.00

limiarScoreFinal_np = limiarScore.getLimiarScore_NaoPodado(coScoreFinal, icFinal, subjectScoreFinal)
limiarScoreFinal_p = limiarScore.getLimiarScore_Podado(coScoreFinal, icFinal, subjectScoreFinal)

print("Limiar Score = ", round(limiarScoreFinal_np, 4))