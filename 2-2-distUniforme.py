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

a = float(input("Ingrese el límite inferior (A): "))
b = float(input("Ingrese el límite superior (B): "))

while b <= a:
    b = float(input("B debe ser mayor que A. Ingrese nuevamente: "))

sucesion = []

# ==========================================
# GENERACIÓN (Libro de Naylor)
# X = A + (B-A)*R
# ==========================================

for _ in range(longitud_sucesion):
    r = random.random()
    x = a + (b - a) * r
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

x = np.linspace(a - 1, b + 1, 1000)

pdf = stats.uniform.pdf(
    x,
    loc=a,
    scale=b - a
)

plt.plot(
    x,
    pdf,
    "r--",
    linewidth=2,
    label="PDF Teórica"
)

plt.title(f"Distribución Uniforme [{a}, {b}]")
plt.xlabel("Valor")
plt.ylabel("Densidad")
plt.legend()
plt.grid(True)
plt.show()

# ==========================================
# TEST GENERAL
# ==========================================

def test_general():

    esperanza_teorica = (a + b) / 2
    varianza_teorica = (b - a) ** 2 / 12

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

    intervalos = np.linspace(a, b, k + 1)

    observados, _ = np.histogram(
        sucesion,
        bins=intervalos
    )

    esperados = np.ones(k) * len(sucesion) / k

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
        "uniform",
        args=(a, b - a)
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