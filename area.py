import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def calcular_area(puntos):
    """Calcula el área de un polígono dado un conjunto de puntos."""
    n = len(puntos)
    area = 0
    for i in range(n):
        j = (i + 1) % n  # siguiente punto, con retorno al inicio
        area += puntos[i][0] * puntos[j][1]
        area -= puntos[j][0] * puntos[i][1]
    area = abs(area) / 2.0
    return area

def leer_datos(filename):
    """Lee los datos del archivo y los organiza en grupos de loops."""
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    loops = []
    loop = []
    
    for line in lines:
        # Eliminar espacios en blanco y saltos de línea
        line = line.strip()
        
        if line == "":
            # Si hay una línea vacía, significa que termina un loop
            if loop:
                loops.append(loop)
                loop = []
        else:
            # Añadir las coordenadas a la lista del loop actual
            x, y = map(int, line.split(','))
            loop.append((x, y))
    
    # Añadir el último loop si no está vacío
    if loop:
        loops.append(loop)
    
    return loops

# Lee los datos desde el archivo
filename = "imagenes/imagen.txt"  # Asegúrate de que el archivo esté en el mismo directorio o ajusta la ruta
loops = leer_datos(filename)

# Cargar la imagen
image_path = filename.replace('.txt', '.png')  # La imagen tiene el mismo nombre que el archivo de texto
image = Image.open(image_path)

# Crear la figura para graficar
plt.figure(figsize=(10, 10))
plt.imshow(image, cmap='gray', origin='upper')  # Mostrar la imagen en escala de grises

# Graficar cada loop sobre la imagen
for i, loop in enumerate(loops):
    # Convertir los puntos a un array para graficar
    loop = np.array(loop)
    x = loop[:, 0]
    y = loop[:, 1]

    # Calcular el área del loop
    area = calcular_area(loop)
    print(f"Área del loop {i+1}: {area:.2f} px²")
    
    # Dibujar el polígono sobre la imagen
    plt.plot(np.append(x, x[0]), np.append(y, y[0]), label=f"Loop {i+1} (Área: {area:.2f} px²)", linewidth=2)

# Añadir título y leyenda
plt.title("Imagen con los loops y sus áreas")
plt.legend()

# Mostrar la imagen con los loops dibujados
plt.axis('off')  # Ocultar los ejes
plt.show()
