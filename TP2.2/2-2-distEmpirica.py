import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

longitud_sucesion = 0
while longitud_sucesion <= 0:
    longitud_sucesion = int(input("Ingrese la cantidad de numeros a generar: "))

n_valores = 0
while n_valores <= 0:
    n_valores = int(input("Ingrese la cantidad de valores distintos de la distribucion empirica: "))

valores = []
probabilidades = []

for i in range(n_valores):
    x = float(input(f"Ingrese el valor {i+1}: "))
    valores.append(x)

suma_prob = -1
while suma_prob != 1.0:
    probabilidades = []
    suma_prob = 0
    print("Ingrese las probabilidades (deben sumar 1):")
    for i in range(n_valores):
        p = float(input(f"  P(X={valores[i]}) = "))
        probabilidades.append(p)
        suma_prob += p
    if abs(suma_prob - 1.0) > 1e-9:
        print(f"Las probabilidades suman {suma_prob:.4f}, deben sumar 1. Ingreselas nuevamente.")

# ==========================================
# GENERACION (Transformada Inversa)
# ==========================================

sucesion = []

for _ in range(longitud_sucesion):
    r = random.random()
    acum = 0
    for i in range(n_valores):
        acum += probabilidades[i]
        if r <= acum:
            sucesion.append(valores[i])
            break

sucesion = np.array(sucesion)

# ==========================================
# GRAFICO
# ==========================================

valores_unicos, conteos = np.unique(sucesion, return_counts=True)
frecuencias_relativas = conteos / longitud_sucesion

plt.bar(
    [str(v) for v in valores_unicos],
    frecuencias_relativas,
    color="skyblue",
    edgecolor="black",
    alpha=0.7,
    label="Frecuencia Resultante"
)

plt.plot(
    [str(v) for v in valores],
    probabilidades,
    "ro--",
    lw=2,
    label="PMF Teorica"
)

plt.title(f"Distribucion Empirica Discreta - {longitud_sucesion} numeros generados")
plt.xlabel("Valor")
plt.ylabel("Probabilidad / Frecuencia Relativa")
plt.legend()
plt.grid(True)
plt.show()

# ==========================================
# TABLA COMPARATIVA
# ==========================================

valores_unicos, conteos = np.unique(sucesion, return_counts=True)
frecuencias_relativas = conteos / longitud_sucesion

print("\n========== TABLA COMPARATIVA ==========")
print(f"{'Valor':>10} {'Freq. Obtenida':>15} {'Freq. Relativa':>15} {'Prob. Teorica':>15} {'Diferencia':>15}")
print("-" * 70)
for v in valores:
    idx = np.where(valores_unicos == v)[0]
    if len(idx) > 0:
        fo = conteos[idx[0]]
        fr = frecuencias_relativas[idx[0]]
    else:
        fo = 0
        fr = 0.0
    pt = probabilidades[valores.index(v)]
    print(f"{v:>10} {fo:>15} {fr:>15.6f} {pt:>15.6f} {abs(fr - pt):>15.6f}")

# ==========================================
# HISTOGRAMA DE BARRAS
# ==========================================

plt.figure()
plt.bar(
    [str(v) for v in valores_unicos],
    conteos,
    color="skyblue",
    edgecolor="black",
    alpha=0.7
)
plt.title(f"Distribucion Empirica Discreta - Frecuencias Obtenidas ({longitud_sucesion} numeros)")
plt.xlabel("Valor")
plt.ylabel("Frecuencia Absoluta")
plt.grid(True, axis="y")
plt.show()

# ==========================================
# TEST GENERAL
# ==========================================

def test_general(eTeorica, vTeorica):

    sumaMedia = 0
    for n in sucesion:
        sumaMedia += n
    esperanza = sumaMedia / longitud_sucesion

    dif_abs_e = abs(esperanza - eTeorica)

    print("\n========== TEST GENERAL ==========")
    print("ESPERANZA:")
    print("Teorica: ", eTeorica)
    print("Obtenida: ", esperanza)
    print("Diferencia absoluta: ", dif_abs_e)
    margen_permitido_e = 1.96 * math.sqrt(vTeorica) / math.sqrt(longitud_sucesion)
    print("Margen permitido: ", margen_permitido_e)
    print("Veredicto:")
    if dif_abs_e <= margen_permitido_e:
        print("LA ESPERANZA PASA EL TEST")
    else:
        print("LA ESPERANZA NO PASA EL TEST")

    sumaVarianza = 0
    for n in sucesion:
        sumaVarianza = sumaVarianza + (n - esperanza) ** 2
    varianza = sumaVarianza / (longitud_sucesion - 1)

    errorRelV = abs((varianza - vTeorica) / vTeorica)

    print("VARIANZA:")
    print("Teorica: ", vTeorica)
    print("Obtenida: ", varianza)
    print("Error relativo: ", errorRelV)
    margen_permitido_v = 0.05
    print("Margen permitido: ", margen_permitido_v)
    print("Veredicto:")
    if errorRelV <= margen_permitido_v:
        print("LA VARIANZA PASA EL TEST")
    else:
        print("LA VARIANZA NO PASA EL TEST")

# ==========================================
# CHI CUADRADO
# ==========================================

def test_chi_cuadrado(alfa=0.05):

    print("\n========== CHI-CUADRADO ==========")

    observados = []
    esperados = []

    for i in range(n_valores):
        obs = np.sum(sucesion == valores[i])
        esp = probabilidades[i] * longitud_sucesion
        observados.append(obs)
        esperados.append(esp)

    observados = np.array(observados)
    esperados = np.array(esperados)

    chi2 = np.sum((observados - esperados) ** 2 / esperados)

    grados_libertad = n_valores - 1

    p_valor = 1 - stats.chi2.cdf(chi2, grados_libertad)

    print(f"Chi2 = {chi2:.4f}")
    print(f"p-valor = {p_valor:.6f}")

    if p_valor < alfa:
        print("SE RECHAZA H0")
    else:
        print("NO SE RECHAZA H0")

# ==========================================
# EJECUCION
# ==========================================

eTeorica = sum(valores[i] * probabilidades[i] for i in range(n_valores))
vTeorica = sum((valores[i] ** 2) * probabilidades[i] for i in range(n_valores)) - eTeorica ** 2

test_general(eTeorica, vTeorica)

test_chi_cuadrado()
