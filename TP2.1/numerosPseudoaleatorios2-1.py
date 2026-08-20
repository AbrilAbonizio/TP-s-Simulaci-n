import sys
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

print(sys.argv)
# Valida que los argumentos sean los correctos
if (len(sys.argv) != 5 or sys.argv[1] != "-g" or sys.argv[3] != "-n"):
  print("Parámetros Incorrectos")
  sys.exit(1)

tipo_generador = str(sys.argv[2])
longitud_sucesion = int(sys.argv[4])

sucesion = []
sucesion_real = []
sucesion_binario = []
seed = 0

numeros_aleatorios = [
    0.5938, 0.4471, 0.6797, 0.4878, 0.4232, 0.7406, 0.6033, 0.8355, 0.9528, 0.5853,
    0.6074, 0.7301, 0.6206, 0.3892, 0.0846, 0.6711, 0.2870, 0.4429, 0.3475, 0.5548,
    0.8314, 0.1382, 0.0039, 0.9837, 0.5244, 0.3184, 0.5238, 0.4113, 0.7411, 0.2617,
    0.0077, 0.5751, 0.5063, 0.8450, 0.4995, 0.5574, 0.0966, 0.5741, 0.9835, 0.2036,
    0.2408, 0.0302, 0.0966, 0.8113, 0.7029, 0.4888, 0.2650, 0.9119, 0.1834, 0.5426,
    0.8930, 0.6945, 0.5454, 0.3055, 0.5134, 0.3679, 0.0334, 0.0865, 0.6372, 0.1862,
    0.8653, 0.6332, 0.2037, 0.1523, 0.6922, 0.5771, 0.2521, 0.6871, 0.5874, 0.4117,
    0.8491, 0.8037, 0.1886, 0.9083, 0.9632, 0.5702, 0.5344, 0.2175, 0.6485, 0.6190,
    0.5272, 0.2374, 0.0771, 0.2963, 0.3583, 0.7498, 0.2370, 0.3332, 0.9180, 0.8209,
    0.0079, 0.5054, 0.0557, 0.0355, 0.4616, 0.7997, 0.3702, 0.7257, 0.0221, 0.6456,
    0.1226, 0.4591, 0.9790, 0.3966, 0.4538, 0.7651, 0.7398, 0.5504, 0.0582, 0.5801,
    0.5958, 0.8846, 0.8847, 0.0083, 0.3457, 0.5290, 0.1467, 0.6690, 0.0828, 0.6190,
    0.9657, 0.7666, 0.8108, 0.5693, 0.3680, 0.9660, 0.9246, 0.7856, 0.8638, 0.5420,
    0.1369, 0.1456, 0.0785, 0.6369, 0.8607, 0.1441, 0.9057, 0.8148, 0.1593, 0.7193,
    0.9327, 0.1439, 0.5723, 0.0046, 0.1338, 0.7497, 0.3376, 0.4484, 0.0417, 0.5709,
    0.8927, 0.7768, 0.7767, 0.6938, 0.8486, 0.3020, 0.0162, 0.1979, 0.8067, 0.1339,
    0.5501, 0.0738, 0.1832, 0.4749, 0.5773, 0.7163, 0.4056, 0.3730, 0.1028, 0.8402,
    0.7515, 0.5318, 0.2413, 0.2366, 0.8228, 0.5168, 0.8771, 0.2006, 0.5086, 0.5573,
    0.3057, 0.5994, 0.4868, 0.3329, 0.8067, 0.5387, 0.0365, 0.1065, 0.4871, 0.4217,
    0.6629, 0.4103, 0.0922, 0.6088, 0.4167, 0.0879, 0.1781, 0.9144, 0.8465, 0.2345,
    0.0686, 0.7519, 0.0560, 0.8533, 0.8226, 0.8248, 0.8240, 0.8214, 0.2919, 0.4671,
    0.9884, 0.1593, 0.3590, 0.5216, 0.9652, 0.1487, 0.6628, 0.8509, 0.9596, 0.7408,
    0.4602, 0.7613, 0.0526, 0.4346, 0.9505, 0.7124, 0.3143, 0.4079, 0.4224, 0.1177,
    0.3979, 0.0910, 0.9252, 0.1718, 0.1693, 0.1495, 0.9433, 0.7952, 0.9064, 0.7240,
    0.6454, 0.2478, 0.6250, 0.1837, 0.6039, 0.1845, 0.0699, 0.5326, 0.3983, 0.7139,
    0.7285, 0.9802, 0.9894, 0.0934, 0.2007, 0.1343, 0.2695, 0.3715, 0.9123, 0.5347,
    0.3615, 0.4043, 0.9550, 0.0514, 0.5620, 0.5520, 0.2824, 0.2144, 0.7469, 0.3808,
    0.3433, 0.5402, 0.2799, 0.5368, 0.2314, 0.9955, 0.3157, 0.3767, 0.2512, 0.0830,
    0.4434, 0.8660, 0.4656, 0.4108, 0.4035, 0.8894, 0.5133, 0.1514, 0.9624, 0.9229,
    0.3403, 0.3239, 0.7350, 0.2480, 0.3325, 0.7952, 0.8624, 0.9922, 0.0419, 0.0558,
    0.5895, 0.3242, 0.6948, 0.5812, 0.3675, 0.0076, 0.4134, 0.0993, 0.6831, 0.4092,
    0.4118, 0.7532, 0.1141, 0.6670, 0.8788, 0.0665, 0.5391, 0.6125, 0.8337, 0.3124,
    0.6338, 0.8177, 0.8655, 0.6171, 0.1272, 0.6315, 0.2402, 0.1813, 0.5816, 0.4787,
    0.8229, 0.9272, 0.0655, 0.7290, 0.3518, 0.9414, 0.1330, 0.5174, 0.0179, 0.2677,
    0.0016, 0.9589, 0.0234, 0.9070, 0.0419, 0.9744, 0.1023, 0.3986, 0.6098, 0.4010,
    0.5223, 0.3995, 0.5259, 0.3444, 0.0791, 0.9895, 0.7288, 0.3530, 0.7250, 0.3990,
    0.2716, 0.8322, 0.5894, 0.1073, 0.6385, 0.6305, 0.2747, 0.3766, 0.2242, 0.7994,
    0.3828, 0.9129, 0.4817, 0.4063, 0.1294, 0.6364, 0.9948, 0.8120, 0.5590, 0.9631,
    0.1994, 0.6539, 0.5039, 0.0688, 0.1616, 0.5350, 0.0614, 0.0716, 0.9088, 0.2314,
    0.0247, 0.7210, 0.0029, 0.2464, 0.0147, 0.3243, 0.5275, 0.9460, 0.0683, 0.6897,
    0.1611, 0.6546, 0.3449, 0.8202, 0.8913, 0.9693, 0.8628, 0.7698, 0.3685, 0.6067,
    0.7095, 0.4360, 0.9286, 0.7294, 0.9713, 0.6921, 0.2579, 0.5076, 0.1052, 0.0040,
    0.6302, 0.7487, 0.6811, 0.4864, 0.0000, 0.6848, 0.6786, 0.5085, 0.3845, 0.3060,
    0.2779, 0.1761, 0.9610, 0.4991, 0.2173, 0.2910, 0.9262, 0.4182, 0.5985, 0.4293,
    0.7369, 0.7077, 0.2114, 0.8871, 0.2727, 0.5418, 0.7647, 0.5215, 0.0401, 0.0739,
    0.8981, 0.2147, 0.5602, 0.7631, 0.7485, 0.6578, 0.3560, 0.3664, 0.9453, 0.8821,
    0.6308, 0.4204, 0.1155, 0.9434, 0.5629, 0.8485, 0.2077, 0.3070, 0.2147, 0.8825,
    0.6208, 0.5302, 0.7488, 0.0029, 0.6016, 0.9423, 0.9344, 0.6102, 0.0650, 0.5462,
    0.5743, 0.9600, 0.8833, 0.8704, 0.2742, 0.5397, 0.4121, 0.7496, 0.1334, 0.9891,
    0.8643, 0.1437, 0.0920, 0.8653, 0.4972, 0.4409, 0.6511, 0.2345, 0.4726, 0.0918,
    
    0.2700, 0.9257, 0.9801, 0.3930, 0.2259, 0.5720, 0.3786, 0.3108, 0.1978, 0.6569,
    0.2890, 0.7962, 0.0511, 0.3990, 0.8730, 0.2154, 0.4081, 0.9096, 0.8474, 0.5795,
    0.6139, 0.9289, 0.3464, 0.5456, 0.9056, 0.7534, 0.0456, 0.5287, 0.5206, 0.0728,
    0.6691, 0.9790, 0.1122, 0.8825, 0.9481, 0.9056, 0.7018, 0.4574, 0.2539, 0.3461,
    0.2511, 0.1970, 0.8526, 0.7894, 0.5145, 0.9379, 0.3286, 0.6823, 0.0469, 0.2226,
    0.4226, 0.6481, 0.0631, 0.4852, 0.6338, 0.5343, 0.5361, 0.1555, 0.3893, 0.9970,
    0.8324, 0.2902, 0.3476, 0.6492, 0.4638, 0.6235, 0.9343, 0.3832, 0.2557, 0.8737,
    0.3332, 0.6849, 0.7348, 0.1405, 0.0582, 0.3506, 0.2756, 0.2595, 0.6302, 0.0573,
    0.7415, 0.6509, 0.6261, 0.5411, 0.7601, 0.8039, 0.0086, 0.2199, 0.3450, 0.2130,
    0.0398, 0.5487, 0.7990, 0.6212, 0.2598, 0.7234, 0.7315, 0.8069, 0.9130, 0.4982,
    0.4932, 0.7194, 0.1053, 0.1110, 0.6563, 0.8195, 0.9629, 0.2793, 0.5666, 0.8294,
    0.8481, 0.4565, 0.6466, 0.0007, 0.5474, 0.2229, 0.5315, 0.2366, 0.1465, 0.5487,
    0.8949, 0.2032, 0.7094, 0.1882, 0.4143, 0.7826, 0.2693, 0.2188, 0.4570, 0.2196,
    0.1881, 0.7272, 0.6329, 0.5623, 0.4785, 0.4420, 0.2763, 0.1937, 0.6322, 0.4635,
    0.2427, 0.7398, 0.6256, 0.1959, 0.5534, 0.6514, 0.3693, 0.5363, 0.9239, 0.2969,
    0.3138, 0.2722, 0.3532, 0.0611, 0.8325, 0.0250, 0.0652, 0.0375, 0.1106, 0.2561,
    0.5235, 0.3267, 0.1538, 0.0339, 0.8534, 0.6020, 0.3449, 0.4834, 0.0494, 0.1988,
    0.0881, 0.7453, 0.0721, 0.8444, 0.3934, 0.8921, 0.0190, 0.6329, 0.4022, 0.7603,
    0.1415, 0.8320, 0.4947, 0.6469, 0.9491, 0.1020, 0.5448, 0.1687, 0.0069, 0.5180,
    0.8320, 0.0909, 0.3904, 0.7460, 0.2060, 0.7425, 0.8743, 0.9475, 0.0974, 0.9632,
    0.5660, 0.8948, 0.4979, 0.8593, 0.5857, 0.2207, 0.4477, 0.2896, 0.6537, 0.4977,
    0.2950, 0.4971, 0.8516, 0.9636, 0.3635, 0.4508, 0.7268, 0.0344, 0.1387, 0.2030,
    0.5383, 0.4574, 0.8583, 0.1420, 0.2800, 0.3822, 0.8890, 0.0112, 0.8741, 0.2100,
    0.5142, 0.8369, 0.1677, 0.1281, 0.6728, 0.2223, 0.9282, 0.8408, 0.1182, 0.0131,
    0.3013, 0.4081, 0.3543, 0.6360, 0.9691, 0.7027, 0.0684, 0.4548, 0.4608, 0.3097,
    0.0544, 0.4551, 0.7040, 0.9312, 0.1948, 0.2620, 0.9462, 0.7344, 0.4155, 0.6639,
    0.8826, 0.1808, 0.3839, 0.6044, 0.2378, 0.1866, 0.5384, 0.3056, 0.2645, 0.8666,
    0.5653, 0.2500, 0.8360, 0.0665, 0.6961, 0.4545, 0.8090, 0.1241, 0.7086, 0.5861,
    0.6070, 0.4451, 0.8511, 0.6273, 0.3300, 0.5626, 0.5495, 0.3329, 0.0841, 0.9690,
    0.3023, 0.8061, 0.8185, 0.5980, 0.3277, 0.7321, 0.7708, 0.7480, 0.9094, 0.3085,
    0.6074, 0.5205, 0.8293, 0.9671, 0.3442, 0.9982, 0.0357, 0.0883, 0.0998, 0.0853,
    0.6942, 0.1669, 0.3804, 0.1283, 0.4689, 0.4108, 0.1967, 0.0242, 0.6581, 0.7937,
    0.3462, 0.7135, 0.7322, 0.8058, 0.5638, 0.2705, 0.2669, 0.6193, 0.8145, 0.5202,
    0.7978, 0.0894, 0.0357, 0.7803, 0.1461, 0.8773, 0.5903, 0.1067, 0.5404, 0.4549,
    0.2710, 0.3510, 0.6060, 0.2744, 0.4028, 0.0738, 0.9366, 0.6289, 0.6515, 0.3525,
    0.2061, 0.8204, 0.8340, 0.5122, 0.6873, 0.5348, 0.0062, 0.2672, 0.9405, 0.5315,
    0.2034, 0.4045, 0.6401, 0.6348, 0.0503, 0.2057, 0.4116, 0.9356, 0.9700, 0.2709,
    0.5709, 0.4688, 0.8985, 0.5964, 0.8487, 0.3495, 0.0576, 0.8504, 0.1383, 0.6274,
    0.7710, 0.1965, 0.2846, 0.9891, 0.4238, 0.5172, 0.4421, 0.8365, 0.2704, 0.9288,
    0.4251, 0.1837, 0.6987, 0.0267, 0.7542, 0.9593, 0.2431, 0.6504, 0.3565, 0.5927,
    0.0489, 0.6537, 0.8085, 0.7010, 0.5609, 0.3856, 0.5582, 0.8978, 0.3096, 0.5089,
    0.3422, 0.9655, 0.5667, 0.0064, 0.5915, 0.1829, 0.3123, 0.3637, 0.3563, 0.0606,
    0.2481, 0.8823, 0.1939, 0.6375, 0.3722, 0.4612, 0.5091, 0.8149, 0.8537, 0.3108,
    0.0404, 0.0955, 0.1758, 0.5016, 0.8487, 0.9944, 0.9480, 0.3270, 0.5666, 0.3737,
    0.5915, 0.4105, 0.0602, 0.0449, 0.9463, 0.1109, 0.1896, 0.5714, 0.8344, 0.7335,
    0.8853, 0.6535, 0.1112, 0.9903, 0.4229, 0.8947, 0.3876, 0.5029, 0.2243, 0.0072,
    0.0534, 0.7955, 0.8947, 0.3050, 0.5394, 0.5169, 0.2091, 0.8820, 0.8351, 0.9153,
    0.0744, 0.5102, 0.1460, 0.9676, 0.7449, 0.7981, 0.8580, 0.6438, 0.6091, 0.1305,
    0.0661, 0.3522, 0.4447, 0.9943, 0.6206, 0.2273, 0.9958, 0.9442, 0.1648, 0.7005,
    0.2969, 0.4991, 0.0483, 0.2728, 0.3450, 0.3791, 0.3691, 0.0640, 0.7197, 0.4363
]

