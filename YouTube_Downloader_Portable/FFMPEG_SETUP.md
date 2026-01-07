# Configuración de FFmpeg para Calidades Altas

## ¿Qué es FFmpeg y por qué lo necesitas?

FFmpeg es una herramienta que permite combinar archivos de video y audio. YouTube almacena las calidades altas (720p, 1080p, 4K) como archivos separados de video y audio, por lo que necesitamos FFmpeg para combinarlos en un solo archivo MP4.

## Instalación de FFmpeg en Windows

### Opción 1: Descarga Directa (Recomendada)

1. **Descargar FFmpeg:**
   - Ve a: https://www.gyan.dev/ffmpeg/builds/
   - Descarga la versión "release builds" (archivo .zip)

2. **Extraer e Instalar:**
   - Extrae el archivo ZIP en `C:\ffmpeg`
   - Deberías tener la estructura: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Agregar al PATH:**
   - Presiona `Win + R`, escribe `sysdm.cpl` y presiona Enter
   - Ve a la pestaña "Avanzado" → "Variables de entorno"
   - En "Variables del sistema", busca "Path" y haz clic en "Editar"
   - Haz clic en "Nuevo" y agrega: `C:\ffmpeg\bin`
   - Haz clic en "Aceptar" en todas las ventanas

4. **Verificar la instalación:**
   - Abre una nueva ventana de PowerShell o CMD
   - Escribe: `ffmpeg -version`
   - Deberías ver información sobre la versión de FFmpeg

### Opción 2: Usando Chocolatey

Si tienes Chocolatey instalado:
```powershell
choco install ffmpeg
```

### Opción 3: Usando Winget

Si tienes Windows 10/11 con winget:
```powershell
winget install Gyan.FFmpeg
```

## ¿Qué calidades estarán disponibles?

### Sin FFmpeg:
- Solo calidades progresivas (360p, 480p máximo)
- Video y audio en un solo archivo

### Con FFmpeg:
- Todas las calidades disponibles (360p, 480p, 720p, 1080p, 1440p, 2160p/4K)
- Mejor calidad de audio
- Archivos optimizados

## Comportamiento del Descargador

1. **Con FFmpeg instalado:**
   - Descarga video y audio por separado
   - Los combina automáticamente
   - Elimina los archivos temporales
   - Resultado: archivo MP4 de alta calidad

2. **Sin FFmpeg:**
   - Si seleccionas una calidad alta, descargará solo el video (sin audio)
   - Mostrará un mensaje informativo
   - Fallback automático a calidades progresivas cuando sea posible

## Solución de Problemas

### "FFmpeg no disponible"
- Verifica que FFmpeg esté en el PATH
- Reinicia el descargador después de instalar FFmpeg
- Prueba ejecutar `ffmpeg -version` en CMD/PowerShell

### Descarga lenta
- Las calidades altas requieren más tiempo
- El proceso de combinación puede tomar unos segundos adicionales

### Error de combinación
- El descargador guardará solo el video si falla la combinación
- Puedes usar herramientas externas para agregar audio después

## Notas Importantes

- FFmpeg es completamente opcional
- El descargador funciona sin FFmpeg, pero con calidades limitadas
- La instalación de FFmpeg es un proceso único
- Una vez instalado, todas las calidades estarán disponibles automáticamente