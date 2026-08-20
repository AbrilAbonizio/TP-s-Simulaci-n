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

eTeorica = (a + b) / 2
vTeorica = (b - a) ** 2 / 12

test_general(eTeorica, vTeorica)


test_kolmogorov()