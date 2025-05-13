import cv2
import numpy as np
import os

# Variables globales para almacenar el punto de inicio de la línea y los puntos extremos
punto_inicio = None
puntos_extremos = []  # Lista para almacenar los puntos finales de las líneas
primer_punto = None  # Almacena el primer punto para cerrar el loop
cerrar_loop = False  # Flag para saber si el loop debe cerrarse automáticamente
loop_num = 1  # Contador de loops

# Variables para manejar las imágenes
imagenes = []  # Lista para almacenar las rutas de las imágenes
indice_imagen = 0  # Índice de la imagen actual
ruta_carpeta = 'imagenes/'  # Ruta de la carpeta con las imágenes

# Obtener todas las imágenes de la carpeta
for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(('.png', '.jpg', '.jpeg')):  # Solo imágenes
        imagenes.append(os.path.join(ruta_carpeta, archivo))

# Si no hay imágenes en la carpeta
if not imagenes:
    print("No se encontraron imágenes en la carpeta.")
    exit()

# Función para manejar los eventos del mouse
def dibujar_linea(event, x, y, flags, param):
    global punto_inicio, puntos_extremos, primer_punto, cerrar_loop

    # Si se hace clic izquierdo, almacena el punto de inicio o el punto final de la línea
    if event == cv2.EVENT_LBUTTONDOWN:
        # Si el loop ya se cerró, no permitir más clics
        if cerrar_loop:
            return

        # Si no hay un punto de inicio, el punto de clic se convierte en el inicio de la línea
        if punto_inicio is None:
            # Guardamos el primer punto y comenzamos la primera línea
            primer_punto = (x, y)  # Guardamos el primer punto
            punto_inicio = (x, y)  # Comenzamos la línea desde el primer punto
        else:
            # Si ya tenemos un punto de inicio, dibujamos la línea y la añadimos a los extremos
            cv2.line(image, punto_inicio, (x, y), (0, 255, 0), 2)  # Trazar la línea verde
            puntos_extremos.append((x, y))  # Agregar el punto final de la línea
            punto_inicio = (x, y)  # El nuevo punto final es el inicio de la siguiente línea

    # Si se hace clic y arrastra el mouse, dibuja la línea provisional
    elif event == cv2.EVENT_MOUSEMOVE:
        if punto_inicio:  # Si ya se ha marcado el punto de inicio
            image_copy = image.copy()  # Crear una copia para no modificar la imagen original
            cv2.line(image_copy, punto_inicio, (x, y), (0, 255, 0), 2)  # Trazar la línea verde
            cv2.imshow("Imagen", image_copy)  # Mostrar la imagen con la línea

# Función para cerrar el loop automáticamente con la tecla 'c'
def cerrar_bucle():
    global cerrar_loop, loop_num, primer_punto, puntos_extremos
    if primer_punto is not None and len(puntos_extremos) > 0:
        # Dibuja la línea de cierre desde el último extremo hasta el primer punto
        cv2.line(image, puntos_extremos[-1], primer_punto, (0, 0, 255), 2)  # Línea roja para cerrar
        cerrar_loop = True  # Establecer el flag de cierre del loop
        puntos_extremos.append(primer_punto)  # Añadir el primer punto como el último punto para completar el ciclo
        # Guardar el loop con sus puntos
        guardar_anotaciones(imagenes[indice_imagen], loop_num)
        loop_num += 1  # Incrementar el número del loop
        # Limpiar los puntos del loop actual para empezar un nuevo loop
        puntos_extremos.clear()
        primer_punto = None  # Asegurarnos de limpiar la variable para el siguiente loop

# Función para guardar las anotaciones en un archivo de texto
def guardar_anotaciones(imagen_path, loop_num):
    nombre_archivo = ruta_carpeta
    nombre_archivo += os.path.splitext(os.path.basename(imagen_path))[0] + '.txt'
    
    with open(nombre_archivo, 'a') as f:
        #f.write(f'Loop {loop_num}:\n')
        
        # Guardamos los puntos del loop en el archivo
        for punto in puntos_extremos:
            f.write(f'{punto[0]}, {punto[1]}\n')
        
        f.write("\n")  # Separador entre anotaciones de diferentes loops

# Función para reiniciar el estado para una nueva imagen
def reiniciar_estado():
    global punto_inicio, puntos_extremos, primer_punto, cerrar_loop, loop_num
    punto_inicio = None
    puntos_extremos = []
    primer_punto = None
    cerrar_loop = False
    loop_num = 1  # Reiniciar el contador de loops

# Cargar la primera imagen
image = cv2.imread(imagenes[indice_imagen])

# Crear una ventana y asignar la función del mouse
cv2.imshow("Imagen", image)
cv2.setMouseCallback("Imagen", dibujar_linea)

# Esperar hasta que se presione la tecla 'q' para cerrar
while True:
    # Mostrar los puntos extremos para ayudar al usuario a conectar líneas
    for punto in puntos_extremos:
        cv2.circle(image, punto, 5, (0, 0, 255), -1)  # Dibujar los puntos finales como círculos rojos
    
    # Mostrar el primer punto de inicio como un círculo azul
    if primer_punto is not None:
        cv2.circle(image, primer_punto, 5, (255, 0, 0), -1)  # Círculo azul para el primer punto

    # Mostrar la imagen actualizada
    cv2.imshow("Imagen", image)

    # Esperar un breve tiempo y verificar si se ha presionado la tecla 'q', 'n', 'c', 'r'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Si se presiona la tecla 'q', cerrar el bucle y guardar
        guardar_anotaciones(imagenes[indice_imagen], loop_num)  # Guardar las anotaciones
        cv2.destroyAllWindows()
        break
    elif key == ord('n'):  # Si se presiona la tecla 'n', pasar a la siguiente imagen
        guardar_anotaciones(imagenes[indice_imagen], loop_num)  # Guardar las anotaciones antes de cambiar de imagen
        # Pasar a la siguiente imagen
        indice_imagen = (indice_imagen + 1) % len(imagenes)  # Ciclamos entre las imágenes
        if indice_imagen == 0:  # Si ya no hay más imágenes, terminar el programa
            print("No hay más imágenes en la carpeta. El programa se cerrará.")
            guardar_anotaciones(imagenes[indice_imagen], loop_num)  # Guardar anotaciones de la última imagen
            cv2.destroyAllWindows()
            break
        image = cv2.imread(imagenes[indice_imagen])  # Cargar la nueva imagen
        reiniciar_estado()  # Restablecer el estado del ciclo para la nueva imagen
        cv2.imshow("Imagen", image)  # Mostrar la nueva imagen

    elif key == ord('c'):  # Si se presiona la tecla 'c', cerrar el loop
        cerrar_bucle()

    elif key == ord('r'):  # Si se presiona la tecla 'r', reiniciar el estado del ciclo
        reiniciar_estado()
        cv2.imshow("Imagen", image)  # Mostrar la imagen actualizada

# Cerrar las ventanas
cv2.destroyAllWindows()
