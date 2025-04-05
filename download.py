import tkinter
import tkinter.filedialog
import customtkinter as ctk
import threading
import os
from pytubefix import YouTube, Search
import urllib.error
import re
from CTkMessagebox import CTkMessagebox # Para mostrar errores/info de forma más elegante

# --- Language Support System ---
# Languages: English, Spanish, German, French
LANGUAGES = {
    "en": "English",
    "es": "Español",
    "de": "Deutsch",
    "fr": "Français"
}

# Translation dictionaries
TRANSLATIONS = {
    # English translations
    "en": {
        # Window title
        "app_title": "YouTube Downloader (MP3/MP4) - Pytubefix",
        # Main elements
        "title": "YouTube Downloader",
        "mode": "Mode:",
        "mode_url": "Single URL",
        "mode_batch": "Batch Search",
        "url_label": "Paste the video URL:",
        "batch_label": "Paste the names (one per line):",
        "folder_label": "Save to:",
        "browse_button": "Select",
        "format_label": "Select the format:",
        "audio_option": "Audio (MP3)",
        "video_option": "Video (MP4)",
        "quality_label": "Quality (Video):",
        "download_button": "Download",
        # Status messages
        "status_paste_url": "Paste a YouTube URL",
        "status_paste_names": "Paste names to search (one per line)",
        "status_invalid_url": "Invalid or incomplete URL",
        "status_checking_url": "Checking URL and qualities...",
        "status_no_mp4": "No MP4 (progressive) videos found for {title}...",
        "status_no_qualities": "No valid qualities found for {title}...",
        "status_network_error": "Network error when checking URL.",
        "status_unavailable": "Video unavailable or restricted.",
        "status_streaming_error": "Could not process video information (streamingData).",
        "status_verify_error": "Error checking URL: {error}",
        "status_video_prefix": "Video: {title}...",
        "status_error_no_url": "Error: No URL to download.",
        "status_quality_error": "Error: Unrecognized video quality.",
        "status_quality_unavailable": "Error: Quality {quality} unavailable.",
        "status_select_quality": "Error: Select a video quality.",
        "status_starting_download": "Starting download...",
        "status_no_search_terms": "Error: No search terms in the list.",
        "status_batch_start": "Starting batch downloads ({count} items)...",
        "status_batch_searching": "Batch ({current}/{total}): Searching '{term}'...",
        "status_batch_not_found": "Batch ({current}/{total}): No result found for '{term}'...",
        "status_batch_no_mp4": "Batch ({current}/{total}): No progressive MP4 for '{title}'...",
        "status_error_no_audio": "{prefix}Error: No audio stream found.",
        "status_quality_not_found": "{prefix}Error: Quality {quality} not found. Trying highest.",
        "status_no_mp4_stream": "{prefix}Error: No progressive MP4 video stream found.",
        "status_internal_error": "{prefix}Internal error: Video quality not specified.",
        "status_file_exists": "{prefix}Already exists: {filename}",
        "status_downloading": "{prefix}Downloading {type}: {title}...",
        "status_download_renamed": "{prefix}Downloaded! Saved as {filename} (couldn't rename)",
        "status_success": "{prefix}Success! Saved as: {filename}",
        "status_download_error": "{prefix}Error ({error_type}) downloading: {error}",
        "status_unexpected_error": "Unexpected error starting download: {error}",
        "batch_complete": "Batch completed: {success} success(es), {fail} failure(s).",
        "downloading": "Downloading...",
        "progress": "Progress...",
        # Error messages
        "error_invalid_folder": "The selected destination folder is invalid.",
        "error_invalid_folder_title": "Error",
        # Language selector
        "language_label": "Language:",
        # Folder error
        "folder_error_title": "Error",
        "folder_error_message": "The selected destination folder is invalid."
    },
    # Spanish translations
    "es": {
        # Window title
        "app_title": "Descargador YouTube (MP3/MP4) - Pytubefix",
        # Main elements
        "title": "Descargador YouTube",
        "mode": "Modo:",
        "mode_url": "URL Única",
        "mode_batch": "Búsqueda por Lote",
        "url_label": "Pega la URL del video:",
        "batch_label": "Pega los nombres (uno por línea):",
        "folder_label": "Guardar en:",
        "browse_button": "Seleccionar",
        "format_label": "Selecciona el formato:",
        "audio_option": "Audio (MP3)",
        "video_option": "Video (MP4)",
        "quality_label": "Calidad (Video):",
        "download_button": "Descargar",
        # Status messages
        "status_paste_url": "Pega una URL de YouTube",
        "status_paste_names": "Pega nombres para buscar (uno por línea)",
        "status_invalid_url": "URL inválida o incompleta",
        "status_checking_url": "Verificando URL y calidades...",
        "status_no_mp4": "No se encontraron videos MP4 (progresivos) para {title}...",
        "status_no_qualities": "No se encontraron calidades válidas para {title}...",
        "status_network_error": "Error de red al verificar URL.",
        "status_unavailable": "Video no disponible o restringido.",
        "status_streaming_error": "No se pudo procesar la información del video (streamingData).",
        "status_verify_error": "Error al verificar URL: {error}",
        "status_video_prefix": "Video: {title}...",
        "status_error_no_url": "Error: No hay URL para descargar.",
        "status_quality_error": "Error: Calidad de video no reconocida.",
        "status_quality_unavailable": "Error: Calidad {quality} no disponible.",
        "status_select_quality": "Error: Selecciona una calidad de video.",
        "status_starting_download": "Iniciando descarga...",
        "status_no_search_terms": "Error: No hay términos de búsqueda en la lista.",
        "status_batch_start": "Iniciando descargas por lote ({count} items)...",
        "status_batch_searching": "Lote ({current}/{total}): Buscando '{term}'...",
        "status_batch_not_found": "Lote ({current}/{total}): No se encontró resultado para '{term}'...",
        "status_batch_no_mp4": "Lote ({current}/{total}): No hay MP4 progresivo para '{title}'...",
        "status_error_no_audio": "{prefix}Error: No se encontró stream de audio.",
        "status_quality_not_found": "{prefix}Error: Calidad {quality} no encontrada. Intentando la más alta.",
        "status_no_mp4_stream": "{prefix}Error: No se encontró ningún stream de video MP4 progresivo.",
        "status_internal_error": "{prefix}Error interno: Calidad de video no especificada.",
        "status_file_exists": "{prefix}Ya existe: {filename}",
        "status_downloading": "{prefix}Descargando {type}: {title}...",
        "status_download_renamed": "{prefix}¡Descargado! Guardado como {filename} (no se pudo renombrar)",
        "status_success": "{prefix}¡Éxito! Guardado como: {filename}",
        "status_download_error": "{prefix}Error ({error_type}) descargando: {error}",
        "status_unexpected_error": "Error inesperado iniciando descarga: {error}",
        "batch_complete": "Lote completado: {success} éxito(s), {fail} fallo(s).",
        "downloading": "Descargando...",
        "progress": "Progreso...",
        # Error messages
        "error_invalid_folder": "La carpeta de destino seleccionada no es válida.",
        "error_invalid_folder_title": "Error",
        # Language selector
        "language_label": "Idioma:",
        # Folder error
        "folder_error_title": "Error",
        "folder_error_message": "La carpeta de destino seleccionada no es válida."
    },
    # German translations
    "de": {
        # Window title
        "app_title": "YouTube Downloader (MP3/MP4) - Pytubefix",
        # Main elements
        "title": "YouTube Downloader",
        "mode": "Modus:",
        "mode_url": "Einzel-URL",
        "mode_batch": "Batch-Suche",
        "url_label": "Video-URL einfügen:",
        "batch_label": "Namen einfügen (einer pro Zeile):",
        "folder_label": "Speichern unter:",
        "browse_button": "Auswählen",
        "format_label": "Format auswählen:",
        "audio_option": "Audio (MP3)",
        "video_option": "Video (MP4)",
        "quality_label": "Qualität (Video):",
        "download_button": "Herunterladen",
        # Status messages
        "status_paste_url": "Fügen Sie eine YouTube-URL ein",
        "status_paste_names": "Fügen Sie Namen zum Suchen ein (einen pro Zeile)",
        "status_invalid_url": "Ungültige oder unvollständige URL",
        "status_checking_url": "Überprüfe URL und Qualitäten...",
        "status_no_mp4": "Keine MP4-Videos (progressiv) gefunden für {title}...",
        "status_no_qualities": "Keine gültigen Qualitäten gefunden für {title}...",
        "status_network_error": "Netzwerkfehler beim Überprüfen der URL.",
        "status_unavailable": "Video nicht verfügbar oder eingeschränkt.",
        "status_streaming_error": "Videoinformationen konnten nicht verarbeitet werden (streamingData).",
        "status_verify_error": "Fehler beim Überprüfen der URL: {error}",
        "status_video_prefix": "Video: {title}...",
        "status_error_no_url": "Fehler: Keine URL zum Herunterladen.",
        "status_quality_error": "Fehler: Videoqualität nicht erkannt.",
        "status_quality_unavailable": "Fehler: Qualität {quality} nicht verfügbar.",
        "status_select_quality": "Fehler: Wählen Sie eine Videoqualität.",
        "status_starting_download": "Starte Download...",
        "status_no_search_terms": "Fehler: Keine Suchbegriffe in der Liste.",
        "status_batch_start": "Starte Batch-Downloads ({count} Elemente)...",
        "status_batch_searching": "Batch ({current}/{total}): Suche '{term}'...",
        "status_batch_not_found": "Batch ({current}/{total}): Kein Ergebnis gefunden für '{term}'...",
        "status_batch_no_mp4": "Batch ({current}/{total}): Kein progressives MP4 für '{title}'...",
        "status_error_no_audio": "{prefix}Fehler: Kein Audio-Stream gefunden.",
        "status_quality_not_found": "{prefix}Fehler: Qualität {quality} nicht gefunden. Versuche höchste.",
        "status_no_mp4_stream": "{prefix}Fehler: Kein progressiver MP4-Videostream gefunden.",
        "status_internal_error": "{prefix}Interner Fehler: Videoqualität nicht angegeben.",
        "status_file_exists": "{prefix}Existiert bereits: {filename}",
        "status_downloading": "{prefix}Herunterladen {type}: {title}...",
        "status_download_renamed": "{prefix}Heruntergeladen! Gespeichert als {filename} (konnte nicht umbenannt werden)",
        "status_success": "{prefix}Erfolg! Gespeichert als: {filename}",
        "status_download_error": "{prefix}Fehler ({error_type}) beim Herunterladen: {error}",
        "status_unexpected_error": "Unerwarteter Fehler beim Starten des Downloads: {error}",
        "batch_complete": "Batch abgeschlossen: {success} Erfolg(e), {fail} Fehler.",
        "downloading": "Herunterladen...",
        "progress": "Fortschritt...",
        # Error messages
        "error_invalid_folder": "Der ausgewählte Zielordner ist ungültig.",
        "error_invalid_folder_title": "Fehler",
        # Language selector
        "language_label": "Sprache:",
        # Folder error
        "folder_error_title": "Fehler",
        "folder_error_message": "Der ausgewählte Zielordner ist ungültig."
    },
    # French translations
    "fr": {
        # Window title
        "app_title": "Téléchargeur YouTube (MP3/MP4) - Pytubefix",
        # Main elements
        "title": "Téléchargeur YouTube",
        "mode": "Mode:",
        "mode_url": "URL Unique",
        "mode_batch": "Recherche par Lot",
        "url_label": "Collez l'URL de la vidéo:",
        "batch_label": "Collez les noms (un par ligne):",
        "folder_label": "Enregistrer dans:",
        "browse_button": "Sélectionner",
        "format_label": "Sélectionnez le format:",
        "audio_option": "Audio (MP3)",
        "video_option": "Vidéo (MP4)",
        "quality_label": "Qualité (Vidéo):",
        "download_button": "Télécharger",
        # Status messages
        "status_paste_url": "Collez une URL YouTube",
        "status_paste_names": "Collez les noms à rechercher (un par ligne)",
        "status_invalid_url": "URL invalide ou incomplète",
        "status_checking_url": "Vérification de l'URL et des qualités...",
        "status_no_mp4": "Aucune vidéo MP4 (progressive) trouvée pour {title}...",
        "status_no_qualities": "Aucune qualité valide trouvée pour {title}...",
        "status_network_error": "Erreur réseau lors de la vérification de l'URL.",
        "status_unavailable": "Vidéo indisponible ou restreinte.",
        "status_streaming_error": "Impossible de traiter les informations vidéo (streamingData).",
        "status_verify_error": "Erreur lors de la vérification de l'URL: {error}",
        "status_video_prefix": "Vidéo: {title}...",
        "status_error_no_url": "Erreur: Pas d'URL à télécharger.",
        "status_quality_error": "Erreur: Qualité vidéo non reconnue.",
        "status_quality_unavailable": "Erreur: Qualité {quality} non disponible.",
        "status_select_quality": "Erreur: Sélectionnez une qualité vidéo.",
        "status_starting_download": "Démarrage du téléchargement...",
        "status_no_search_terms": "Erreur: Pas de termes de recherche dans la liste.",
        "status_batch_start": "Démarrage des téléchargements par lot ({count} éléments)...",
        "status_batch_searching": "Lot ({current}/{total}): Recherche '{term}'...",
        "status_batch_not_found": "Lot ({current}/{total}): Aucun résultat trouvé pour '{term}'...",
        "status_batch_no_mp4": "Lot ({current}/{total}): Pas de MP4 progressif pour '{title}'...",
        "status_error_no_audio": "{prefix}Erreur: Aucun flux audio trouvé.",
        "status_quality_not_found": "{prefix}Erreur: Qualité {quality} non trouvée. Essai de la plus haute.",
        "status_no_mp4_stream": "{prefix}Erreur: Aucun flux vidéo MP4 progressif trouvé.",
        "status_internal_error": "{prefix}Erreur interne: Qualité vidéo non spécifiée.",
        "status_file_exists": "{prefix}Existe déjà: {filename}",
        "status_downloading": "{prefix}Téléchargement {type}: {title}...",
        "status_download_renamed": "{prefix}Téléchargé! Enregistré sous {filename} (impossible de renommer)",
        "status_success": "{prefix}Succès! Enregistré sous: {filename}",
        "status_download_error": "{prefix}Erreur ({error_type}) lors du téléchargement: {error}",
        "status_unexpected_error": "Erreur inattendue lors du démarrage du téléchargement: {error}",
        "batch_complete": "Lot terminé: {success} succès, {fail} échec(s).",
        "downloading": "Téléchargement...",
        "progress": "Progression...",
        # Error messages
        "error_invalid_folder": "Le dossier de destination sélectionné n'est pas valide.",
        "error_invalid_folder_title": "Erreur",
        # Language selector
        "language_label": "Langue:",
        # Folder error
        "folder_error_title": "Erreur",
        "folder_error_message": "Le dossier de destination sélectionné n'est pas valide."
    }
}