def generador_GCL(seed):
  global sucesion_binario
  mGCL = pow(2,32) 
  while seed <= 0 or seed >= mGCL:
    seed = int(input("Ingresar la semilla: "))
    if seed <= 0 or seed >= mGCL:
      print("La semilla debe ser un valor entero entre 0 y 4.294.967.296")

  a = random.randint(0,(mGCL-1) // 4) * 4 + 1  
  c = random.randint(0,mGCL-1)
  c = c | 1 # Fuerza que sea impar
  
  valor = seed
  
  for i in range(0,longitud_sucesion):
    valor = (a*valor+c) % mGCL
    sucesion.append(valor)
    sucesion_real.append(valor/mGCL)

  sucesion_binario = entero_a_binario(sucesion,32)  

  print("a utilizado = " + str(a))
  print("c utilizado = " + str(c))
  print("m utilizado = " + str(mGCL))
  
  return seed


def generador_CM(seed):  # CM = Cuadrados Medios
  global sucesion_binario
  while seed <= 0 or len(str(seed)) != 4:
    seed = int(input("Ingresar la semilla: "))
    if seed <= 0 or len(str(seed)) != 4:
      print("La semilla debe ser un valor entero mayor a 0 y de 4 dígitos")
  
  nueva_semilla = int(seed)

  for _ in range(0, longitud_sucesion):
    
    valor = nueva_semilla ** 2
    valor_str = str(valor)
        
    if len(valor_str) != 8:
      valor_str = valor_str.zfill(8)

    centro = valor_str[2:6]
    nueva_semilla = int(centro)

    sucesion.append(nueva_semilla)
    sucesion_real.append(nueva_semilla/10000)

  sucesion_binario = entero_a_binario(sucesion, 14) # La representación en binario de la salida ocupa como max 14 bits
  
  return seed 


def generador_Mersenne_Twister(seed):
  global sucesion_binario
  while seed <= 0:
    seed = int(input("Ingresar la semilla: "))
    if seed <= 0:
      print("La semilla debe ser un valor entero mayor a 0")
  
  random.seed(seed)

  m_mt = pow(2,32)

  for _ in range(0, longitud_sucesion):
    numero_entero = random.getrandbits(32)
    sucesion.append(numero_entero)

    numero_real = numero_entero / m_mt
    sucesion_real.append(numero_real)
  
  sucesion_binario = entero_a_binario(sucesion, 32)

  return seed


def test_chi_cuadrado(sucesion_numeros, tipo, alfa=0.05):
    
    # Normalización de los datos
  #if tipo == "GCL":
    #mGCL = pow(2, 32)
    #datos = [x / mGCL for x in sucesion_numeros]
        
  #if tipo == "CM":
    #datos = [x / 10000 for x in sucesion_numeros]
        
  if tipo == "MT": # Solo para generador MT
    datos = sucesion_numeros 

  
  print(f" \n  PRUEBA DE CHI-CUADRADO ({tipo})")
    
  k = 10
  longitud_sucesion = len(sucesion_numeros)
  intervalos = np.linspace(0.0, 1.0, k + 1) # Define los intervalos
  observados, _ = np.histogram(sucesion_numeros, bins=intervalos) # Cuenta las frecuencias observadas
  esperados = longitud_sucesion / k   # Calculo de la frecuencia esperada
    
  chi_cuadrado_tabla = [((o_i - esperados) ** 2) / esperados for o_i in observados]
  estadistico_chi2 = sum(chi_cuadrado_tabla)
    
  grados_libertad = k - 1
  p_valor = 1 - stats.chi2.cdf(estadistico_chi2, grados_libertad)

  print(f"\nCantidad de números evaluados (n): {longitud_sucesion} \nIntervalos: {k} \nFrecuencia esperada por intervalo: {esperados}")
  print("\n")
  print("Distribución de los números en los intervalos:")
  for i in range(k):
    print(f" Intervalo [{intervalos[i]:.1f} - {intervalos[i+1]:.1f}): Observados = {observados[i]}")
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


def test_frecuencia_monobit(cadena):
  n = len(cadena)
  print("----------TEST FRECUENCIA MONOBIT---------------")
  print("Funciona mejor en cadenas de más de 100 bits. La cadena tiene ", n, " bits.")

  cant_unos = cadena.count('1')
  cant_ceros = n - cant_unos
  suma_monobit = cant_unos - cant_ceros

  estadistico_prueba = abs(suma_monobit) / math.sqrt(n)

  p_value =   math.erfc(estadistico_prueba / math.sqrt(2))

  if p_value < 0.01:
    print("El generador NO PASA la prueba de frecuencia monobit.")
  else:
    print("El generador PASA la prueba de frecuencia monobit.")
  
  return cant_unos / n
  


def test_frecuencia_bloque(cadena):
  n = len(cadena)

  print("----------TEST FRECUENCIA DENTRO DEL BLOQUE---------------")
  print("Funciona mejor en cadenas de más de 100 bits. La cadena tiene ", n, " bits.")

  cant_bloques_max = min(99, n // 20)

  if cant_bloques_max < 2:
    print("La cadena es demasiado corta para hacer un test válido.")

  else:
    cant_bloques = random.randint(2, cant_bloques_max)
    tam_bloque = n // cant_bloques
    print("Se usarán ", cant_bloques, " bloques de ", tam_bloque, " bits cada uno.")

    proporciones = [ # Array con la proporcion de 1s en cada bloque
      cadena[i:i + tam_bloque].count('1') / tam_bloque 
      for i in range(0, cant_bloques * tam_bloque, tam_bloque)
      ]
    suma_desvios = sum((pi - 0.5)**2 for pi in proporciones)
    chi_sq_obs = 4 * tam_bloque * suma_desvios

    p_value = stats.chi2.sf(chi_sq_obs, cant_bloques)

    if p_value < 0.01:
      print("El generador NO PASA la prueba de frecuencia de bloque.")
    else:
      print("El generador PASA la prueba de frecuencia de bloque.")


def test_rachas(cadena, pi):
  n = len(cadena)
  print("----------TEST DE RACHAS---------------")
  print("Funciona mejor en cadenas de más de 100 bits. La cadena tiene ", n, " bits.")
  print()
  print("PRE-TEST:")
  if abs(pi - 0.5) >= 2 / math.sqrt(n):
        print("NO PASA pre-test -> NO PASA el test de rachas")
  else:
    print("PASA pre-test")
    print("TEST DE RACHAS")
    
    saltos = 0

    for i in range(n-1):
      if cadena[i] != cadena[i+1]:
        saltos += 1
    
    vn_obs = saltos + 1

    num = abs(vn_obs - 2 * n * pi * (1 - pi))
    den = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_value = math.erfc(num / den)

    if p_value < 0.01:
      print("El generador NO PASA la prueba de rachas.")
    else:
      print("El generador PASA la prueba de rachas.")  


def entero_a_binario(lista_enteros, cant_bits):
  return "".join(f"{num:0{cant_bits}b}" for num in lista_enteros)


# PROGRAMA PRINCIPAL 
if tipo_generador == "GCL":
  seed = generador_GCL(seed) 
elif tipo_generador == "CM":
  seed = generador_CM(seed)
elif tipo_generador == "MT":
  seed = generador_Mersenne_Twister(seed)

test_chi_cuadrado(sucesion_real, tipo_generador)

pi_monobit = test_frecuencia_monobit(sucesion_binario)

test_frecuencia_bloque(sucesion_binario)

test_rachas(sucesion_binario, pi_monobit)

# Test numeros aleatorios
aleatorios_enteros = [int(i * (2**13)) for i in numeros_aleatorios] # Se sacrifica precisión para obtener un resultado no sesgado por el espacio de valores sobrantes.
aleatorios_binarios = entero_a_binario(aleatorios_enteros, 13)
test_chi_cuadrado(numeros_aleatorios, "random.org")
pi_monobit = test_frecuencia_monobit(aleatorios_binarios)
test_frecuencia_bloque(aleatorios_binarios)
test_rachas(aleatorios_binarios, pi_monobit)

plt.figure(figsize=(10,5))
plt.suptitle(f"{longitud_sucesion} números generados - Generador {tipo_generador} - Semilla {seed}")
generacion = list(range(1, longitud_sucesion + 1))
plt.title("Números Pseudo-Aleatorios")
plt.xlabel("n")
plt.ylabel("res (Número generado)")
plt.scatter(generacion, sucesion, color='red', s=10, label='Número generado')

plt.figure(figsize=(10,5))
plt.suptitle("Números Aleatorio - Generador random.org")
plt.xlabel("n")
plt.ylabel("res (Número Obtenido)")

if longitud_sucesion <= len(numeros_aleatorios):
  numeros_a_graficar = numeros_aleatorios[:longitud_sucesion]
  eje_x_random = list(range(1, longitud_sucesion + 1))
else:
  numeros_a_graficar = numeros_aleatorios
  eje_x_random = list(range(1, len(numeros_aleatorios) + 1))

plt.scatter(eje_x_random, numeros_a_graficar, color='red', s=10, label='Número Obtenido')
plt.legend()

plt.tight_layout()
plt.subplots_adjust(hspace=0.5, top=0.9)
plt.show()