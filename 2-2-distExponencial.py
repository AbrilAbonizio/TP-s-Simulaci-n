import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

# ==========================================
# INGRESO DE DATOS
# ==========================================

longitud_sucesion = 0
while longitud_sucesion <= 0:
    longitud_sucesion = int(input("Ingrese la cantidad de números a generar: "))

esperanza = 0
while esperanza <= 0:
    esperanza = float(input("Ingrese la esperanza: "))

sucesion = []

# ==========================================
# GENERACIÓN (Libro de Naylor)
# X = -EX * LOG(R)
# ==========================================

for _ in range(longitud_sucesion):
    r = random.random()
    x = -esperanza * math.log(r)
    sucesion.append(x)

# ==========================================
# GRÁFICO
# ==========================================

plt.hist(
    sucesion,
    bins=15,
    density=True,
    color="skyblue",
    edgecolor="black",
    alpha=0.7,
    label="Frecuencia Resultante"
)

x = np.linspace(0, max(sucesion), 1000)

pdf = stats.expon.pdf(
    x,
    scale=esperanza
)

plt.plot(
    x,
    pdf,
    "r--",
    linewidth=2,
    label="PDF Teórica"
)

plt.title(f"Distribución Exponencial (Esperanza = {esperanza})")
plt.xlabel("Valor")
plt.ylabel("Densidad")
plt.legend()
plt.grid(True)
plt.show()

# ==========================================
# TEST GENERAL
# ==========================================

def test_general():

    esperanza_teorica = esperanza
    varianza_teorica = esperanza ** 2

    media = np.mean(sucesion)
    varianza = np.var(sucesion, ddof=1)

    print("\n========== TEST GENERAL ==========")

    print(f"\nEsperanza teórica : {esperanza_teorica:.4f}")
    print(f"Esperanza obtenida: {media:.4f}")

    print(f"\nVarianza teórica : {varianza_teorica:.4f}")
    print(f"Varianza obtenida: {varianza:.4f}")

# ==========================================
# CHI CUADRADO
# ==========================================

def test_chi_cuadrado(alfa=0.05):

    print("\n========== CHI-CUADRADO ==========")

    k = 10

    intervalos = np.linspace(0, max(sucesion), k + 1)

    observados, _ = np.histogram(
        sucesion,
        bins=intervalos
    )

    esperados = []

    for i in range(k):

        prob = stats.expon.cdf(
            intervalos[i + 1],
            scale=esperanza
        ) - stats.expon.cdf(
            intervalos[i],
            scale=esperanza
        )

        esperados.append(prob * len(sucesion))

    esperados = np.array(esperados)

    chi2 = np.sum(
        (observados - esperados) ** 2 / esperados
    )

    grados_libertad = k - 1

    p_valor = 1 - stats.chi2.cdf(
        chi2,
        grados_libertad
    )

    print(f"Chi² = {chi2:.4f}")
    print(f"p-valor = {p_valor:.6f}")

    if p_valor < alfa:
        print("SE RECHAZA H0")
    else:
        print("NO SE RECHAZA H0")

# ==========================================
# KOLMOGOROV-SMIRNOV
# ==========================================

def test_kolmogorov(alfa=0.05):

    print("\n===== KOLMOGOROV-SMIRNOV =====")

    d, p = stats.kstest(
        sucesion,
        "expon",
        args=(0, esperanza)
    )

    print(f"D = {d:.6f}")
    print(f"p-valor = {p:.6f}")

    if p < alfa:
        print("SE RECHAZA H0")
    else:
        print("NO SE RECHAZA H0")


# ==========================================
# EJECUCIÓN
# ==========================================

test_general()

test_chi_cuadrado()

test_kolmogorov()
