#!/usr/bin/env python3
"""
Script para crear el ejecutable del YouTube Downloader
"""

import os
import subprocess
import sys
import shutil


def remove_generated_directory(name):
    """Remove only a generated directory inside this repository."""
    repository = os.path.realpath(os.getcwd())
    target = os.path.realpath(os.path.join(repository, name))
    if os.path.commonpath((repository, target)) != repository or target == repository:
        raise ValueError(f"Refusing to remove directory outside the repository: {target}")
    if os.path.isdir(target):
        shutil.rmtree(target)

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    
    print("🚀 Iniciando build del YouTube Downloader...")
    
    # Limpiar builds anteriores
    if os.path.exists("build"):
        print("🧹 Limpiando directorio build...")
        remove_generated_directory("build")
    
    if os.path.exists("dist"):
        print("🧹 Limpiando directorio dist...")
        remove_generated_directory("dist")
    
    # Comando PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin ventana de consola
        "--name=YouTube_Downloader",    # Nombre del ejecutable
        "--icon=icono1.ico",           # Icono de la aplicación
        "--add-data=img;img",          # Incluir carpeta de imágenes
        "--hidden-import=customtkinter", # Importaciones ocultas necesarias
        "--hidden-import=CTkMessagebox",
        "--hidden-import=pytubefix",
        "--hidden-import=pytubefix.extract",
        "--hidden-import=pytubefix.streams",
        "--hidden-import=pytubefix.helpers",
        "--hidden-import=pytubefix.exceptions",
        "--hidden-import=pytubefix.cipher",
        "--hidden-import=pytubefix.innertube",
        "--hidden-import=pytubefix.metadata",
        "--hidden-import=pytubefix.query",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=requests",
        "--hidden-import=urllib3",
        "--hidden-import=json",
        "--hidden-import=re",
        "--hidden-import=subprocess",
        "--collect-all=customtkinter",  # Recopilar todos los archivos de customtkinter
        "--collect-all=pytubefix",     # Incluir los scripts JS de BotGuard
        "--collect-all=nodejs_wheel",  # Incluir Node.js para el cliente WEB
        "--collect-all=imageio_ffmpeg", # Incluir FFmpeg para MP3 y video con audio
        "--noconfirm",                 # No pedir confirmación
        "download.py"                  # Archivo principal
    ]
    
    print("📦 Ejecutando PyInstaller...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completado exitosamente!")
        
        # Verificar que el ejecutable se creó
        exe_path = os.path.join("dist", "YouTube_Downloader.exe")
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"📁 Ejecutable creado: {exe_path}")
            print(f"📏 Tamaño: {file_size:.1f} MB")
            
            # Crear carpeta de distribución
            dist_folder = "YouTube_Downloader_Portable"
            if os.path.exists(dist_folder):
                remove_generated_directory(dist_folder)
            
            os.makedirs(dist_folder)
            
            # Copiar ejecutable
            shutil.copy2(exe_path, dist_folder)
            
            # Copiar archivos adicionales
            files_to_copy = [
                "FFMPEG_SETUP.md",
                "readme.md"
            ]
            
            for file in files_to_copy:
                if os.path.exists(file):
                    shutil.copy2(file, dist_folder)
            
            print(f"📦 Paquete portable creado: {dist_folder}/")
            print("\n🎉 ¡Build completado!")
            print(f"🚀 Ejecutable listo en: {dist_folder}/YouTube_Downloader.exe")
            
        else:
            print("❌ Error: No se encontró el ejecutable generado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante el build:")
        print(f"Código de salida: {e.returncode}")
        print(f"Error: {e.stderr}")
        return False
    
    return True

def main():
    """Función principal"""
    print("=" * 50)
    print("  YouTube Downloader - Build Script")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("download.py"):
        print("❌ Error: No se encontró download.py")
        print("Asegúrate de ejecutar este script desde el directorio del proyecto")
        return False
    
    # Verificar que PyInstaller está instalado
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: PyInstaller no está instalado")
        print("Ejecuta: pip install pyinstaller")
        return False
    
    # Construir ejecutable
    success = build_executable()
    
    if success:
        print("\n✨ Notas importantes:")
        print("• El ejecutable incluye todas las dependencias necesarias")
        print("• El ejecutable incluye FFmpeg para MP3 y MP4 con audio")
        print("• El ejecutable es portable - no requiere instalación")
        print("• Puedes distribuir la carpeta YouTube_Downloader_Portable completa")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
