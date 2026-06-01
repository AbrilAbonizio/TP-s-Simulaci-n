import sys
import random
import matplotlib.pyplot as plt

print(sys.argv)
# Valida que los argumentos sean los correctos
if (len(sys.argv) != 5 or sys.argv[1] != "-g" or sys.argv[3] != "-n"):
  print("Parámetros Incorrectos")
  sys.exit(1)

tipo_generador = str(sys.argv[2])
longitud_sucesion = int(sys.argv[4])

sucesion = []
seed = 0
mGCL = pow(2,32)

while seed <= 0 or seed >= mGCL:
    seed = int(input("Ingresar la semilla: "))
    if seed <= 0 or seed >= mGCL:
        print("La semilla debe ser un valor entero entre 0 y 4.294.967.296")
sucesion.append(seed)

if tipo_generador == "GCL":
   a = random.randint(0,mGCL-1 // 4) * 4 + 1  
   c = random.randint(0,mGCL-1)
   c = c | 1 # Fuerza que sea impar
   for i in range(0,longitud_sucesion):
      sucesion.append((a*sucesion[-1]+c) % mGCL)

print("a utilizado = " + str(a))
print("c utilizado = " + str(c))
print("m utilizado = " + str(mGCL))
print("Los " + str(longitud_sucesion) + " generados son: ")
print(sucesion[1:])

plt.figure(figsize=(10,5))
plt.suptitle(f"{longitud_sucesion} números generados - Generador {tipo_generador} - Semilla {seed}")
plt.title("Números generados")
plt.xlabel("n")
plt.ylabel("res (Nómero generado)")
generacion = list(range(1, longitud_sucesion + 1))
plt.scatter(generacion, sucesion[1:], color='red', s=10, label='Número generado')

plt.tight_layout()
plt.subplots_adjust(hspace=0.5, top=0.9)
plt.show()