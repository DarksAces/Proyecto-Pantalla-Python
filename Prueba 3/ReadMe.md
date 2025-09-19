Proyecto: Editor Interactivo de Imágenes y Texto con Pygame

Descripción:

Este proyecto es un editor interactivo desarrollado en Python con Pygame. Permite:

Cargar y mostrar imágenes.

Mover y redimensionar imágenes movibles con el ratón.

Editar texto directamente en la ventana gráfica, línea por línea.

El editor demuestra cómo manejar múltiples objetos gráficos, detectar colisiones y aplicar transformaciones en tiempo real dentro de Pygame.

Funcionalidades implementadas:

Carga automática de imágenes desde la carpeta imagenes/ relativa al script.

Control de movibilidad: cada imagen puede ser movible o fija.

Interacción con ratón:

Click izquierdo: arrastra y mueve imágenes movibles.

Click derecho: redimensiona imágenes movibles manteniendo proporciones.

Escalado dinámico: cada imagen mantiene su escala independiente.

Detección de colisiones: solo la imagen bajo el cursor responde a la interacción.

Límites de ventana: las imágenes no pueden salirse de los márgenes.

Edición de texto: las líneas marcadas como editables permiten escribir, borrar y agregar saltos de línea.

Cursor dinámico: muestra la posición actual dentro del texto editable.

Configuración de imágenes:

Se definen en una lista de diccionarios:

images = [

{

"surface": pygame.image.load("imagenes/imagen.png"), # Superficie de Pygame

"pos": [x, y], # Posición en pantalla

"movible": True/False, # Si se puede mover/redimensionar

"scale": 1.0 # Escala (1 = tamaño original)

}

]

Ejemplo de configuración:

images = [

{"surface": pygame.image.load("img1.png"), "pos": [50, 100], "movible": False, "scale": 0.5},

{"surface": pygame.image.load("img2.png"), "pos": [300, 200], "movible": True, "scale": 0.5},

]

Controles:

Mover imagen: Click izquierdo + arrastrar → mueve la imagen seleccionada (solo si es movible).

Redimensionar: Click derecho + arrastrar → cambia el tamaño de la imagen manteniendo proporciones.

Escribir texto: teclado → inserta texto en la línea editable.

Salir: cerrar ventana → termina la aplicación.

Estructura del código:

images: lista de diccionarios con todas las imágenes y sus propiedades.

Variables de arrastre y escalado:

dragging\_image: referencia a la imagen actualmente manipulada.

offset: compensación para un arrastre suave.

resizing: bandera que indica si se está redimensionando.

Variables de texto:

lines: lista de líneas de texto, cada una con fragmentos y bandera editable.

cursor\_row, cursor\_col: posición del cursor dentro del texto editable.

Funciones principales:

draw\_text(): renderiza todas las líneas de texto y el cursor.

Renderizado de imágenes: escala y dibuja imágenes según su propiedad scale y posición.

Manejo de eventos: detecta clicks, arrastre, redimensionado y escritura de texto.

Sistema de colisiones: solo la imagen bajo el cursor responde a interacciones.

Limitaciones:

Solo soporta formatos de imagen compatibles con Pygame (PNG, JPG, BMP, etc.).

No hay funcionalidad de guardar o exportar el estado.

No se pueden rotar las imágenes.

Sin soporte de capas o agrupación avanzada de imágenes.

Redimensionado basado en posición del ratón, no en handles visuales.

No hay historial de deshacer/rehacer.

Estructura de archivos:

proyecto/

├── editor\_imagenes.py # Archivo principal

└── imagenes/ # Carpeta de imágenes

├── img1.png

├── img2.png

└── ...

Mejoras posibles:

Handles de redimensionado visibles en las esquinas.

Rotación de imágenes mediante teclado o ratón.

Sistema de capas para organizar imágenes por profundidad.

Guardar proyecto como imagen o archivo de estado.

Herramientas adicionales: recorte, filtros, efectos, transparencia.

Panel de propiedades de imagen para modificar escala y posición.

Soporte de GIF animados u otros formatos especiales.

Deshacer/Rehacer para revertir acciones en texto o imágenes.

Dependencias:

Python 3.10+

Pygame

Instalación:

pip install pygame

Uso:

Crear una carpeta imagenes/ en el mismo directorio que el script.

Colocar las imágenes deseadas en la carpeta (img1.png, img2.png, etc.).

Ejecutar el script:

python editor\_imagenes.py

Usar click izquierdo para mover imágenes movibles.

Usar click derecho para redimensionar imágenes movibles.

Escribir en las líneas de texto editables con el teclado.
