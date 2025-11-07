import matplotlib.pyplot as plt
import pandas as pd


# ------------------------------------------
# 🩸 Funkcje rysujące histogramy
# ------------------------------------------
def plot_age_hist(df):
    """Histogram wieku pacjentów"""
    if df is None or "Age" not in df.columns:
        print("⚠️ Brak danych do wyświetlenia histogramu wieku.")
        return
    plt.figure()
    plt.hist(df["Age"].dropna(), bins=10, color="skyblue", edgecolor="black")
    plt.title("Histogram wieku pacjentów")
    plt.xlabel("Wiek [lata]")
    plt.ylabel("Liczba pacjentów")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def plot_heartrate_hist(df):
    """Histogram tętna"""
    if df is None or "HeartRate" not in df.columns:
        print("⚠️ Brak danych do wyświetlenia histogramu tętna.")
        return
    plt.figure()
    plt.hist(df["HeartRate"].dropna(), bins=10, color="lightcoral", edgecolor="black")
    plt.title("Histogram tętna")
    plt.xlabel("Tętno [uderzenia/min]")
    plt.ylabel("Liczba pacjentów")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def plot_systolic_hist(df):
    """Histogram ciśnienia skurczowego"""
    if df is None or "SystolicBP" not in df.columns:
        print("⚠️ Brak danych do wyświetlenia histogramu ciśnienia skurczowego.")
        return
    plt.figure()
    plt.hist(df["SystolicBP"].dropna(), bins=10, color="lightgreen", edgecolor="black")
    plt.title("Histogram ciśnienia skurczowego (SystolicBP)")
    plt.xlabel("Ciśnienie skurczowe [mmHg]")
    plt.ylabel("Liczba pacjentów")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def plot_diastolic_hist(df):
    """Histogram ciśnienia rozkurczowego"""
    if df is None or "DiastolicBP" not in df.columns:
        print("⚠️ Brak danych do wyświetlenia histogramu ciśnienia rozkurczowego.")
        return
    plt.figure()
    plt.hist(df["DiastolicBP"].dropna(), bins=10, color="plum", edgecolor="black")
    plt.title("Histogram ciśnienia rozkurczowego (DiastolicBP)")
    plt.xlabel("Ciśnienie rozkurczowe [mmHg]")
    plt.ylabel("Liczba pacjentów")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


# ------------------------------------------
# 📈 Wykres rozrzutu (Age vs SystolicBP)
# ------------------------------------------
def plot_scatter(df):
    """Wykres rozrzutu wieku vs ciśnienia skurczowego"""
    if df is None or "Age" not in df.columns or "SystolicBP" not in df.columns:
        print("⚠️ Brak danych do wyświetlenia wykresu rozrzutu.")
        return
    plt.figure()
    plt.scatter(df["Age"], df["SystolicBP"], color="royalblue", alpha=0.7)
    plt.title("Wykres rozrzutu: Wiek vs SystolicBP")
    plt.xlabel("Wiek [lata]")
    plt.ylabel("Ciśnienie skurczowe [mmHg]")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


# ------------------------------------------
# 💾 Funkcje pomocnicze – do zapisu wykresów
# ------------------------------------------
def save_hist(df, col, filename, folder):
    """
    Tworzy histogram dla kolumny `col` i zapisuje do pliku.
    Używane w raporcie PDF.
    """
    import os
    path = os.path.join(folder, filename)
    if df is not None and col in df.columns:
        plt.figure()
        plt.hist(df[col].dropna(), bins=10, edgecolor='black', color='lightblue')
        plt.title(f"Histogram {col}")
        plt.xlabel(col)
        plt.ylabel("Liczba pacjentów")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
    return path


def save_scatter(df, filename, folder):
    """
    Tworzy wykres rozrzutu (Age vs SystolicBP) i zapisuje do pliku.
    Używane w raporcie PDF.
    """
    import os
    path = os.path.join(folder, filename)
    if df is not None and "Age" in df.columns and "SystolicBP" in df.columns:
        plt.figure()
        plt.scatter(df["Age"], df["SystolicBP"], color="royalblue", alpha=0.7)
        plt.title("Wykres rozrzutu: Wiek vs SystolicBP")
        plt.xlabel("Wiek [lata]")
        plt.ylabel("SystolicBP [mmHg]")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
    return path
