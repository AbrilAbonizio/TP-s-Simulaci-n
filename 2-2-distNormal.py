import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# ==========================================
# INGRESO DE DATOS
# ==========================================

longitud_sucesion = 0
while longitud_sucesion <= 0:
    longitud_sucesion = int(input("Ingrese la cantidad de números a generar: "))

media = float(input("Ingrese la media: "))

desvio = 0
while desvio <= 0:
    desvio = float(input("Ingrese el desvío estándar: "))

sucesion = []

# ==========================================
# GENERACIÓN (Libro de Naylor)
# SUM = SUM + R (12 veces)
# X = STDX * (SUM - 6) + EX
# ==========================================

for _ in range(longitud_sucesion):

    suma = 0

    for _ in range(12):
        suma += random.random()

    x = desvio * (suma - 6) + media

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

x = np.linspace(min(sucesion), max(sucesion), 1000)

pdf = stats.norm.pdf(
    x,
    loc=media,
    scale=desvio
)

plt.plot(
    x,
    pdf,
    "r--",
    linewidth=2,
    label="PDF Teórica"
)

plt.title(f"Distribución Normal (μ = {media}, σ = {desvio})")
plt.xlabel("Valor")
plt.ylabel("Densidad")
plt.legend()
plt.grid(True)
plt.show()

# ==========================================
# TEST GENERAL
# ==========================================

def test_general():

    esperanza_teorica = media
    varianza_teorica = desvio ** 2

    esperanza = np.mean(sucesion)
    varianza = np.var(sucesion, ddof=1)

    print("\n========== TEST GENERAL ==========")

    print(f"\nEsperanza teórica : {esperanza_teorica:.4f}")
    print(f"Esperanza obtenida: {esperanza:.4f}")

    print(f"\nVarianza teórica : {varianza_teorica:.4f}")
    print(f"Varianza obtenida: {varianza:.4f}")

# ==========================================
# CHI CUADRADO
# ==========================================

def test_chi_cuadrado(alfa=0.05):

    print("\n========== CHI-CUADRADO ==========")

    k = 10

    intervalos = np.linspace(
        min(sucesion),
        max(sucesion),
        k + 1
    )

    observados, _ = np.histogram(
        sucesion,
        bins=intervalos
    )

    esperados = []

    for i in range(k):

        prob = stats.norm.cdf(
            intervalos[i+1],
            loc=media,
            scale=desvio
        ) - stats.norm.cdf(
            intervalos[i],
            loc=media,
            scale=desvio
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
        "norm",
        args=(media, desvio)
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

