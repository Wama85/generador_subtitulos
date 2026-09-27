import streamlit as st
from faster_whisper import WhisperModel
from pathlib import Path
import tempfile
import os


# ==========================================================
# CONFIGURACIÓN DE STREAMLIT
# ==========================================================

st.set_page_config(
    page_title="Generador de Subtítulos",
    page_icon="🎬",
    layout="wide"
)


# ==========================================================
# FUNCIONES
# ==========================================================

def segundos_a_srt(segundos):
    """Convierte segundos al formato HH:MM:SS,mmm."""

    milisegundos_totales = round(segundos * 1000)

    horas = milisegundos_totales // 3_600_000
    resto = milisegundos_totales % 3_600_000

    minutos = resto // 60_000
    resto %= 60_000

    segundos = resto // 1000
    milisegundos = resto % 1000

    return f"{horas:02}:{minutos:02}:{segundos:02},{milisegundos:03}"


def segundos_a_tiempo(segundos):
    """Convierte segundos a HH:MM:SS."""

    segundos = int(segundos)

    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    return f"{horas:02}:{minutos:02}:{segundos:02}"


def generar_txt(segmentos):
    """Genera el contenido TXT."""

    return "\n".join(
        segmento["texto"]
        for segmento in segmentos
    )


def generar_srt(segmentos):
    """Genera el contenido SRT."""

    contenido = []

    for numero, segmento in enumerate(segmentos, start=1):

        inicio = segundos_a_srt(segmento["inicio"])
        fin = segundos_a_srt(segmento["fin"])

        contenido.append(str(numero))
        contenido.append(f"{inicio} --> {fin}")
        contenido.append(segmento["texto"])
        contenido.append("")

    return "\n".join(contenido)


@st.cache_resource
def cargar_modelo():
    """Carga Whisper una sola vez."""

    return WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )


# ==========================================================
# ENCABEZADO
# ==========================================================

st.title("🎬 Generador de Subtítulos")

st.write(
    "Convierte automáticamente el audio de un video "
    "en subtítulos utilizando reconocimiento de voz."
)

st.divider()


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    idioma = st.selectbox(
        "Idioma del video",
        [
            "Detectar automáticamente",
            "Español",
            "Inglés",
            "Italiano",
            "Portugués",
            "Francés",
            "Alemán"
        ]
    )

with col2:

    st.info(
        "El sistema generará automáticamente "
        "una transcripción TXT y un archivo SRT."
    )


# ==========================================================
# MAPA DE IDIOMAS
# ==========================================================

idiomas = {
    "Detectar automáticamente": None,
    "Español": "es",
    "Inglés": "en",
    "Italiano": "it",
    "Portugués": "pt",
    "Francés": "fr",
    "Alemán": "de"
}


# ==========================================================
# SUBIR VIDEO
# ==========================================================

archivo_video = st.file_uploader(
    "Selecciona un video",
    type=[
        "mp4",
        "mov",
        "avi",
        "mkv",
        "webm",
        "m4v"
    ]
)


# ==========================================================
# VIDEO CARGADO
# ==========================================================