# --- Set Default Language ---
DEFAULT_LANGUAGE = "en"

# --- Configuración de la Apariencia ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("YouTube Downloader (MP3/MP4) - Pytubefix")  # Default title, will be updated with language
        self.geometry("600x720")  # Increased height for language selector
        self.resizable(False, False)

        # --- Variables ---
        self.save_path = ctk.StringVar(value=os.getcwd())
        self.download_type = ctk.StringVar(value="audio") # Llama a _on_format_change al cambiar
        self.selected_quality = ctk.StringVar(value="") # Variable para la calidad seleccionada
        self.available_video_streams = {} # Diccionario para mapear "resolución" -> stream object
        self.mode = ctk.StringVar(value="url")
        self._check_url_debouncer = None
        self._is_downloading = False
        
        # --- Language Support ---
        self.language = ctk.StringVar(value=DEFAULT_LANGUAGE)
        self.language.trace_add("write", self._on_language_change)
        self.texts = {}  # Will hold the current language's texts

        # --- Widgets ---
        self._load_language(self.language.get())  # Load initial language
        self.create_widgets()
        self._on_mode_change() # Set initial UI state based on default mode
        self._update_quality_widgets_state() # Estado inicial de los widgets de calidad

    def _load_language(self, lang_code):
        """Loads the translations for the specified language code."""
        if lang_code in TRANSLATIONS:
            self.texts = TRANSLATIONS[lang_code]
        else:
            # Fallback to default language
            self.texts = TRANSLATIONS[DEFAULT_LANGUAGE]

    def _on_language_change(self, *args):
        """Updates the UI when language is changed."""
        self._load_language(self.language.get())
        self._update_ui_texts()

    def _update_ui_texts(self):
        """Updates all UI text elements to match the current language."""
        # Update window title
        self.title(self.texts["app_title"])
        
        # Update main widgets text
        self.title_label.configure(text=self.texts["title"])
        self.mode_label.configure(text=self.texts["mode"])
        self.radio_mode_url.configure(text=self.texts["mode_url"])
        self.radio_mode_batch.configure(text=self.texts["mode_batch"])
        self.url_label.configure(text=self.texts["url_label"])
        self.batch_label.configure(text=self.texts["batch_label"])
        self.folder_label.configure(text=self.texts["folder_label"])
        self.browse_button.configure(text=self.texts["browse_button"])
        self.format_label.configure(text=self.texts["format_label"])
        self.radio_audio.configure(text=self.texts["audio_option"])
        self.radio_video.configure(text=self.texts["video_option"])
        self.quality_label.configure(text=self.texts["quality_label"])
        self.download_button.configure(text=self.texts["download_button"])
        self.language_label.configure(text=self.texts["language_label"])
        
        # Update status based on current state
        self._on_mode_change()  # This will update the status label text

    def create_widgets(self):
        # --- Marco Principal ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- Título ---
        self.title_label = ctk.CTkLabel(main_frame, text=self.texts["title"], font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(10, 15))

        # --- Language Selector ---
        language_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        language_frame.pack(pady=(0, 10))

        self.language_label = ctk.CTkLabel(language_frame, text=self.texts["language_label"])
        self.language_label.pack(side="left", padx=(0, 10))

        # Create a list of language names for display
        language_names = [LANGUAGES[code] for code in LANGUAGES.keys()]
        language_codes = list(LANGUAGES.keys())
        
        self.language_selector = ctk.CTkComboBox(
            language_frame,
            values=language_names,
            command=lambda choice: self.language.set(language_codes[language_names.index(choice)])
        )
        # Set initial selection to match current language
        current_language_name = LANGUAGES[self.language.get()]
        self.language_selector.set(current_language_name)
        self.language_selector.pack(side="left", padx=10)

        # --- Mode Selector ---
        mode_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mode_frame.pack(pady=(0, 10))

        self.mode_label = ctk.CTkLabel(mode_frame, text=self.texts["mode"])
        self.mode_label.pack(side="left", padx=(0, 10))

        self.radio_mode_url = ctk.CTkRadioButton(mode_frame, text=self.texts["mode_url"], variable=self.mode, value="url", command=self._on_mode_change)
        self.radio_mode_url.pack(side="left", padx=10)

        self.radio_mode_batch = ctk.CTkRadioButton(mode_frame, text=self.texts["mode_batch"], variable=self.mode, value="batch", command=self._on_mode_change)
        self.radio_mode_batch.pack(side="left", padx=10)

        # --- Frame for URL input (conditionally shown) ---
        self.url_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.url_frame.pack(fill="x", padx=50, pady=(0, 10)) # Packed here, visibility controlled later

        self.url_label = ctk.CTkLabel(self.url_frame, text=self.texts["url_label"])
        self.url_label.pack(pady=(10, 5))

        # MODIFIED: Bind KeyRelease for automatic verification
        self.url_entry = ctk.CTkEntry(self.url_frame, width=350, placeholder_text="https://www.youtube.com/watch?v=...")
        self.url_entry.pack(side="left", expand=True, fill="x", pady=(0,10), padx=(0,0)) # Removed right padx
        self.url_entry.bind("<KeyRelease>", self._schedule_url_check)

        # --- NEW: Frame for Batch input (conditionally shown) ---
        self.batch_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        # Packed later in _on_mode_change

        self.batch_label = ctk.CTkLabel(self.batch_frame, text=self.texts["batch_label"])
        self.batch_label.pack(pady=(10, 5))

        self.batch_textbox = ctk.CTkTextbox(self.batch_frame, height=100, width=350) # Added width
        self.batch_textbox.pack(pady=(0,10), fill="x")

        # --- Selección de Carpeta ---
        self.folder_label = ctk.CTkLabel(main_frame, text=self.texts["folder_label"])
        self.folder_label.pack(pady=(10, 5))

        folder_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        folder_frame.pack(pady=(0, 10), fill="x", padx=50)

        self.folder_entry = ctk.CTkEntry(folder_frame, textvariable=self.save_path, state="readonly", width=300)
        self.folder_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.browse_button = ctk.CTkButton(folder_frame, text=self.texts["browse_button"], command=self.select_folder, width=80) # Ancho ajustado
        self.browse_button.pack(side="left")

        # --- Selector de Formato ---
        self.format_label = ctk.CTkLabel(main_frame, text=self.texts["format_label"])
        self.format_label.pack(pady=(15, 5))

        format_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        format_frame.pack(pady=(0, 5)) # Menos padding inferior

        self.radio_audio = ctk.CTkRadioButton(format_frame, text=self.texts["audio_option"], variable=self.download_type, value="audio", command=self._on_format_change)
        self.radio_audio.pack(side="left", padx=10)

        self.radio_video = ctk.CTkRadioButton(format_frame, text=self.texts["video_option"], variable=self.download_type, value="video", command=self._on_format_change)
        self.radio_video.pack(side="left", padx=10)

        # --- Selector de Calidad de Video (NUEVO) ---
        self.quality_frame = ctk.CTkFrame(main_frame, fg_color="transparent") # Frame para agrupar calidad
        self.quality_frame.pack(pady=(5, 10), fill="x", padx=50)

        self.quality_label = ctk.CTkLabel(self.quality_frame, text=self.texts["quality_label"])
        self.quality_label.pack(side="left", padx=(0, 10))

        self.quality_combobox = ctk.CTkComboBox(
            self.quality_frame,
            variable=self.selected_quality,
            values=[""], # Inicialmente vacío o con placeholder
            state="disabled", # Empieza deshabilitado
            width=150
        )
        self.quality_combobox.pack(side="left", expand=True, fill="x")

        # --- Botón de Descarga ---
        self.download_button = ctk.CTkButton(main_frame, text=self.texts["download_button"], command=self.start_download_dispatcher, height=40, font=ctk.CTkFont(size=14, weight="bold"), state="disabled")
        self.download_button.pack(pady=20)

        # --- Barra de Progreso ---
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(5, 5))
        self.progress_label = ctk.CTkLabel(main_frame, text="0%")
        self.progress_label.pack(pady=(0, 10))

        # --- Etiqueta de Estado ---
        self.status_label = ctk.CTkLabel(main_frame, text="", text_color="gray")
        self.status_label.pack(pady=(10, 10))

    # --- Mode Switching Logic ---
    def _on_mode_change(self):
        """Handles switching between URL and Batch modes."""
        current_mode = self.mode.get()
        # Cancel any pending URL checks
        if self._check_url_debouncer:
            self.after_cancel(self._check_url_debouncer)
            self._check_url_debouncer = None

        if current_mode == "url":
            self.batch_frame.pack_forget()  # Hide batch frame
            self.url_frame.pack(fill="x", padx=50, pady=(0, 10))  # Show URL frame
            self.status_label.configure(text=self.texts["status_paste_url"], text_color="gray")
            # Enable/disable download based on if URL was previously verified
            self.download_button.configure(state="normal" if self.available_video_streams else "disabled")
            self._update_quality_widgets_state()  # Update quality state based on current format
        elif current_mode == "batch":
            self.url_frame.pack_forget()  # Hide URL frame
            self.batch_frame.pack(fill="x", padx=50, pady=(0, 10))  # Show batch frame
            self.status_label.configure(text=self.texts["status_paste_names"], text_color="gray")
            self.download_button.configure(state="normal")  # Enable download for batch mode
            # Disable quality selection for batch mode
            self.quality_label.configure(state="disabled")
            self.quality_combobox.configure(state="disabled")
            self.available_video_streams = {}  # Clear stream info
            self.selected_quality.set("")
            self.quality_combobox.configure(values=[""])

        # Reset progress
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        # Ensure widgets are enabled if not downloading
        if not self._is_downloading:
            self.enable_widgets()

    # --- Debounced URL Checker ---
    def _schedule_url_check(self, event=None):
        """Schedules the URL quality check after a brief pause."""
        if self.mode.get() != "url": return  # Only check in URL mode

        # Cancel the previous scheduled check if it exists
        if self._check_url_debouncer:
            self.after_cancel(self._check_url_debouncer)

        # Schedule the check after 750ms
        self._check_url_debouncer = self.after(750, self.start_fetch_qualities_thread)

    # --- Format Change Handler ---
    def _on_format_change(self):
        """Called when switching between Audio and Video."""
        self._update_quality_widgets_state()
        # If we change to audio, clear quality selection
        if self.download_type.get() == "audio":
            self.selected_quality.set("")
            self.quality_combobox.configure(values=[""])
            self.available_video_streams = {}

    def _update_quality_widgets_state(self):
        """Enables/disables quality widgets based on format AND mode."""
        is_video = self.download_type.get() == "video"
        is_url_mode = self.mode.get() == "url"
        # Enable quality only if URL mode, Video format, and streams are loaded
        new_state = "normal" if is_url_mode and is_video and self.available_video_streams else "disabled"
        self.quality_label.configure(state=new_state)
        self.quality_combobox.configure(state=new_state)

    def start_fetch_qualities_thread(self):
        """Starts fetching qualities in a separate thread (for URL mode)."""
        # Ensure this is only called in URL mode
        if self.mode.get() != "url":
            print("Attempted to fetch qualities outside URL mode.")
            return

        url = self.url_entry.get().strip()
        if not url or not url.startswith(("https://www.youtube.com/", "https://youtu.be/")):
            # Don't show popup for invalid URL during typing, just update status
            self.status_label.configure(text=self.texts["status_invalid_url"], text_color="red")
            self.download_button.configure(state="disabled")
            self.quality_combobox.configure(values=[""], state="disabled")
            self.selected_quality.set("")
            self.available_video_streams = {}
            self._update_quality_widgets_state()
            return

        # UI update: indicate checking is happening
        self.status_label.configure(text=self.texts["status_checking_url"], text_color="orange")
        # Disable download button while checking
        self.download_button.configure(state="disabled")
        self.quality_combobox.configure(values=[""], state="disabled")
        self.selected_quality.set("")
        self.available_video_streams = {}
        self._update_quality_widgets_state()  # Ensure quality is disabled during check

        fetch_thread = threading.Thread(target=self._fetch_qualities_task, args=(url,), daemon=True)
        fetch_thread.start()

    def _fetch_qualities_task(self, url):
        """Task that runs in thread to get qualities."""
        try:
            yt = YouTube(url)
            # Prioritize progressive (video+audio) MP4 streams
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

            if not streams:
                # Try adaptive if progressive fails? For now, fail
                message = self.texts["status_no_mp4"].format(title=yt.title[:30])
                self.after(0, self._update_ui_after_fetch, None, message, None, url)
                return

            stream_map = {}
            quality_options = []
            # Store stream object with formatted display string
            stream_map_display = {}
            for s in streams:
                if s.resolution not in stream_map:  # Avoid duplicate resolutions
                    display_text = f"{s.resolution} ({s.filesize_mb:.1f} MB)"
                    stream_map[s.resolution] = s  # Map resolution ('720p') to stream
                    stream_map_display[display_text] = s  # Map display text to stream
                    quality_options.append(display_text)  # List for combobox

            if not quality_options:
                message = self.texts["status_no_qualities"].format(title=yt.title[:30])
                self.after(0, self._update_ui_after_fetch, None, message, None, url)
                return

            # Pass the original URL along to check if it changed while fetching
            video_prefix = self.texts["status_video_prefix"].format(title=yt.title[:40])
            self.after(0, self._update_ui_after_fetch, stream_map, video_prefix, quality_options, url)

        except urllib.error.URLError as e:
            self.after(0, self._update_ui_after_fetch, None, self.texts["status_network_error"], None, url)
        except Exception as e:
            print(f"Error fetching qualities: {e}")  # Log detailed error
            # Check if it's a common pytube error
            if "unavailable" in str(e).lower():
                error_msg = self.texts["status_unavailable"]
            elif isinstance(e, KeyError) and 'streamingData' in str(e):
                error_msg = self.texts["status_streaming_error"]
            else:
                error_msg = self.texts["status_verify_error"].format(error=str(e)[:50])
            self.after(0, self._update_ui_after_fetch, None, error_msg, None, url)

    def _update_ui_after_fetch(self, stream_map, status_message, quality_options, original_url):
        """Updates UI after fetching qualities (runs in main thread)."""
        # Check if the URL has changed since the fetch started
        current_url = self.url_entry.get().strip()
        if self.mode.get() != "url" or current_url != original_url:
            # URL changed or mode switched, discard results
            return

        self.status_label.configure(text=status_message, text_color="green" if stream_map else "red")

        if stream_map and quality_options:
            self.available_video_streams = stream_map  # Save resolution -> stream map
            # Prepare display values like "720p (XX MB)"
            display_options = [f"{res} ({s.filesize_mb:.1f} MB)" for res, s in stream_map.items()]
            # Sort options by resolution
            try:
                display_options.sort(key=lambda x: int(re.match(r"(\d+)p", x).group(1)), reverse=True)
            except:
                pass  # Ignore sorting errors if format unexpected

            self.quality_combobox.configure(values=display_options)
            if display_options:
                self.selected_quality.set(display_options[0])  # Select the first (highest) by default
            else:
                self.selected_quality.set("")  # Shouldn't happen if quality_options is valid

            self.download_button.configure(state="normal")  # Enable download
            self._update_quality_widgets_state()  # Enable combobox if in Video mode
        else:
            self.available_video_streams = {}
            self.quality_combobox.configure(values=[""], state="disabled")
            self.selected_quality.set("")
            self.download_button.configure(state="disabled")  # Keep disabled if failed
            self._update_quality_widgets_state()  # Ensure disabled

    def select_folder(self):
        """Opens folder selection dialog."""
        folder_selected = tkinter.filedialog.askdirectory()
        if folder_selected:
            self.save_path.set(folder_selected)

    def sanitize_filename(self, title):
        """Sanitizes a filename by removing invalid characters."""
        sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        # Limit length to avoid OS issues
        return sanitized[:150]

    def progress_callback(self, stream, chunk, bytes_remaining):
        """Callback for download progress updates."""
        try:
            total_size = stream.filesize
            if total_size is None or total_size == 0:
                # Cannot calculate percentage if total size is unknown
                if self.progress_label.cget("text") != self.texts["downloading"]:
                    self.after(0, self.update_progress_label_only, self.texts["downloading"])
                # Reset bar if size unknown
                self.after(0, self.progress_bar.set, 0)
            else:
                bytes_downloaded = total_size - bytes_remaining
                percentage = (bytes_downloaded / total_size) * 100
                self.after(0, self.update_progress, percentage)
        except Exception as e:
            self.after(0, self.update_progress_label_only, self.texts["progress"])

    def update_progress(self, percentage):
        """Updates progress bar and percentage label."""
        self.progress_bar.set(percentage / 100)
        self.progress_label.configure(text=f"{percentage:.1f}%")

    def update_progress_label_only(self, text):
        """Updates just the progress label text."""
        self.progress_label.configure(text=text)

    # --- Download Dispatcher ---
    def start_download_dispatcher(self):
        """Checks the mode and starts the appropriate download process."""
        if self._is_downloading:  # Prevent multiple downloads at once
            print("Download already in progress.")
            return

        save_location = self.save_path.get()
        if not save_location or not os.path.isdir(save_location):
            CTkMessagebox(
                title=self.texts["folder_error_title"], 
                message=self.texts["folder_error_message"], 
                icon="cancel"
            )
            self.status_label.configure(text=self.texts["error_invalid_folder"], text_color="red")
            return

        current_mode = self.mode.get()
        self.disable_widgets_for_download()  # Disable UI

        if current_mode == "url":
            self.start_single_download_thread()
        elif current_mode == "batch":
            self.start_batch_download_thread()
        else:
            print(f"Unknown mode: {current_mode}")
            self.enable_widgets()  # Re-enable if mode is wrong

    def disable_widgets_for_download(self):
        """Disables interactive widgets during download."""
        self._is_downloading = True
        self.download_button.configure(state="disabled", text=self.texts["downloading"])
        self.browse_button.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        self.batch_textbox.configure(state="disabled")
        self.folder_entry.configure(state="disabled")
        self.radio_audio.configure(state="disabled")
        self.radio_video.configure(state="disabled")
        self.radio_mode_url.configure(state="disabled")
        self.radio_mode_batch.configure(state="disabled")
        self.language_selector.configure(state="disabled")  # Disable language changes during download
        self.quality_combobox.configure(state="disabled")  # Always disable during download
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")

    def start_single_download_thread(self):
        """Starts download for single URL mode."""
        url = self.url_entry.get().strip()
        if not url:  # Should be caught earlier, but double-check
            self.update_status(self.texts["status_error_no_url"], "red")
            self.enable_widgets()
            return

        save_location = self.save_path.get()  # Already validated
        chosen_format = self.download_type.get()
        quality_selection_full = self.selected_quality.get()  # E.g. "720p (15.3 MB)"

        # Extract only the resolution (e.g. "720p") from the selection
        chosen_quality = ""
        if chosen_format == "video" and quality_selection_full:
            match = re.match(r"(\d+)p", quality_selection_full)
            if match:
                chosen_quality = match.group(0)  # Get the full match (e.g. "720p")
            else:
                # This case might happen if the combobox value is somehow invalid
                self.update_status(self.texts["status_quality_error"], "red")
                self.enable_widgets()
                return
            # Verify the chosen quality exists in our map
            if chosen_quality not in self.available_video_streams:
                self.update_status(self.texts["status_quality_unavailable"].format(quality=chosen_quality), "red")
                self.enable_widgets()
                return
        elif chosen_format == "video" and not quality_selection_full:
            # Video selected but no quality chosen
            self.update_status(self.texts["status_select_quality"], "red")
            self.enable_widgets()
            return

        self.status_label.configure(text=self.texts["status_starting_download"], text_color="orange")

        # Pass the format AND the quality key (e.g., "720p") if applicable
        download_thread = threading.Thread(target=self.download_media, 
                                          args=(url, save_location, chosen_format, chosen_quality), 
                                          daemon=True)
        download_thread.start()

    def start_batch_download_thread(self):
        """Starts the batch download process in a separate thread."""
        search_terms_raw = self.batch_textbox.get("1.0", "end-1c").strip()
        search_terms = [term.strip() for term in search_terms_raw.split('\n') if term.strip()]

        if not search_terms:
            self.update_status(self.texts["status_no_search_terms"], "red")
            self.enable_widgets()
            return

        save_location = self.save_path.get()  # Already validated
        chosen_format = self.download_type.get()

        self.status_label.configure(
            text=self.texts["status_batch_start"].format(count=len(search_terms)), 
            text_color="orange"
        )

        batch_thread = threading.Thread(
            target=self._batch_download_task, 
            args=(search_terms, save_location, chosen_format), 
            daemon=True
        )
        batch_thread.start()

    def _batch_download_task(self, terms, save_path, download_type):
        """Performs search and download for each term in the list."""
        total_items = len(terms)
        success_count = 0
        fail_count = 0

        for i, term in enumerate(terms):
            item_num = i + 1
            status_msg = self.texts["status_batch_searching"].format(
                current=item_num, 
                total=total_items, 
                term=term[:30]
            )
            self.after(0, self.update_status, status_msg)
            self.after(0, self.update_progress, 0)  # Reset progress for each item
            self.after(0, self.update_progress_label_only, f"Item {item_num}/{total_items}")

            try:
                search = Search(term)
                results = search.results

                if not results:
                    status_msg = self.texts["status_batch_not_found"].format(
                        current=item_num, 
                        total=total_items, 
                        term=term[:30]
                    )
                    self.after(0, self.update_status, status_msg, "orange")
                    fail_count += 1
                    continue  # Skip to next term

                first_result_yt = results[0]  # Get the first YouTube object
                video_url = first_result_yt.watch_url
                video_title = first_result_yt.title

                # Determine quality_key if video type
                quality_key = ""  # Not used for audio
                if download_type == "video":
                    # Fetch streams for this video
                    streams = first_result_yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
                    if streams:
                        quality_key = streams[0].resolution  # Get e.g., "720p" from the best stream
                    else:
                        status_msg = self.texts["status_batch_no_mp4"].format(
                            current=item_num, 
                            total=total_items, 
                            title=video_title[:30]
                        )
                        self.after(0, self.update_status, status_msg, "orange")
                        fail_count += 1
                        continue

                # Download this item
                download_successful = self._execute_single_download(
                    video_url, save_path, download_type, quality_key, 
                    first_result_yt, item_num, total_items
                )

                if download_successful:
                    success_count += 1
                else:
                    fail_count += 1

            except Exception as e:
                status_msg = self.texts["status_batch_not_found"].format(
                    current=item_num, 
                    total=total_items, 
                    term=term[:30]
                )
                self.after(0, self.update_status, status_msg, "red")
                fail_count += 1
                # Log the full error
                print(f"Error during batch processing for term '{term}': {e}")

        # Batch finished
        final_status = self.texts["batch_complete"].format(success=success_count, fail=fail_count)
        final_color = "green" if success_count > 0 and fail_count == 0 else ("orange" if success_count > 0 else "red")
        self.after(0, self.update_status, final_status, final_color)
        self.after(0, self.enable_widgets)

    def _execute_single_download(self, url, save_path, download_type, video_quality, yt_object=None, item_num=None, total_items=None):
        """Downloads a single media item. Assumes UI is already disabled."""
        prefix = f"Batch ({item_num}/{total_items}): " if item_num is not None else ""
        try:
            # Use provided yt_object if available, otherwise create new
            if yt_object:
                yt = yt_object
                # Attach progress callback if using existing object
                yt.register_on_progress_callback(self.progress_callback)
            else:
                yt = YouTube(url, on_progress_callback=self.progress_callback)

            stream = None
            file_extension = ""
            status_type = download_type

            if download_type == "audio":
                stream = yt.streams.get_audio_only(subtype='mp4')  # Prefer mp4 container for audio
                if not stream:  # Fallback if mp4 audio not found
                    stream = yt.streams.get_audio_only()
                file_extension = ".mp3"  # Final desired extension
                if not stream:
                    self.after(0, self.update_status, 
                              self.texts["status_error_no_audio"].format(prefix=prefix), "red")
                    return False
            elif download_type == "video":
                # In batch mode or URL mode with quality selected
                if video_quality:  # We have a specific quality target
                    # Get the exact stream based on quality key (e.g., '720p')
                    stream_map_local = {s.resolution: s for s in yt.streams.filter(progressive=True, file_extension='mp4')}
                    stream = stream_map_local.get(video_quality)
                    if stream:
                        file_extension = ".mp4"
                        status_type = f"video ({video_quality})"
                    else:
                        # Fallback if specific quality wasn't found
                        self.after(0, self.update_status, 
                                  self.texts["status_quality_not_found"].format(
                                      prefix=prefix, quality=video_quality
                                  ), "orange")
                        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                        if stream:
                            file_extension = ".mp4"
                            status_type = f"video ({stream.resolution} - highest)"
                        else:
                            self.after(0, self.update_status, 
                                      self.texts["status_no_mp4_stream"].format(prefix=prefix), "red")
                            return False
                else:  # No specific quality given (shouldn't happen for video in single mode)
                    self.after(0, self.update_status, 
                              self.texts["status_internal_error"].format(prefix=prefix), "red")
                    return False

            # --- Prepare filename ---
            base_filename = self.sanitize_filename(yt.title)
            output_filename = f"{base_filename}{file_extension}"
            final_file_path = os.path.join(save_path, output_filename)

            # Check if file already exists
            if os.path.exists(final_file_path):
                self.after(0, self.update_status, 
                          self.texts["status_file_exists"].format(prefix=prefix, filename=output_filename), "blue")
                self.after(0, self.update_progress, 100.0)  # Mark as complete
                return True  # Treat existing as success

            # --- Download ---
            self.after(0, self.update_status, 
                      self.texts["status_downloading"].format(
                          prefix=prefix, type=status_type, title=yt.title[:30]
                      ), "orange")
            # Download with a temporary name or let pytube decide
            downloaded_file_path = stream.download(output_path=save_path)
            actual_downloaded_filename = os.path.basename(downloaded_file_path)

            # --- Rename/Move to desired final name ---
            final_filename_to_show = actual_downloaded_filename  # Default if rename fails
            rename_needed = downloaded_file_path != final_file_path

            if rename_needed:
                try:
                    # Ensure target does not exist
                    if os.path.exists(final_file_path):
                        os.remove(final_file_path)
                    os.rename(downloaded_file_path, final_file_path)
                    final_filename_to_show = output_filename
                    rename_success = True
                except OSError as e:
                    print(f"Error renaming file to {output_filename}: {e}")
                    self.after(0, self.update_status, 
                              self.texts["status_download_renamed"].format(
                                  prefix=prefix, filename=final_filename_to_show
                              ), "orange")
                    rename_success = False
            else:
                # Already downloaded with the correct name
                final_filename_to_show = output_filename
                rename_success = True

            # --- Report Success ---
            if rename_success:
                self.after(0, self.update_progress, 100.0)
                self.after(0, self.update_status, 
                          self.texts["status_success"].format(
                              prefix=prefix, filename=final_filename_to_show
                          ), "green")
                return True
            else:
                # Renaming failed but download was successful
                self.after(0, self.update_progress, 100.0)
                return False  # Count as failure for batch stats if rename fails

        # --- Exception handling ---
        except Exception as e:
            error_type = type(e).__name__
            self.after(0, self.update_status, 
                      self.texts["status_download_error"].format(
                          prefix=prefix, error_type=error_type, error=str(e)[:60]
                      ), "red")
            print(f"Error downloading '{url}': {e}")  # Log full error
            # Ensure progress bar doesn't show partial progress on error
            self.after(0, self.progress_bar.set, 0)
            self.after(0, self.update_progress_label_only, "Error")
            return False

    def download_media(self, url, save_path, download_type, video_quality):
        """Target for the single URL download thread."""
        try:
            download_successful = self._execute_single_download(url, save_path, download_type, video_quality)
            # Status is updated within _execute_single_download
        except Exception as e:
            # Catch unexpected errors in the thread setup itself
            self.after(0, self.update_status, 
                      self.texts["status_unexpected_error"].format(error=str(e)), "red")
        finally:
            # Re-enable widgets after single download attempt
            self.after(0, self.enable_widgets)

    def update_status(self, message, color="gray"):
        """Updates the status label with a message and color."""
        # Limit status message length
        max_len = 80
        display_message = message if len(message) <= max_len else message[:max_len-3] + "..."
        self.status_label.configure(text=display_message, text_color=color)

    def enable_widgets(self):
        """Re-enables interactive widgets after download or when changing mode."""
        self._is_downloading = False
        current_mode = self.mode.get()

        # Enable mode switching always
        self.radio_mode_url.configure(state="normal")
        self.radio_mode_batch.configure(state="normal")
        self.language_selector.configure(state="normal")  # Re-enable language selection

        # Enable folder selection
        self.browse_button.configure(state="normal")
        self.folder_entry.configure(state="normal" if self.save_path.get() else "readonly")

        # Enable format selection
        self.radio_audio.configure(state="normal")
        self.radio_video.configure(state="normal")

        # Enable mode-specific inputs
        if current_mode == "url":
            self.url_entry.configure(state="normal")
            self.batch_textbox.configure(state="disabled")  # Ensure batch is disabled
            # Quality widgets are handled by _update_quality_widgets_state
            self._update_quality_widgets_state()
            # Enable download button only if URL has been verified successfully
            self.download_button.configure(state="normal" if self.available_video_streams else "disabled")

        elif current_mode == "batch":
            self.url_entry.configure(state="disabled")  # Ensure URL is disabled
            self.batch_textbox.configure(state="normal")
            # Quality widgets remain disabled in batch mode
            self.quality_label.configure(state="disabled")
            self.quality_combobox.configure(state="disabled")
            # Enable download button for batch mode
            self.download_button.configure(state="normal")

        # Restore download button text
        self.download_button.configure(text=self.texts["download_button"])


# --- Run the Application ---
if __name__ == "__main__":
    app = App()
    app.mainloop()