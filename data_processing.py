import pandas as pd
import sqlite3


# -------------------------------
# Wczytywanie danych
# -------------------------------

def load_csv(path):
    """
    Wczytuje dane pacjentów z pliku CSV.
    Oczekiwane kolumny: PatientID, Age, Gender, BloodPressure, HeartRate, Symptoms
    Automatycznie rozdziela BloodPressure na SystolicBP i DiastolicBP.
    """
    df = pd.read_csv(path)

    # Upewnij się, że kolumna BloodPressure istnieje
    if "BloodPressure" in df.columns:
        # Rozdzielenie wartości "120/80" na dwie liczby
        bp_split = df["BloodPressure"].astype(str).str.split("/", expand=True)
        if bp_split.shape[1] == 2:
            df["SystolicBP"] = pd.to_numeric(bp_split[0], errors="coerce")
            df["DiastolicBP"] = pd.to_numeric(bp_split[1], errors="coerce")
        else:
            df["SystolicBP"] = pd.to_numeric(df["BloodPressure"], errors="coerce")
            df["DiastolicBP"] = None

    return df


def load_sqlite(db_path, table='patients'):
    """
    Wczytuje dane z bazy SQLite (tabela 'patients').
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()

    # Tak samo rozdziel ciśnienie
    if "BloodPressure" in df.columns:
        bp_split = df["BloodPressure"].astype(str).str.split("/", expand=True)
        if bp_split.shape[1] == 2:
            df["SystolicBP"] = pd.to_numeric(bp_split[0], errors="coerce")
            df["DiastolicBP"] = pd.to_numeric(bp_split[1], errors="coerce")
        else:
            df["SystolicBP"] = pd.to_numeric(df["BloodPressure"], errors="coerce")
            df["DiastolicBP"] = None

    return df


# -------------------------------
# Filtrowanie danych
# -------------------------------

def filter_dataframe(df, age_min=None, age_max=None, systolic_min=None, systolic_max=None,
                     diastolic_min=None, diastolic_max=None, gender=None, symptoms_contains=None):
    """
    Filtruje dane według podanych kryteriów.
    """
    out = df.copy()

    if age_min is not None:
        out = out[out["Age"] >= age_min]
    if age_max is not None:
        out = out[out["Age"] <= age_max]
    if systolic_min is not None:
        out = out[out["SystolicBP"] >= systolic_min]
    if systolic_max is not None:
        out = out[out["SystolicBP"] <= systolic_max]
    if diastolic_min is not None:
        out = out[out["DiastolicBP"] >= diastolic_min]
    if diastolic_max is not None:
        out = out[out["DiastolicBP"] <= diastolic_max]
    if gender:
        out = out[out["Gender"].str.upper() == gender.upper()]
    if symptoms_contains:
        out = out[out["Symptoms"].str.contains(symptoms_contains, case=False, na=False)]

    return out


# -------------------------------
# Statystyki
# -------------------------------

def compute_statistics(df, groupby=None):
    """
    Oblicza statystyki: średnia i mediana dla kolumn liczbowych.
    Jeśli podano groupby, dane są grupowane po wskazanej kolumnie (np. 'Gender').
    """
    res = {}
    if groupby and groupby in df.columns:
        grouped = df.groupby(groupby)
        res["mean"] = grouped.mean(numeric_only=True)
        res["median"] = grouped.median(numeric_only=True)
    else:
        res["mean"] = df.mean(numeric_only=True)
        res["median"] = df.median(numeric_only=True)
    return res


# -------------------------------
# Eksport
# -------------------------------

def export_csv(df, path):
    """
    Eksportuje DataFrame do pliku CSV.
    """
    df.to_csv(path, index=False)
