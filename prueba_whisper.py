from faster_whisper import WhisperModel
from pathlib import Path

# ==========================================
# CONFIGURACIÓN
# ==========================================

VIDEO = "video.mp4"
MODELO = "small"

# ==========================================
# FUNCIONES
# ==========================================

def segundos_a_srt(segundos):
    """Convierte segundos al formato HH:MM:SS,mmm usado por SRT."""

    milisegundos_totales = round(segundos * 1000)

    horas = milisegundos_totales // 3_600_000
    resto = milisegundos_totales % 3_600_000

    minutos = resto // 60_000
    resto = resto % 60_000

    segundos = resto // 1000
    milisegundos = resto % 1000

    return f"{horas:02}:{minutos:02}:{segundos:02},{milisegundos:03}"


# ==========================================
# COMPROBAR VIDEO
# ==========================================

ruta_video = Path(VIDEO)

if not ruta_video.exists():
    print(f"ERROR: No se encontró el archivo {VIDEO}")
    print("Coloca un video llamado video.mp4 en esta carpeta.")
    exit()


# ==========================================
# CREAR CARPETA OUTPUT
# ==========================================

carpeta_output = Path("output")
carpeta_output.mkdir(exist_ok=True)

archivo_txt = carpeta_output / "transcripcion.txt"
archivo_srt = carpeta_output / "subtitulos.srt"


# ==========================================
# INICIO
# ==========================================

print("=" * 50)
print("GENERADOR DE SUBTÍTULOS - PRUEBA WHISPER")
print("=" * 50)

print("\nCargando modelo Whisper...")

model = WhisperModel(
    MODELO,
    device="cpu",
    compute_type="int8"
)

print("Modelo cargado correctamente.")


# ==========================================
# TRANSCRIPCIÓN
# ==========================================

print("\nAnalizando video...")
print("Esto puede tardar dependiendo de la duración del video.\n")

segments, info = model.transcribe(
    VIDEO,
    language="es",
    beam_size=5
)

print(f"Idioma detectado: {info.language}")
print(f"Probabilidad: {info.language_probability:.2%}")

print("\n" + "=" * 50)
print("TRANSCRIPCIÓN")
print("=" * 50)


# ==========================================
# PROCESAR SEGMENTOS
# ==========================================

segmentos = []

for segment in segments:

    texto = segment.text.strip()

    if not texto:
        continue

    segmentos.append({
        "inicio": segment.start,
        "fin": segment.end,
        "texto": texto
    })

    print(
        f"[{segment.start:.2f}s --> {segment.end:.2f}s] "
        f"{texto}"
    )


# ==========================================
# GENERAR TXT
# ==========================================

with open(archivo_txt, "w", encoding="utf-8") as archivo:

    for segmento in segmentos:
        archivo.write(segmento["texto"] + "\n")


# ==========================================
# GENERAR SRT
# ==========================================

with open(archivo_srt, "w", encoding="utf-8") as archivo:

    for numero, segmento in enumerate(segmentos, start=1):

        inicio = segundos_a_srt(segmento["inicio"])
        fin = segundos_a_srt(segmento["fin"])

        archivo.write(f"{numero}\n")
        archivo.write(f"{inicio} --> {fin}\n")
        archivo.write(f"{segmento['texto']}\n\n")


# ==========================================
# RESULTADO
# ==========================================

print("\n" + "=" * 50)
print("RESULTADO")
print("=" * 50)

print(f"Segmentos reconocidos: {len(segmentos)}")

if segmentos:

    print("\nArchivos generados correctamente:")
    print(f"TXT: {archivo_txt}")
    print(f"SRT: {archivo_srt}")

else:

    print("No se detectó voz en el video.")