
# 🎵 Localify Player  

**EN | [PL below](#-localify-player-pl)**  

A simple self-hosted music player inspired by Spotify.  
It lets you upload and stream local music files on your PC, phone or other devices over the same network.  
It also supports Discord Rich Presence (RPC), so your friends can see what you’re listening to.

---

## ✨ Features (EN)

- 🎧 Play local music files (`.mp3`, `.m4a`, `.wav`, `.flac`, `.ogg`)  
- 📱 Access from phone or any device on the same Wi-Fi by typing your PC’s IP  
- 🖼️ Displays metadata: title, artist, album, cover art  
- ▶️ Spotify-style UI: play / pause, next / previous, shuffle, repeat  
- 🔊 Volume slider & progress bar  
- ⬆️ Upload songs via browser  
- 🟣 Discord Rich Presence integration – automatic status update  

---

## 🚀 Installation (EN)

1. Clone the repository:  
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO


2. Install dependencies:

   ```bash
   pip install flask mutagen Pillow pypresence
   ```
3. Create a `music` folder (automatically created on first run).
4. \[Optional] Create a Discord application at [Discord Developer Portal](https://discord.com/developers/applications) and get your **Client ID**.
   Put it in the Python script:

   ```python
   DISCORD_CLIENT_ID = "YOUR_CLIENT_ID"
   ```
5. Run the server:

   ```bash
   python app.py
   ```
6. Open in your browser: `http://localhost:5000` or `http://<your_pc_ip>:5000` (for phone).

---

## 📝 Usage (EN)

* Upload files via the built-in uploader or copy them directly into the `music` folder.
* Click on a track to play it.
* Control playback, volume, shuffle and repeat from the web UI.
* If Discord Rich Presence is configured and Discord is running, your status will update automatically.

# 🎵 Localify Player (PL)

Prosty, samodzielny odtwarzacz muzyki inspirowany Spotify.
Pozwala przesyłać i odtwarzać pliki muzyczne lokalnie na PC, telefonie lub innych urządzeniach w tej samej sieci.
Obsługuje również Discord Rich Presence (RPC), dzięki czemu znajomi widzą, czego słuchasz.

---

## ✨ Funkcje (PL)

* 🎧 Odtwarzanie lokalnych plików muzycznych (`.mp3`, `.m4a`, `.wav`, `.flac`, `.ogg`)
* 📱 Dostęp z telefonu lub dowolnego urządzenia w tej samej sieci Wi-Fi po wpisaniu IP komputera
* 🖼️ Wyświetlanie metadanych: tytuł, artysta, album, okładka
* ▶️ Interfejs w stylu Spotify: play / pause, następny / poprzedni, losowe, powtarzanie
* 🔊 Suwak głośności i pasek postępu
* ⬆️ Wgrywanie utworów przez przeglądarkę
* 🟣 Integracja z Discord Rich Presence – automatyczna aktualizacja statusu

---

## 🚀 Instalacja (PL)

1. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/TWOJ_UZYTKOWNIK/TWOJE_REPO.git
   cd TWOJE_REPO
   ```
2. Zainstaluj zależności:

   ```bash
   pip install flask mutagen Pillow pypresence
   ```
3. Utwórz folder `music` (zostanie też utworzony automatycznie przy pierwszym uruchomieniu).
4. \[Opcjonalnie] Utwórz aplikację w [Discord Developer Portal](https://discord.com/developers/applications) i pobierz **Client ID**.
   Wklej je do skryptu Pythona:

   ```python
   DISCORD_CLIENT_ID = "TWOJE_CLIENT_ID"
   ```
5. Uruchom serwer:

   ```bash
   python app.py
   ```
6. Otwórz w przeglądarce: `http://localhost:5000` lub `http://<ip_komputera>:5000` (dla telefonu).

---

## 📝 Użycie (PL)

* Wgraj pliki przez wbudowany uploader lub skopiuj je bezpośrednio do folderu `music`.
* Kliknij utwór, aby go odtworzyć.
* Steruj odtwarzaniem, głośnością, losowym trybem i powtarzaniem z poziomu web UI.
* Jeśli skonfigurujesz Discord Rich Presence i Discord będzie włączony, status zaktualizuje się automatycznie.

---
