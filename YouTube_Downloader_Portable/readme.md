# YouTube Downloader (MP3/MP4) - Pytubefix GUI

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pytubefix](https://img.shields.io/badge/powered%20by-pytubefix-red.svg)](https://github.com/pytubefix/pytubefix)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-green.svg)](https://github.com/TomSchimansky/CustomTkinter)

![GitHub top language](https://img.shields.io/github/languages/top/YourUsername/YourRepoName) <!-- Replace YourUsername/YourRepoName -->
![GitHub last commit](https://img.shields.io/github/last-commit/YourUsername/YourRepoName) <!-- Replace YourUsername/YourRepoName -->

---

**Download your favorite YouTube videos or audios easily and quickly with this intuitive desktop application.**

This application allows you to download YouTube content in MP4 (video) or MP3 (audio) format directly to your computer. It offers two modes of operation: download from a specific URL or batch search and download based on search terms.

Built with Python, `pytubefix` for YouTube interaction, and `CustomTkinter` for a modern and pleasant graphical interface.

## ✨ Key Features

*   **Intuitive Graphical Interface:** Easy to use thanks to `CustomTkinter`.
*   **Single URL Mode:** Paste the URL of a YouTube video to download it.
    *   Automatic URL verification when pasting or typing.
    *   Video quality selection (progressive MP4).
*   **Batch Search Mode:** Paste a list of names or search terms (one per line).
    *   The application will search for each term on YouTube.
    *   It will automatically download the first result found for each term.
*   **Flexible Formats:** Download as MP4 video (with audio) or extract only the audio in MP3 format.
*   **Folder Selector:** Easily choose where to save your downloads.
*   **Progress Bar:** Visualize the download progress in real-time.
*   **Cross-Platform:** Works on Windows, macOS, and Linux (as long as Python and Tkinter are installed).

## 📸 Screenshots

*(Here you can add your screenshots. Replace the descriptive text with the Markdown image syntax)*

**Single URL Mode:**
![Placeholder: Main interface in URL mode](img/single-url.png "Interface in URL Mode")

**Batch Search Mode:**
![Placeholder: Main interface in Batch mode](img/batch-url.png "Interface in Batch Mode")

**Quality Selection (URL Mode):**
![Placeholder: Quality selection dropdown](img/quality-select.png "Quality Selection")

## 🛠️ Installation

### Windows portable

Run `YouTube_Downloader_Portable/YouTube_Downloader.exe` from the repository. This build includes Python, Node.js and FFmpeg, so it can create MP3 files and MP4 files with sound without installing those tools separately.

### From source

You need to have **Python 3.8 or higher** installed on your system.

1.  **Clone the repository (or download the ZIP):**
    ```bash
    git clone https://github.com/Nikoxx99/BetterYoutubeDownloader.git # Replace with your URL
    cd BetterYoutubeDownloader
    ```

2.  **(Optional but recommended) Create a virtual environment:**
    ```bash
    python -m venv venv
    # Activate it:
    # Windows: .\venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    python -m pip install -r requirements.txt
    ```

    The requirements include `pytubefix>=11.1.0`. Its `WEB` client uses Node.js to generate a YouTube PO Token automatically; the current pytubefix package installs the Node.js runtime dependency. `imageio-ffmpeg` supplies FFmpeg on common platforms for real MP3 conversion and MP4 files with sound. See [FFMPEG_SETUP.md](FFMPEG_SETUP.md) if your platform does not have a bundled FFmpeg binary.

## YouTube bot-detection error

The application uses pytubefix's `WEB` client for URL checks, downloads and batch search. If YouTube returns a bot-detection error, the app shows a message suggesting another network or waiting before retrying. This response can indicate that YouTube has blocked the current connection or session; updating the app does not guarantee that YouTube will allow the request.

For diagnosis, update the dependencies with `python -m pip install -U -r requirements.txt`, try the same public video in a browser on the same network, and retry later or from another network. If the browser also cannot play it, check whether the video itself is unavailable or restricted. The app does not sign in to YouTube or import browser cookies automatically. See the [pytubefix PO Token guide](https://pytubefix.readthedocs.io/en/latest/user/po_token.html) for current upstream limitations.

## ▶️ How to Use

1.  **Run the application:**
    ```bash
    python download.py
    ```

2.  **Select the Mode:**
    *   **Single URL:** Paste the full YouTube video URL into the corresponding field. The application will automatically verify the URL and, if it's valid and you selected "Video (MP4)", it will load the available qualities.
    *   **Batch Search:** Paste a list of song names, artists, or any search term into the large text box, ensuring each term is on a new line.

3.  **Choose the Destination Folder:** Click "Select" ("Seleccionar") to choose where the downloaded files will be saved.

4.  **Select the Format:** Choose between "Audio (MP3)" or "Video (MP4)".

5.  **(URL Mode - Video Only):** If you chose "Video (MP4)" and the URL is valid, select the desired quality from the dropdown menu.

6.  **Download:** Click the "Download" ("Descargar") button.
    *   In **URL Mode**, the specified video/audio will be downloaded.
    *   In **Batch Mode**, the application will search for each term and download the first result for each, showing the overall progress and the status of each item.

7.  **Monitor Progress:** Observe the progress bar and status label to see the download progress.

## 🤝 Contributions

Contributions are welcome. If you have ideas to improve the application, find a bug, or want to add new features, please:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Make your changes and commit (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

This project is under the MIT License. See the `LICENSE` file (if you add one) for more details.

---

*Created with ❤️ using Python*