if archivo_video is not None:

    st.success(f"Video cargado: {archivo_video.name}")

    st.video(archivo_video)

    st.divider()

    if st.button(
            "🎙️ Generar subtítulos",
            type="primary",
            use_container_width=True
    ):

        extension = Path(archivo_video.name).suffix
        ruta_temporal = None

        try:

            # ==================================================
            # GUARDAR VIDEO TEMPORAL
            # ==================================================

            with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=extension
            ) as temporal:

                temporal.write(archivo_video.getbuffer())
                ruta_temporal = temporal.name


            # ==================================================
            # CARGAR WHISPER
            # ==================================================

            estado_modelo = st.empty()
            estado_modelo.info(
                "Cargando modelo de reconocimiento..."
            )

            modelo = cargar_modelo()

            estado_modelo.success(
                "Modelo cargado correctamente."
            )


            # ==================================================
            # PREPARAR TRANSCRIPCIÓN
            # ==================================================

            st.subheader("Procesamiento")

            barra_progreso = st.progress(0)

            texto_porcentaje = st.empty()
            texto_tiempo = st.empty()
            texto_segmento = st.empty()

            texto_porcentaje.write(
                "**Progreso: 0%**"
            )

            texto_tiempo.write(
                "Preparando análisis del video..."
            )

            texto_segmento.info(
                "Esperando los primeros segmentos..."
            )


            # ==================================================
            # TRANSCRIBIR
            # ==================================================

            segments, info = modelo.transcribe(
                ruta_temporal,
                language=idiomas[idioma],
                beam_size=5
            )

            # Duración total detectada por Whisper
            duracion_total = info.duration

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

                # ==============================================
                # CALCULAR PROGRESO
                # ==============================================

                if duracion_total > 0:

                    porcentaje = int(
                        (segment.end / duracion_total) * 100
                    )

                    porcentaje = min(
                        max(porcentaje, 0),
                        99
                    )

                else:

                    porcentaje = 0


                # ==============================================
                # ACTUALIZAR INTERFAZ
                # ==============================================

                barra_progreso.progress(porcentaje)

                texto_porcentaje.write(
                    f"**Progreso: {porcentaje}%**"
                )

                tiempo_actual = segundos_a_tiempo(
                    segment.end
                )

                tiempo_total = segundos_a_tiempo(
                    duracion_total
                )

                texto_tiempo.write(
                    f"Procesado: **{tiempo_actual}** "
                    f"/ **{tiempo_total}**"
                )

                texto_segmento.info(
                    f"🎙️ {texto}"
                )


            # ==================================================
            # FINALIZAR BARRA
            # ==================================================

            barra_progreso.progress(100)

            texto_porcentaje.write(
                "**Progreso: 100%**"
            )

            texto_tiempo.write(
                f"Procesado: **"
                f"{segundos_a_tiempo(duracion_total)}"
                f" / "
                f"{segundos_a_tiempo(duracion_total)}"
                f"**"
            )

            texto_segmento.success(
                "Procesamiento completado."
            )


            # ==================================================
            # RESULTADOS
            # ==================================================

            if segmentos:

                txt = generar_txt(segmentos)
                srt = generar_srt(segmentos)

                st.session_state["txt"] = txt
                st.session_state["srt"] = srt
                st.session_state["segmentos"] = segmentos

                st.session_state["nombre_video"] = Path(
                    archivo_video.name
                ).stem

                st.session_state["idioma_detectado"] = (
                    info.language
                )

                st.session_state["probabilidad"] = (
                    info.language_probability
                )

                st.success(
                    "Subtítulos generados correctamente."
                )

            else:

                st.warning(
                    "No se detectó voz en el video."
                )


        except Exception as error:

            st.error(
                f"Ocurrió un error durante el procesamiento:\n\n"
                f"{error}"
            )


        finally:

            # ==================================================
            # ELIMINAR VIDEO TEMPORAL
            # ==================================================

            if ruta_temporal and os.path.exists(
                    ruta_temporal
            ):

                try:
                    os.remove(ruta_temporal)

                except PermissionError:
                    pass


# ==========================================================
# MOSTRAR RESULTADOS
# ==========================================================

if "segmentos" in st.session_state:

    st.divider()

    st.subheader("Resultado de la transcripción")

    idioma_detectado = st.session_state.get(
        "idioma_detectado",
        "-"
    )

    probabilidad = st.session_state.get(
        "probabilidad",
        0
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Idioma detectado",
            idioma_detectado.upper()
        )

    with col2:

        st.metric(
            "Coincidencia",
            f"{probabilidad:.2%}"
        )

    with col3:

        st.metric(
            "Segmentos",
            len(st.session_state["segmentos"])
        )


    # ======================================================
    # TRANSCRIPCIÓN
    # ======================================================

    st.subheader("📝 Transcripción")

    texto_editado = st.text_area(
        "Texto reconocido",
        value=st.session_state["txt"],
        height=400
    )


    # ======================================================
    # DESCARGAS
    # ======================================================

    st.subheader("Descargar archivos")

    nombre = st.session_state.get(
        "nombre_video",
        "subtitulos"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📄 Descargar TXT",
            data=st.session_state["txt"],
            file_name=f"{nombre}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        st.download_button(
            label="🎬 Descargar SRT",
            data=st.session_state["srt"],
            file_name=f"{nombre}.srt",
            mime="text/plain",
            use_container_width=True
        )