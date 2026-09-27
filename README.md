# 🎬 Generador de Subtítulos con IA

Aplicación desarrollada en **Python + Streamlit** que permite generar automáticamente subtítulos a partir de un archivo de video utilizando **faster-whisper**.

El sistema reconoce el audio del video, genera la transcripción y permite descargar los resultados en formato **TXT** y **SRT**.

## Funciones

- Carga de videos.
- Reconocimiento automático de voz.
- Detección automática del idioma.
- Selección manual del idioma.
- Generación automática de subtítulos.
- Barra de progreso durante el procesamiento.
- Visualización de la transcripción.
- Exportación en formato TXT.
- Exportación en formato SRT.
- Procesamiento local en la computadora.

## Formatos de video

La aplicación admite:

- MP4
- MOV
- AVI
- MKV
- WEBM
- M4V

## Requisitos

Se recomienda utilizar:

- Python 3.10 o superior
- Windows 10/11
- Conexión a Internet durante la primera ejecución para descargar el modelo de reconocimiento

## Instalación

### 1. Descargar o clonar el proyecto

Descargar el repositorio desde GitHub o clonarlo mediante Git.

### 2. Abrir una terminal

Ingresar a la carpeta del proyecto:

```powershell
cd generador_subtitulos
```

### 3. Instalar las dependencias

Ejecutar:

```powershell
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` contiene las librerías necesarias:

```text
streamlit
faster-whisper
```

## Ejecutar la aplicación

Ejecutar:

```powershell
python -m streamlit run app.py
```

Streamlit abrirá automáticamente la aplicación en el navegador.

Si no se abre automáticamente, revisar la dirección local mostrada en la terminal, normalmente:

```text
http://localhost:8501
```

## Uso

1. Abrir la aplicación.
2. Seleccionar el idioma del video o utilizar la detección automática.
3. Cargar un archivo de video.
4. Presionar **Generar subtítulos**.
5. Esperar a que finalice el procesamiento.
6. Revisar la transcripción generada.
7. Descargar el archivo TXT o SRT.

## Archivo TXT

El archivo TXT contiene únicamente la transcripción:

```text
Buenos días a todos.
Hoy vamos a aprender sobre redes de computadoras.
Comenzaremos revisando algunos conceptos básicos.
```

## Archivo SRT

El archivo SRT contiene la transcripción junto con los tiempos del video:

```text
1
00:00:00,000 --> 00:00:03,500
Buenos días a todos.

2
00:00:03,500 --> 00:00:07,200
Hoy vamos a aprender sobre redes de computadoras.
```

Este archivo puede utilizarse como subtítulo en reproductores y programas de edición de video compatibles con SRT.

## Primera ejecución

Durante la primera ejecución, `faster-whisper` puede descargar automáticamente el modelo de reconocimiento de voz.

Por este motivo, la primera ejecución puede tardar más de lo habitual y requiere conexión a Internet.

Una vez descargado el modelo, podrá reutilizarse en las siguientes ejecuciones.

## Rendimiento

El tiempo necesario para generar los subtítulos depende principalmente de:

- Duración del video.
- Procesador de la computadora.
- Cantidad de audio que debe analizarse.
- Modelo de reconocimiento utilizado.

Los videos largos pueden requerir varios minutos de procesamiento.

## Estructura

```text
generador_subtitulos/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Privacidad

El procesamiento del video se realiza localmente utilizando `faster-whisper`.

Los videos cargados se utilizan temporalmente durante la generación de los subtítulos y el archivo temporal se elimina después del procesamiento.

## Uso académico

Este proyecto puede utilizarse como herramienta de apoyo para proyectos académicos de video, permitiendo generar una primera versión automática de los subtítulos que posteriormente puede ser revisada y corregida.

## Tecnologías utilizadas

- Python
- Streamlit
- faster-whisper
- Whisper

## Próximas mejoras

Entre las funcionalidades que pueden incorporarse posteriormente se encuentran:

- Edición individual de subtítulos.
- Corrección de subtítulos manteniendo los tiempos.
- Traducción automática.
- Exportación a VTT.
- Generación de subtítulos en diferentes idiomas.
- Integración de subtítulos directamente en el video.