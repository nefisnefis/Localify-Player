
# Localify Player 🎵

## **Polski / Polish**

Localify Player to prosty, lokalny serwer muzyczny w stylu Spotify, który pozwala odtwarzać pliki muzyczne z komputera w przeglądarce.  
Program umożliwia przeglądanie i odtwarzanie utworów z funkcjami takimi jak shuffle, repeat, regulacja głośności, a także wyświetla metadane utworów (tytuł, wykonawca, album, okładka).

## Funkcje
- Odtwarzanie lokalnych plików muzycznych (.mp3, .m4a, .wav, .flac, .ogg)  
- Czytanie metadanych utworów (tytuł, wykonawca, album, okładka)  
- Przyciski shuffle i repeat  
- Regulacja głośności i postępu odtwarzania  
- Możliwość pobierania utworów  
- Prostey interfejs w przeglądarce  

## Instalacja
1. Sklonuj repozytorium:
   ```bash
   git clone <repo-url>
   cd <repo-folder>
2. Zainstaluj wymagane pakiety:

   ```bash
   pip install flask mutagen Pillow
   ```
3. Umieść swoje pliki muzyczne w folderze `music` (program utworzy go automatycznie, jeśli nie istnieje).
4. Uruchom aplikację:

   ```bash
   python localify.py (w sumie wystrczy uruchomic z pliku)
   ```
5. Otwórz przeglądarkę i wejdź na adres:

   ```
   http://<TWÓJ_IP>:5000
   ```

---

## **English**

Localify Player is a simple local music server inspired by Spotify, allowing you to play music files from your computer in a browser.
It supports browsing and playing tracks with features like shuffle, repeat, volume control, and it reads track metadata (title, artist, album, cover).

## Features

* Play local music files (.mp3, .m4a, .wav, .flac, .ogg)
* Read track metadata (title, artist, album, cover)
* Shuffle and repeat buttons
* Volume and progress control
* Download tracks
* Simple browser-based interface

## Installation

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. Install dependencies:

   ```bash
   pip install flask mutagen Pillow
   ```
3. Place your music files in the `music` folder (it will be created automatically if missing).
4. Run the application:

   ```bash
   python localify.py
   ```
5. Open your browser and go to:

   ```
   http://<YOUR_IP>:5000
   ```

---

**Requirements / Wymagania**

* Python 3.7+
* Flask
* Mutagen
* Pillow
