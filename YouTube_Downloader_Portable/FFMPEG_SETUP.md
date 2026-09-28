# FFmpeg y los formatos MP3/MP4

La aplicación instala imageio-ffmpeg junto con las dependencias de Python. Sus paquetes para Windows, macOS y Linux habituales incluyen FFmpeg. El programa lo utiliza para convertir el audio descargado a un MP3 real y para unir video y audio cuando YouTube los ofrece por separado.

## Instalación desde el código

Ejecuta este comando dentro de tu entorno virtual:

    python -m pip install -r requirements.txt

No necesitas agregar ffmpeg al PATH si imageio-ffmpeg incluye el ejecutable para tu plataforma. Si el programa indica que FFmpeg no está disponible, reinstala las dependencias y comprueba el ejecutable:

    python -m pip install -U -r requirements.txt
    python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"

Si usas una plataforma sin binario incluido, instala FFmpeg desde https://ffmpeg.org/download.html y configura IMAGEIO_FFMPEG_EXE con la ruta completa. En PowerShell, por ejemplo:

    $env:IMAGEIO_FFMPEG_EXE = 'C:\ffmpeg\bin\ffmpeg.exe'
    python download.py

La aplicación informa un error si no puede convertir o unir los archivos. No renombra audio de otro formato como .mp3 ni guarda un MP4 sin sonido como si la operación hubiera terminado correctamente.