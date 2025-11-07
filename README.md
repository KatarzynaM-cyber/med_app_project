# Medical Data Analyzer

## Opis
Prosty projekt w Pythonie analizujący dane medyczne pacjentów (wiek, ciśnienie, objawy).
Aplikacja umożliwia:
- wczytanie danych z pliku CSV (PatientID, Age, Gender, BloodPressure, HeartRate, Symptoms),
- filtrowanie danych wg wybranych kryteriów,
- obliczenia statystyczne (średnia, mediana, grupowanie — Pandas),
- wizualizacje danych (histogramy, wykresy rozrzutu — Matplotlib),
- eksport wyników i wykresów do pliku **PDF** z raportem,
- graficzny interfejs użytkownika (Tkinter) do obsługi programu.

## Pliki
- `main.py` — GUI (tkinter) i punkt wejścia aplikacji.
- `data_processing.py` — funkcje wczytywania, filtrowania i statystyk (pandas).
- `viz.py` — funkcje wykresów matplotlib.
- `db.py` — przykładowe połączenie z SQLite (przykładowa baza `sample.db`).
- `sample_data.csv` — przykładowe dane.
- `sample.db` — przykładowa SQLite DB z tabelą `patients`.
- `report.py` - funkcja tworzenia raportów w PDF.
- `requirements.txt` — potrzebne pakiety.
- `.gitignore` — dla repozytorium GitHub.

## Wykorzystane biblioteki

- `pandas`
- `matplotlib`
- `reportlab`
- `tkinter`

## Uruchomienie
1. Utwórz wirtualne środowisko (opcjonalnie):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   venv\Scripts\activate   # Windows
   ```
2. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
3. Uruchom:
   ```bash
   python main.py
   ```

## GitHub
Aby odzwierciedlić pracę w repozytorium:
```bash
git init
git add .
git commit -m "Initial commit - Medical Data Analyzer"
# utwórz repo na GitHub i ustaw remote, a potem:
git remote add origin https://github.com/yourusername/med-data-analyzer.git
git push -u origin main
```

