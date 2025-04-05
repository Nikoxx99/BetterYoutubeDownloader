import tkinter
import tkinter.filedialog
import customtkinter as ctk
import threading
import os
from pytubefix import YouTube, Search
import urllib.error
import re
from CTkMessagebox import CTkMessagebox # Para mostrar errores/info de forma más elegante

# --- Configuración de la Apariencia ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("Descargador YouTube (MP3/MP4) - Pytubefix")
        self.geometry("600x680") # Aumentamos altura para el nuevo ComboBox y botón
        self.resizable(False, False)

        # --- Variables ---
        self.save_path = ctk.StringVar(value=os.getcwd())
        self.download_type = ctk.StringVar(value="audio") # Llama a _on_format_change al cambiar
        self.selected_quality = ctk.StringVar(value="") # Variable para la calidad seleccionada
        self.available_video_streams = {} # Diccionario para mapear "resolución" -> stream object
        self.mode = ctk.StringVar(value="url")
        self._check_url_debouncer = None
        self._is_downloading = False

        # --- Widgets ---
        self.create_widgets()
        self._on_mode_change() # Set initial UI state based on default mode
        self._update_quality_widgets_state() # Estado inicial de los widgets de calidad

    def create_widgets(self):
        # --- Marco Principal ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- Título ---
        title_label = ctk.CTkLabel(main_frame, text="Descargador YouTube", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 15))

        # --- NEW: Mode Selector ---
        mode_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mode_frame.pack(pady=(0, 10))

        mode_label = ctk.CTkLabel(mode_frame, text="Modo:")
        mode_label.pack(side="left", padx=(0, 10))

        self.radio_mode_url = ctk.CTkRadioButton(mode_frame, text="URL Única", variable=self.mode, value="url", command=self._on_mode_change)
        self.radio_mode_url.pack(side="left", padx=10)

        self.radio_mode_batch = ctk.CTkRadioButton(mode_frame, text="Búsqueda por Lote", variable=self.mode, value="batch", command=self._on_mode_change)
        self.radio_mode_batch.pack(side="left", padx=10)

        # --- Frame for URL input (conditionally shown) ---
        self.url_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.url_frame.pack(fill="x", padx=50, pady=(0, 10)) # Packed here, visibility controlled later

        url_label = ctk.CTkLabel(self.url_frame, text="Pega la URL del video:")
        url_label.pack(pady=(10, 5))

        # MODIFIED: Bind KeyRelease for automatic verification
        self.url_entry = ctk.CTkEntry(self.url_frame, width=350, placeholder_text="https://www.youtube.com/watch?v=...")
        self.url_entry.pack(side="left", expand=True, fill="x", pady=(0,10), padx=(0,0)) # Removed right padx
        self.url_entry.bind("<KeyRelease>", self._schedule_url_check)

        # --- NEW: Frame for Batch input (conditionally shown) ---
        self.batch_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        # Packed later in _on_mode_change

        batch_label = ctk.CTkLabel(self.batch_frame, text="Pega los nombres (uno por línea):")
        batch_label.pack(pady=(10, 5))

        self.batch_textbox = ctk.CTkTextbox(self.batch_frame, height=100, width=350) # Added width
        self.batch_textbox.pack(pady=(0,10), fill="x")

        # --- Selección de Carpeta ---
        folder_label = ctk.CTkLabel(main_frame, text="Guardar en:")
        folder_label.pack(pady=(10, 5))

        folder_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        folder_frame.pack(pady=(0, 10), fill="x", padx=50)

        self.folder_entry = ctk.CTkEntry(folder_frame, textvariable=self.save_path, state="readonly", width=300)
        self.folder_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.browse_button = ctk.CTkButton(folder_frame, text="Seleccionar", command=self.select_folder, width=80) # Ancho ajustado
        self.browse_button.pack(side="left")

        # --- Selector de Formato ---
        format_label = ctk.CTkLabel(main_frame, text="Selecciona el formato:")
        format_label.pack(pady=(15, 5))

        format_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        format_frame.pack(pady=(0, 5)) # Menos padding inferior

        self.radio_audio = ctk.CTkRadioButton(format_frame, text="Audio (MP3)", variable=self.download_type, value="audio", command=self._on_format_change)
        self.radio_audio.pack(side="left", padx=10)

        self.radio_video = ctk.CTkRadioButton(format_frame, text="Video (MP4)", variable=self.download_type, value="video", command=self._on_format_change)
        self.radio_video.pack(side="left", padx=10)

        # --- Selector de Calidad de Video (NUEVO) ---
        self.quality_frame = ctk.CTkFrame(main_frame, fg_color="transparent") # Frame para agrupar calidad
        self.quality_frame.pack(pady=(5, 10), fill="x", padx=50)

        self.quality_label = ctk.CTkLabel(self.quality_frame, text="Calidad (Video):")
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
        self.download_button = ctk.CTkButton(main_frame, text="Descargar", command=self.start_download_dispatcher, height=40, font=ctk.CTkFont(size=14, weight="bold"), state="disabled")
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

    # --- NEW: Mode Switching Logic ---
    def _on_mode_change(self):
        """Handles switching between 'URL Única' and 'Búsqueda por Lote' modes."""
        current_mode = self.mode.get()
        # Cancel any pending URL checks
        if self._check_url_debouncer:
            self.after_cancel(self._check_url_debouncer)
            self._check_url_debouncer = None

        if current_mode == "url":
            self.batch_frame.pack_forget() # Hide batch frame
            self.url_frame.pack(fill="x", padx=50, pady=(0, 10)) # Show URL frame
            self.status_label.configure(text="Pega una URL de YouTube", text_color="gray")
            # Enable/disable download based on if URL was previously verified
            self.download_button.configure(state="normal" if self.available_video_streams else "disabled")
            self._update_quality_widgets_state() # Update quality state based on current format
        elif current_mode == "batch":
            self.url_frame.pack_forget() # Hide URL frame
            self.batch_frame.pack(fill="x", padx=50, pady=(0, 10)) # Show batch frame
            self.status_label.configure(text="Pega nombres para buscar (uno por línea)", text_color="gray")
            self.download_button.configure(state="normal") # Enable download for batch mode
            # Disable quality selection for batch mode (downloads first result, maybe highest quality later?)
            self.quality_label.configure(state="disabled")
            self.quality_combobox.configure(state="disabled")
            self.available_video_streams = {} # Clear stream info
            self.selected_quality.set("")
            self.quality_combobox.configure(values=[""])

        # Reset progress
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        # Ensure widgets are enabled if not downloading
        if not self._is_downloading:
            self.enable_widgets()

    # --- NEW: Debounced URL Checker ---
    def _schedule_url_check(self, event=None):
        """Schedules the URL quality check after a brief pause."""
        if self.mode.get() != "url": return # Only check in URL mode

        # Cancel the previous scheduled check if it exists
        if self._check_url_debouncer:
            self.after_cancel(self._check_url_debouncer)

        # Schedule the check after 750ms
        self._check_url_debouncer = self.after(750, self.start_fetch_qualities_thread)

    # --- Modified Functions ---

    def _on_format_change(self):
        """Se llama cuando se cambia entre Audio y Video."""
        self._update_quality_widgets_state()
        # Si cambiamos a audio, limpiamos selección de calidad
        if self.download_type.get() == "audio":
            self.selected_quality.set("")
            self.quality_combobox.configure(values=[""])
            self.available_video_streams = {}
        # If switching to video in URL mode, re-trigger check if URL exists
        # elif self.mode.get() == "url" and self.url_entry.get():
        #     self.start_fetch_qualities_thread() # Re-fetch might be needed if not done yet

    def _update_quality_widgets_state(self):
        """Habilita/deshabilita los widgets de calidad según el formato Y MODO."""
        is_video = self.download_type.get() == "video"
        is_url_mode = self.mode.get() == "url"
        # Enable quality only if URL mode, Video format, and streams are loaded
        new_state = "normal" if is_url_mode and is_video and self.available_video_streams else "disabled"
        self.quality_label.configure(state=new_state)
        self.quality_combobox.configure(state=new_state)

    def start_fetch_qualities_thread(self):
        """Inicia la obtención de calidades en un hilo separado (para URL mode)."""
        # Ensure this is only called in URL mode implicitly by UI flow or add check
        if self.mode.get() != "url":
             print("Attempted to fetch qualities outside URL mode.")
             return

        url = self.url_entry.get().strip()
        if not url or not url.startswith(("https://www.youtube.com/", "https://youtu.be/")):
            # Don't show popup for invalid URL during typing, just update status
            self.status_label.configure(text="URL inválida o incompleta", text_color="red")
            self.download_button.configure(state="disabled")
            self.quality_combobox.configure(values=[""], state="disabled")
            self.selected_quality.set("")
            self.available_video_streams = {}
            self._update_quality_widgets_state()
            return

        # UI update: indicate checking is happening
        self.status_label.configure(text="Verificando URL y calidades...", text_color="orange")
        # Disable download button while checking
        self.download_button.configure(state="disabled")
        self.quality_combobox.configure(values=[""], state="disabled")
        self.selected_quality.set("")
        self.available_video_streams = {}
        self._update_quality_widgets_state() # Ensure quality is disabled during check

        fetch_thread = threading.Thread(target=self._fetch_qualities_task, args=(url,), daemon=True)
        fetch_thread.start()

    def _fetch_qualities_task(self, url):
        """Tarea que se ejecuta en el hilo para obtener las calidades."""
        try:
            yt = YouTube(url)
            # Priorizamos streams progresivos (video+audio) MP4
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

            if not streams:
                # Try adaptive if progressive fails? Maybe later. For now, fail.
                 self.after(0, self._update_ui_after_fetch, None, f"No se encontraron videos MP4 (progresivos) para {yt.title[:30]}...", None, url)
                 return

            stream_map = {}
            quality_options = []
            # MODIFIED: Store stream object directly with a formatted string key
            stream_map_display = {}
            for s in streams:
                 if s.resolution not in stream_map: # Avoid duplicate resolutions
                    display_text = f"{s.resolution} ({s.filesize_mb:.1f} MB)"
                    stream_map[s.resolution] = s # Map resolution ('720p') to stream
                    stream_map_display[display_text] = s # Map display text to stream (easier lookup later?) No, use the simple map.
                    quality_options.append(display_text) # List for combobox

            if not quality_options:
                 self.after(0, self._update_ui_after_fetch, None, f"No se encontraron calidades válidas para {yt.title[:30]}...", None, url)
                 return

            # Pass the original URL along to check if it changed while fetching
            self.after(0, self._update_ui_after_fetch, stream_map, f"Video: {yt.title[:40]}...", quality_options, url)

        except urllib.error.URLError as e:
             self.after(0, self._update_ui_after_fetch, None, "Error de red al verificar URL.", None, url)
        except Exception as e:
             print(f"Error fetching qualities: {e}") # Log detailed error
             # Check if it's a common pytube error (e.g., video unavailable)
             if "unavailable" in str(e).lower():
                 error_msg = "Video no disponible o restringido."
             elif isinstance(e, KeyError) and 'streamingData' in str(e):
                 error_msg = "No se pudo procesar la información del video (streamingData)."
             else:
                 error_msg = f"Error al verificar URL: {str(e)[:50]}"
             self.after(0, self._update_ui_after_fetch, None, error_msg, None, url)

    def _update_ui_after_fetch(self, stream_map, status_message, quality_options, original_url):
        """Actualiza la UI después de intentar obtener las calidades (se ejecuta en hilo principal)."""
        # Check if the URL has changed since the fetch started
        current_url = self.url_entry.get().strip()
        if self.mode.get() != "url" or current_url != original_url:
            # URL changed or mode switched, discard results
            # print(f"URL changed or mode switched. Discarding fetch results for {original_url}")
            return

        self.status_label.configure(text=status_message, text_color="green" if stream_map else "red")

        if stream_map and quality_options:
            self.available_video_streams = stream_map # Guardar el mapeo resolución -> stream
            # Prepare display values like "720p (XX MB)"
            display_options = [f"{res} ({s.filesize_mb:.1f} MB)" for res, s in stream_map.items()]
            # Sort options by resolution (assuming '720p' > '480p') - needs robust sorting
            try:
                display_options.sort(key=lambda x: int(re.match(r"(\d+)p", x).group(1)), reverse=True)
            except: pass # Ignore sorting errors if format unexpected

            self.quality_combobox.configure(values=display_options)
            if display_options:
                self.selected_quality.set(display_options[0]) # Select the first (highest) by default
            else:
                 self.selected_quality.set("") # Should not happen if quality_options is valid

            self.download_button.configure(state="normal") # Habilitar descarga
            self._update_quality_widgets_state() # Habilitar combobox si 'Video' está seleccionado
        else:
            self.available_video_streams = {}
            self.quality_combobox.configure(values=[""], state="disabled")
            self.selected_quality.set("")
            self.download_button.configure(state="disabled") # Mantener deshabilitado si falla
            self._update_quality_widgets_state() # Asegurarse que esté deshabilitado

    def select_folder(self):
        # --- Sin cambios ---
        folder_selected = tkinter.filedialog.askdirectory()
        if folder_selected:
            self.save_path.set(folder_selected)

    def sanitize_filename(self, title):
        # --- Sin cambios ---
        sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        # Limit length to avoid OS issues
        return sanitized[:150]

    def progress_callback(self, stream, chunk, bytes_remaining):
        # --- Sin cambios, pero wrapped in try-except ---
        try:
            total_size = stream.filesize
            if total_size is None or total_size == 0:
                 # Cannot calculate percentage if total size is unknown
                 # Maybe show bytes downloaded instead?
                 # For now, just show "Descargando..." in label if size unknown
                 if self.progress_label.cget("text") != "Descargando...":
                     self.after(0, self.update_progress_label_only, "Descargando...")
                 # Set progress bar to indeterminate if possible? CTkProgressBar doesn't support indeterminate directly
                 # We can simulate by moving it slightly or setting to 0/1
                 self.after(0, self.progress_bar.set, 0) # Reset bar if size unknown
            else:
                bytes_downloaded = total_size - bytes_remaining
                percentage = (bytes_downloaded / total_size) * 100
                self.after(0, self.update_progress, percentage)
        except Exception as e:
            # print(f"Advertencia en callback de progreso: {e}")
            self.after(0, self.update_progress_label_only, "Progreso...") # Generic label on error

    def update_progress(self, percentage):
        # --- Sin cambios ---
        self.progress_bar.set(percentage / 100)
        self.progress_label.configure(text=f"{percentage:.1f}%")

    def update_progress_label_only(self, text):
        # --- Sin cambios ---
        self.progress_label.configure(text=text)

    # --- NEW: Dispatcher for Download Button ---
    def start_download_dispatcher(self):
        """Checks the mode and starts the appropriate download process."""
        if self._is_downloading: # Prevent multiple downloads at once
             print("Download already in progress.")
             return

        save_location = self.save_path.get()
        if not save_location or not os.path.isdir(save_location):
             CTkMessagebox(title="Error", message="La carpeta de destino seleccionada no es válida.", icon="cancel")
             self.status_label.configure(text="Error: Carpeta inválida", text_color="red")
             return

        current_mode = self.mode.get()
        self.disable_widgets_for_download() # Disable UI

        if current_mode == "url":
            self.start_single_download_thread()
        elif current_mode == "batch":
            self.start_batch_download_thread()
        else:
            print(f"Unknown mode: {current_mode}")
            self.enable_widgets() # Re-enable if mode is wrong

    def disable_widgets_for_download(self):
        """Disables interactive widgets during download."""
        self._is_downloading = True
        self.download_button.configure(state="disabled", text="Descargando...")
        self.browse_button.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        self.batch_textbox.configure(state="disabled")
        self.folder_entry.configure(state="disabled")
        self.radio_audio.configure(state="disabled")
        self.radio_video.configure(state="disabled")
        self.radio_mode_url.configure(state="disabled")
        self.radio_mode_batch.configure(state="disabled")
        self.quality_combobox.configure(state="disabled") # Always disable during download
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")

    # --- MODIFIED: Renamed from start_download_thread ---
    def start_single_download_thread(self):
        """Starts download for the single URL mode."""
        url = self.url_entry.get().strip()
        if not url: # Should be caught earlier, but double-check
            self.update_status("Error: No hay URL para descargar.", "red")
            self.enable_widgets()
            return

        save_location = self.save_path.get() # Already validated
        chosen_format = self.download_type.get()
        quality_selection_full = self.selected_quality.get() # Ej: "720p (15.3 MB)"

        # Extract only the resolution (ej: "720p") from the selection
        chosen_quality = ""
        if chosen_format == "video" and quality_selection_full:
             match = re.match(r"(\d+p)", quality_selection_full)
             if match:
                 chosen_quality = match.group(1)
             else:
                  # This case might happen if the combobox value is somehow invalid
                  self.update_status("Error: Calidad de video no reconocida.", "red")
                  self.enable_widgets()
                  return
             # Verify the chosen quality exists in our map
             if chosen_quality not in self.available_video_streams:
                 self.update_status(f"Error: Calidad {chosen_quality} no disponible.", "red")
                 self.enable_widgets()
                 return
        elif chosen_format == "video" and not quality_selection_full:
             # Video selected but no quality chosen (e.g., fetch failed or cleared)
             self.update_status("Error: Selecciona una calidad de video.", "red")
             self.enable_widgets()
             return

        self.status_label.configure(text="Iniciando descarga...", text_color="orange")

        # Pass the format AND the quality key (e.g., "720p") if applicable
        download_thread = threading.Thread(target=self.download_media, args=(url, save_location, chosen_format, chosen_quality), daemon=True)
        download_thread.start()

    # --- NEW: Batch Download Thread Starter ---
    def start_batch_download_thread(self):
        """Starts the batch download process in a separate thread."""
        search_terms_raw = self.batch_textbox.get("1.0", "end-1c").strip()
        search_terms = [term.strip() for term in search_terms_raw.split('\n') if term.strip()]

        if not search_terms:
            self.update_status("Error: No hay términos de búsqueda en la lista.", "red")
            self.enable_widgets()
            return

        save_location = self.save_path.get() # Already validated
        chosen_format = self.download_type.get()
        # For batch, we don't use the quality combobox. We'll default to highest progressive for video.

        self.status_label.configure(text=f"Iniciando descargas por lote ({len(search_terms)} items)...", text_color="orange")

        batch_thread = threading.Thread(target=self._batch_download_task, args=(search_terms, save_location, chosen_format), daemon=True)
        batch_thread.start()

    # --- NEW: Batch Download Task (runs in thread) ---
    def _batch_download_task(self, terms, save_path, download_type):
        """Performs the search and download for each term in the list."""
        total_items = len(terms)
        success_count = 0
        fail_count = 0

        for i, term in enumerate(terms):
            item_num = i + 1
            self.after(0, self.update_status, f"Lote ({item_num}/{total_items}): Buscando '{term[:30]}...'")
            self.after(0, self.update_progress, 0) # Reset progress for each item
            self.after(0, self.update_progress_label_only, f"Item {item_num}/{total_items}")

            try:
                search = Search(term)
                results = search.results

                if not results:
                    self.after(0, self.update_status, f"Lote ({item_num}/{total_items}): No se encontró resultado para '{term[:30]}...'", "orange")
                    fail_count += 1
                    continue # Skip to next term

                first_result_yt = results[0] # Get the first YouTube object
                video_url = first_result_yt.watch_url
                video_title = first_result_yt.title

                # Now call download_media for this specific video
                # We need to determine the 'video_quality' parameter if type is video
                # For batch, let's default to highest progressive MP4
                quality_key = "" # Not used for audio
                if download_type == "video":
                    # Fetch streams specifically for this video
                    streams = first_result_yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
                    if streams:
                        quality_key = streams[0].resolution # Get e.g., "720p" from the best stream
                    else:
                        self.after(0, self.update_status, f"Lote ({item_num}/{total_items}): No hay MP4 progresivo para '{video_title[:30]}...'", "orange")
                        fail_count += 1
                        continue

                # Use a blocking call here within the thread. download_media handles its own UI updates via self.after()
                download_successful = self._execute_single_download(video_url, save_path, download_type, quality_key, first_result_yt, item_num, total_items)

                if download_successful:
                    success_count += 1
                else:
                    fail_count += 1

                # Small delay between downloads? Optional.
                # time.sleep(1)

            except Exception as e:
                 self.after(0, self.update_status, f"Lote ({item_num}/{total_items}): Error procesando '{term[:30]}...': {e}", "red")
                 fail_count += 1
                 # Log the full error
                 print(f"Error during batch processing for term '{term}': {e}")


        # Batch finished
        final_status = f"Lote completado: {success_count} éxito(s), {fail_count} fallo(s)."
        final_color = "green" if success_count > 0 and fail_count == 0 else ("orange" if success_count > 0 else "red")
        self.after(0, self.update_status, final_status, final_color)
        self.after(0, self.enable_widgets)

    # --- NEW HELPER: Executes a single download step (used by batch and potentially single) ---
    # This runs *within* the download thread (either single or batch)
    # Returns True if download (and rename) succeeded, False otherwise
    def _execute_single_download(self, url, save_path, download_type, video_quality, yt_object=None, item_num=None, total_items=None):
        """Downloads a single media item. Assumes UI is already disabled."""
        prefix = f"Lote ({item_num}/{total_items}): " if item_num is not None else ""
        try:
            # Use provided yt_object if available (from batch search), otherwise create new
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
                stream = yt.streams.get_audio_only(subtype='mp4') # Prefer mp4 container for audio
                if not stream: # Fallback if mp4 audio not found
                    stream = yt.streams.get_audio_only()
                file_extension = ".mp3" # Final desired extension
                if not stream:
                    self.after(0, self.update_status, f"{prefix}Error: No se encontró stream de audio.", "red")
                    return False
            elif download_type == "video":
                # In batch mode, video_quality is determined within the batch loop (e.g., highest)
                # In single mode, video_quality comes from the user selection ('720p')
                if video_quality: # We have a specific quality target
                    # Try to get the exact stream based on quality key (e.g., '720p')
                    # Re-fetch streams here if yt_object wasn't passed or to be safe
                    stream_map_local = {s.resolution: s for s in yt.streams.filter(progressive=True, file_extension='mp4')}
                    stream = stream_map_local.get(video_quality)
                    if stream:
                        file_extension = ".mp4"
                        status_type = f"video ({video_quality})"
                    else:
                         # Fallback if specific quality wasn't found (shouldn't happen in single mode if validated)
                         self.after(0, self.update_status, f"{prefix}Error: Calidad {video_quality} no encontrada. Intentando la más alta.", "orange")
                         stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                         if stream:
                              file_extension = ".mp4"
                              status_type = f"video ({stream.resolution} - más alta)"
                         else:
                              self.after(0, self.update_status, f"{prefix}Error: No se encontró ningún stream de video MP4 progresivo.", "red")
                              return False
                else: # No specific quality given (should not happen for video in single mode)
                    self.after(0, self.update_status, f"{prefix}Error interno: Calidad de video no especificada.", "red")
                    return False


            # --- Preparar nombre de archivo ---
            base_filename = self.sanitize_filename(yt.title)
            output_filename = f"{base_filename}{file_extension}"
            final_file_path = os.path.join(save_path, output_filename)

            # Check if file already exists
            if os.path.exists(final_file_path):
                self.after(0, self.update_status, f"{prefix}Ya existe: {output_filename}", "blue")
                self.after(0, self.update_progress, 100.0) # Mark as complete
                return True # Treat existing as success


            # --- Descargar ---
            self.after(0, self.update_status, f"{prefix}Descargando {status_type}: {yt.title[:30]}...", "orange")
            # Download with a temporary name or let pytube decide
            downloaded_file_path = stream.download(output_path=save_path)
            actual_downloaded_filename = os.path.basename(downloaded_file_path)

            # --- Renombrar/Mover al nombre final deseado ---
            final_filename_to_show = actual_downloaded_filename # Default if rename fails
            rename_needed = downloaded_file_path != final_file_path

            if rename_needed:
                try:
                    # Ensure target does not exist (might have been created between check and now)
                    if os.path.exists(final_file_path):
                        os.remove(final_file_path)
                    os.rename(downloaded_file_path, final_file_path)
                    final_filename_to_show = output_filename
                    rename_success = True
                except OSError as e:
                    print(f"Error renaming file to {output_filename}: {e}")
                    self.after(0, self.update_status, f"{prefix}¡Descargado! Guardado como {final_filename_to_show} (no se pudo renombrar)", "orange")
                    rename_success = False
            else:
                # Already downloaded with the correct name (less likely with sanitize)
                final_filename_to_show = output_filename
                rename_success = True


            # --- Report Success ---
            if rename_success:
                 self.after(0, self.update_progress, 100.0)
                 self.after(0, self.update_status, f"{prefix}¡Éxito! Guardado como: {final_filename_to_show}", "green")
                 return True
            else:
                 # Renaming failed, but download itself was okay
                 self.after(0, self.update_progress, 100.0) # Still 100% downloaded
                 return False # Count as failure for batch stats if rename fails? Or true? Let's say false.

        # --- Bloque de excepciones ---
        except Exception as e:
            error_type = type(e).__name__
            self.after(0, self.update_status, f"{prefix}Error ({error_type}) descargando: {str(e)[:60]}", "red")
            print(f"Error downloading '{url}': {e}") # Log full error
            # Ensure progress bar doesn't show partial progress on error
            self.after(0, self.progress_bar.set, 0)
            self.after(0, self.update_progress_label_only, "Error")
            return False

    # --- MODIFIED: Now calls _execute_single_download and handles enabling widgets ---
    def download_media(self, url, save_path, download_type, video_quality):
        """Target for the single URL download thread."""
        try:
            download_successful = self._execute_single_download(url, save_path, download_type, video_quality)
            # Status is updated within _execute_single_download
        except Exception as e:
            # Catch unexpected errors in the thread setup itself
            self.after(0, self.update_status, f"Error inesperado iniciando descarga: {e}", "red")
        finally:
            # Re-enable widgets after single download attempt
            self.after(0, self.enable_widgets)

    def update_status(self, message, color="gray"): # Default color added
        # --- Limit status message length ---
        max_len = 80
        display_message = message if len(message) <= max_len else message[:max_len-3] + "..."
        self.status_label.configure(text=display_message, text_color=color)

    def enable_widgets(self):
        """Habilita los widgets interactivos después de una descarga o al cambiar modo."""
        self._is_downloading = False
        current_mode = self.mode.get()

        # Enable mode switching always
        self.radio_mode_url.configure(state="normal")
        self.radio_mode_batch.configure(state="normal")

        # Enable folder selection
        self.browse_button.configure(state="normal")
        self.folder_entry.configure(state="normal" if self.save_path.get() else "readonly") # Keep readonly appearance

        # Enable format selection
        self.radio_audio.configure(state="normal")
        self.radio_video.configure(state="normal")

        # Enable mode-specific inputs
        if current_mode == "url":
            self.url_entry.configure(state="normal")
            self.batch_textbox.configure(state="disabled") # Ensure batch is disabled
             # Quality widgets are handled by _update_quality_widgets_state
            self._update_quality_widgets_state()
             # Enable download button only if URL has been verified successfully
            self.download_button.configure(state="normal" if self.available_video_streams else "disabled")

        elif current_mode == "batch":
            self.url_entry.configure(state="disabled") # Ensure URL is disabled
            self.batch_textbox.configure(state="normal")
            # Quality widgets remain disabled in batch mode
            self.quality_label.configure(state="disabled")
            self.quality_combobox.configure(state="disabled")
            # Enable download button for batch mode (if not empty?) - check in dispatcher
            self.download_button.configure(state="normal")


        # Restore download button text
        self.download_button.configure(text="Descargar")


# --- Ejecutar la Aplicación ---
if __name__ == "__main__":
    # Instalar CTkMessagebox si no está: pip install CTkMessagebox
    # No critical dependency, can be removed if not wanted
    # try:
    #     import CTkMessagebox
    # except ImportError:
    #     print("Warning: CTkMessagebox not found. Message boxes will use standard tkinter.")
    #     print("Install with: pip install CTkMessagebox")
        # Optionally replace CTkMessagebox calls with tkinter.messagebox

    app = App()
    app.mainloop()