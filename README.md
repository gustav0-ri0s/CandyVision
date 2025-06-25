
# 🎯 CandyVision: Contador de M&M's por Color con Visión Artificial

Este proyecto educativo utiliza una cámara web, OpenCV y Python para detectar y contar M&M’s en tiempo real, diferenciándolos por su color. Ideal para aprender sobre visión por computadora, procesamiento de imágenes y automatización básica.

---

## 🧪 ¿Qué hace?

✅ Detecta lentejas de M&M's por colores: rojo, naranja, amarillo, verde, azul, marrón\
✅ Muestra conteo en pantalla en tiempo real\
✅ Dibuja un marco que delimita el área válida para contar\
✅ Evita doble conteo de una misma lenteja\
✅ Al presionar `Q`, genera un reporte en imagen con los resultados

---

## 💡 Posibles usos reales

Aunque este proyecto fue desarrollado con fines educativos, puede servir como base para aplicaciones prácticas como:

1. Conteo automatizado de productos en líneas de envasado.
2. Clasificación de objetos por color en procesos industriales.
3. Sistemas de control de calidad visual.
4. Herramientas de apoyo para personas con daltonismo o discapacidad visual.
5. Conteo automatizado de medicamentos, ideal para procesos farmacéuticos más higiénicos y precisos.

---

## 💽 Requisitos

- Python 3.7 o superior
- Cámara web
- Entorno como VS Code, PyCharm, o consola

---

## 📦 Instalación

Instala las dependencias necesarias con:

```bash
pip install opencv-python numpy
```

---

## ▶️ Cómo ejecutar

1. Descarga el script `contador_mms_color.py`
2. Ejecuta:

```bash
python contador_mms_color.py
```

3. Coloca las lentejas de M&M frente a la cámara (dentro del marco blanco).
4. Presiona `Q` para guardar un reporte visual en la carpeta `reportes/`.

---

## 📸 Ejemplo de salida
<img src="https://github.com/user-attachments/assets/2f330ac7-a196-496d-ac3b-aa0b63103acc" width="400">
<img src="https://github.com/user-attachments/assets/b8f2b11f-f225-4b8f-97c6-57013524d25a" width="400">

---

## 📚 Créditos

Desarrollado con fines educativos por Gustavo Rios.\
Uso de OpenCV y Numpy.

---

## 🧠 Ideas para expandir

- Generar PDF del reporte
- Clasificación con Machine Learning
- Contador de caramelos por forma y tamaño

