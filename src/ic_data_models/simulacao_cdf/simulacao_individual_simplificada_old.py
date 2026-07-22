import utils


weightedVotes = [-32, 0, -78, -45, 0]

cdf = utils.getCDF(weightedVotes)

limDown = 0.3
limUp = 0.7

conclusao = ""
if cdf <= limDown:
    conclusao = "Completamente Falsa"
elif limDown < cdf <= limUp:
    conclusao = "Inconclusivo"
elif limUp < cdf:
    conclusao = "Completamente Verdadeira"


print("WeightedVotes = ", weightedVotes)
print("CDF = ", cdf)
print("CDF (numpy) = ", cdf_numpy)
print("CDF (calculado) = ", cdf_calculado2)
print("\n---------------   LIMIARES ANTIGOS   -----------------------")
print(f"     Completamente Falsa: 0.0 < CDF <= {limDown}")
print(f"            Inconclusivo: {limDown} < CDF <= {limUp}")
print(f"Completamente Verdadeira: {limUp} < CDF <= 1.0")
print(f"\n---------> Conclusão: {conclusao}")