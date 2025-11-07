# Medical Data Analyzer (Minimal Variant)

## Opis
Prosty projekt w Pythonie analizujący dane medyczne pacjentów (wiek, ciśnienie, objawy).
Aplikacja umożliwia:
- wczytanie danych z pliku CSV lub z bazy SQLite,
- filtrowanie danych według wybranych kryteriów,
- obliczenia statystyczne (średnia, mediana, grupowanie) z użyciem Pandas,
- wizualizację wyników (histogram, wykres rozrzutu) z Matplotlib,
- eksport wyników do pliku CSV.

## Pliki
- `main.py` — GUI (tkinter) i punkt wejścia aplikacji.
- `data_processing.py` — funkcje wczytywania, filtrowania i statystyk (pandas).
- `viz.py` — funkcje wykresów matplotlib.
- `db.py` — przykładowe połączenie z SQLite (przykładowa baza `sample.db`).
- `sample_data.csv` — przykładowe dane.
- `sample.db` — przykładowa SQLite DB z tabelą `patients`.
- `requirements.txt` — potrzebne pakiety.
- `.gitignore` — dla repozytorium GitHub.

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

