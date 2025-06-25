# Contador de M&M's por color usando visión artificial
# Proyecto educativo con OpenCV y webcam

import cv2
import numpy as np
import datetime
import os

# Definir rangos HSV por color
colores = {
    "rojo": [((0, 140, 60), (10, 255, 210))],
    "naranja": [((11, 180, 120), (22, 255, 255))],
    "amarillo": [((23, 100, 100), (35, 255, 255))],
    "verde": [((40, 50, 50), (80, 255, 255))],
    "azul": [((100, 100, 100), (130, 255, 255))],
    "marron": [((0, 0, 0), (180, 255, 50))]
}

# Colores BGR para visualizar textos y rectángulos
colores_bgr = {
    "rojo": (0, 0, 255),
    "naranja": (0, 140, 255),
    "amarillo": (0, 255, 255),
    "verde": (0, 255, 0),
    "azul": (255, 0, 0),
    "marron": (30, 70, 80),
    "Total": (0, 0, 0)
}

# Inicializar cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, w = frame.shape[:2]

    # Marco de conteo ampliado (90% del área)
    x1, y1 = int(w * 0.05), int(h * 0.05)
    x2, y2 = int(w * 0.95), int(h * 0.95)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    # Crear máscaras por color
    mascaras_por_color = {}
    for color, rangos in colores.items():
        mascara = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for rango in rangos:
            mascara |= cv2.inRange(hsv, np.array(rango[0]), np.array(rango[1]))
        mascaras_por_color[color] = mascara

    # Unir máscaras y aplicar ROI
    mascara_total = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for mask in mascaras_por_color.values():
        mascara_total |= mask

    roi_mask = np.zeros_like(mascara_total)
    roi_mask[y1:y2, x1:x2] = mascara_total[y1:y2, x1:x2]

    contornos, _ = cv2.findContours(roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contador_colores = {color: 0 for color in colores}

    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area < 100:
            continue

        x, y, w_box, h_box = cv2.boundingRect(cnt)
        cx, cy = x + w_box // 2, y + h_box // 2
        pixel_hsv = hsv[cy, cx]

        color_detectado = None
        for color_name in ["naranja", "rojo", "amarillo", "verde", "azul", "marron"]:
            for (lower, upper) in colores[color_name]:
                if cv2.inRange(np.uint8([[pixel_hsv]]), np.array(lower), np.array(upper))[0][0] == 255:
                    color_detectado = color_name
                    break
            if color_detectado:
                break

        if color_detectado:
            contador_colores[color_detectado] += 1
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), colores_bgr[color_detectado], 2)
            cv2.putText(frame, color_detectado, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colores_bgr[color_detectado], 1)

    # Mostrar conteo por color
    y_text = 30
    total_general = 0
    for color, cantidad in contador_colores.items():
        cv2.putText(frame, f"{color}: {cantidad}", (10, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colores_bgr[color], 2)
        y_text += 30
        total_general += cantidad

    cv2.putText(frame, f"Total: {total_general}", (10, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.imshow("Conteo en tiempo real de M&M's", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        # Generar reporte visual al presionar Q
        ruta = "reportes"
        os.makedirs(ruta, exist_ok=True)
        frame_reporte = frame.copy()
        alto_tabla = 200
        tabla = np.ones((alto_tabla, frame.shape[1], 3), dtype=np.uint8) * 255

        x_texto = 30
        y_base = 40
        espacio = 30
        for i, (color, cantidad) in enumerate(contador_colores.items()):
            color_bgr = colores_bgr.get(color, (0, 0, 0))
            texto = f"{color}: {cantidad}"
            cv2.putText(tabla, texto, (x_texto, y_base + i * espacio),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_bgr, 2)

        cv2.putText(tabla, f"Total: {total_general}", (x_texto, y_base + len(contador_colores) * espacio + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, colores_bgr["Total"], 2)

        reporte_final = np.vstack((frame_reporte, tabla))
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = os.path.join(ruta, f"reporte_mm_{timestamp}.png")
        success = cv2.imwrite(nombre_archivo, reporte_final)

        if success:
            print(f"[✔] Reporte guardado exitosamente en:\n{os.path.abspath(nombre_archivo)}")
        else:
            print("[❌] Error: no se pudo guardar el reporte.")

        break

cap.release()
cv2.destroyAllWindows()
