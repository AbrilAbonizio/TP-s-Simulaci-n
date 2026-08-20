import random

longitud_sucesion = 0
while longitud_sucesion <=0:
    longitud_sucesion = int(input("Ingrese la cantidad de números a generar: "))

sucesion = []
p=-1
while p < 0 or p > 100:
    p = float(input("Ingrese la probabilidad de éxito de cada ensayo de Bernoulli (%): ")) / 100

q = 1-p

kMin = 9 * q / p

k = 0
while k <= 0:
    k = int(input(f"Ingrese la cantidad de ensayos de Bernoulli a utilizar (conviene k >= {kMin}): "))

for _ in range(longitud_sucesion):
    x = 0
    for _ in range(k):
        if random.random() <= p:
            x += 1
    sucesion.append(x)

#print(sucesion)

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

sucesion = np.array(sucesion)

valores_unicos, conteos = np.unique(sucesion, return_counts=True)
frecuencias_relativas = conteos / longitud_sucesion

plt.bar(valores_unicos, frecuencias_relativas, color='skyblue', edgecolor='black', alpha=0.7, label='Frecuencia Resultante')

x_teorico = np.arange(0, k + 1)
pmf_teorica = stats.binom.pmf(x_teorico, k, p)
plt.plot(x_teorico, pmf_teorica, 'ro--', lw=2, label='PMF Teórica Binomial')

plt.title(f'Distribución Binomial - Probabilidad de éxito {p*100}% - Nro. de ensayos {k} - {longitud_sucesion} números generados')
plt.xlabel('Valor generado')
plt.ylabel('Probabilidad / Frecuencia Relativa')
plt.xticks(x_teorico)
plt.legend()
plt.show()


def test_chi_cuadrado(alfa=0.05):

    print("\n========== CHI-CUADRADO ==========")

    x_vals = np.arange(0, k + 1)

    observados = []
    esperados = []

    for x in x_vals:
        obs = np.sum(sucesion == x)
        esp = stats.binom.pmf(x, k, p) * longitud_sucesion
        if esp >= 5:
            observados.append(obs)
            esperados.append(esp)

    resto_obs = 0
    resto_esp = 0.0
    for x in x_vals:
        obs = np.sum(sucesion == x)
        esp = stats.binom.pmf(x, k, p) * longitud_sucesion
        if esp < 5:
            resto_obs += obs
            resto_esp += esp

    if resto_esp >= 5:
        observados.append(resto_obs)
        esperados.append(resto_esp)

    if len(esperados) < 2:
        print("No hay suficientes categorias con frecuencia esperada >= 5 para realizar el test.")
        return

    observados = np.array(observados)
    esperados = np.array(esperados)

    chi2 = np.sum((observados - esperados) ** 2 / esperados)

    grados_libertad = len(esperados) - 1

    p_valor = 1 - stats.chi2.cdf(chi2, grados_libertad)

    print(f"Chi2 = {chi2:.4f}")
    print(f"p-valor = {p_valor:.6f}")

    if p_valor < alfa:
        print("SE RECHAZA H0")
    else:
        print("NO SE RECHAZA H0")


def test_general(eTeorica, vTeorica):
    #calculo de media
    sumaMedia = 0
    for n in sucesion:
        sumaMedia += n
    esperanza = sumaMedia / longitud_sucesion

    dif_abs_e = abs(esperanza - eTeorica)

    print("ESPERANZA:")
    print("Teórica: ", eTeorica)
    print("Obtenida: ", esperanza)
    print("Diferencia absoluta: ", dif_abs_e)
    margen_permitido_e = 1.96 * math.sqrt(vTeorica) / math.sqrt(longitud_sucesion)
    print("Margen permitido: ", margen_permitido_e)
    print("Veredicto:")
    if dif_abs_e <= margen_permitido_e:
        print("LA ESPERANZA PASA EL TEST")
    else:
        print("LA ESPERANZA NO PASA EL TEST")

    #calculo de varianza
    sumaVarianza = 0
    for n in sucesion:
        sumaVarianza = sumaVarianza + (n - esperanza) ** 2
    varianza = sumaVarianza / (longitud_sucesion - 1)

    errorRelV = abs((varianza - vTeorica) / vTeorica)

    print("VARIANZA:")
    print("Teórica: ", vTeorica)
    print("Obtenida: ", varianza)
    print("Error relativo: ", errorRelV)
    margen_permitido_v = 0.05
    print("Margen permitido: ", margen_permitido_v)
    print("Veredicto:")
    if errorRelV <= margen_permitido_v:
        print("LA VARIANZA PASA EL TEST")
    else:
        print("LA VARIANZA NO PASA EL TEST")

eTeorica = k * p
vTeorica = k * p * q
test_general(eTeorica, vTeorica)
test_chi_cuadrado()