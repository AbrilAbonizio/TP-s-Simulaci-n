import random

longitud_sucesion = 0
while longitud_sucesion <=0:
    longitud_sucesion = int(input("Ingrese la cantidad de números a generar: "))

sucesion = []

esperanza = float(input("Ingrese el valor la esperanza: "))
stdev = float(input("Ingrese el valor la varianza: "))

k=12
for _ in range(longitud_sucesion):
    suma = 0
    for _ in range(k):
        suma += random.random()
    sucesion.append(stdev * (suma - 6) + esperanza)

print(sucesion)

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


plt.hist(sucesion, bins=15, density=True, color='skyblue', edgecolor='black', alpha=0.7)

x = np.linspace(0, max(sucesion), 1000)
pdf_teorica = stats.expon.pdf(x, scale=esperanza)
plt.plot(x, pdf_teorica, 'r--', lw=2, label='PDF Teórica')

plt.title(f'Distribución Normal - Esperanza {esperanza} - Desvío Estándar {stdev}')
plt.xlabel('Valor generado')
plt.ylabel('Densidad')
plt.legend()
plt.show()


def test_chi_cuadrado(sucesion_numeros, tipo, alfa=0.05):
    print(f" \n  PRUEBA DE CHI-CUADRADO ({tipo})")

    k = 10
    longitud_sucesion = len(sucesion_numeros)
    intervalos = np.linspace(0.0, 1.0, k + 1)  # Define los intervalos
    observados, _ = np.histogram(sucesion_numeros, bins=intervalos)  # Cuenta las frecuencias observadas
    esperados = longitud_sucesion / k  # Calculo de la frecuencia esperada

    chi_cuadrado_tabla = [((o_i - esperados) ** 2) / esperados for o_i in observados]
    estadistico_chi2 = sum(chi_cuadrado_tabla)

    grados_libertad = k - 1
    p_valor = 1 - stats.chi2.cdf(estadistico_chi2, grados_libertad)

    print(
        f"\nCantidad de números evaluados (n): {longitud_sucesion} \nIntervalos: {k} \nFrecuencia esperada por intervalo: {esperados}")
    print("\n")
    print("Distribución de los números en los intervalos:")
    for i in range(k):
        print(f" Intervalo [{intervalos[i]:.1f} - {intervalos[i + 1]:.1f}): Observados = {observados[i]}")
    print("\n")
    print(f"Estadístico Chi-cuadrado calculado (X²): {estadistico_chi2:.4f}")
    print(f"p-valor obtenido: {p_valor:.6f}")
    print(f"Nivel de significancia (alfa): {alfa}")
    print("\n")

    if p_valor < alfa:
        print("SE RECHAZA H0 (Los números NO son uniformes)")
        print("El generador NO pasa la prueba de uniformidad")
    else:
        print("NO SE RECHAZA H0 (Los números son uniformes)")
        print("El generador PASA la prueba de uniformidad")


def entero_a_binario(lista_enteros, cant_bits):
    return "".join(f"{num:0{cant_bits}b}" for num in lista_enteros)