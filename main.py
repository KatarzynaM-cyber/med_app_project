import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pandas as pd
import data_processing as dp
import viz
import report

class MedicalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analiza danych medycznych")
        self.root.geometry("750x600")

        self.df = None
        self.sort_state = {}

        # ------------------------------
        # Przyciski główne
        # ------------------------------
        tk.Button(root, text="📂 Wczytaj dane z CSV", command=self.load_csv, width=30).pack(pady=5)
        tk.Button(root, text="👁 Podgląd danych", command=self.show_data_preview, width=30).pack(pady=5)
        tk.Button(root, text="🔍 Filtruj dane (usuń puste)", command=self.filter_data, width=30).pack(pady=5)
        tk.Button(root, text="📊 Pokaż statystyki", command=self.show_stats, width=30).pack(pady=5)

        # ------------------------------
        # Histogramy
        # ------------------------------
        tk.Label(root, text="📈 Histogramy:", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Button(root, text="Wiek (Age)", command=self.plot_age_hist, width=30).pack(pady=2)
        tk.Button(root, text="Tętno (HeartRate)", command=self.plot_heartrate_hist, width=30).pack(pady=2)
        tk.Button(root, text="Ciśnienie skurczowe (SystolicBP)", command=self.plot_systolic_hist, width=30).pack(pady=2)
        tk.Button(root, text="Ciśnienie rozkurczowe (DiastolicBP)", command=self.plot_diastolic_hist, width=30).pack(pady=2)

        # ------------------------------
        # Inne wykresy
        # ------------------------------
        tk.Label(root, text="📉 Inne wykresy:", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Button(root, text="Wiek vs SystolicBP (rozrzut)", command=self.plot_scatter, width=30).pack(pady=2)

        # ------------------------------
        # Eksport
        # ------------------------------
        tk.Label(root, text="💾 Eksport:", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Button(root, text="Eksportuj dane do CSV", command=self.export_data, width=30).pack(pady=2)
        tk.Button(root, text="Utwórz raport PDF", command=self.export_pdf_report, width=30).pack(pady=2)

    # ---------------------------------------
    # Funkcje wczytywania i eksportu
    # ---------------------------------------
    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        try:
            self.df = dp.load_csv(path)
            messagebox.showinfo("Sukces", f"Wczytano dane z pliku:\n{path}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać pliku:\n{e}")

    def export_data(self):
        if self.df is None:
            messagebox.showwarning("Uwaga", "Brak danych do eksportu.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        dp.export_csv(self.df, path)
        messagebox.showinfo("Eksport", f"Dane zapisano do: {path}")

    def export_pdf_report(self):
        if self.df is None:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")
            return
        folder = filedialog.askdirectory(title="Wybierz folder do zapisania raportu")
        if not folder:
            return
        try:
            report.create_pdf_report(self.df, folder)
            messagebox.showinfo("PDF", f"Raport PDF został utworzony w folderze:\n{folder}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się utworzyć raportu PDF:\n{e}")

    # ---------------------------------------
    # Filtracja i statystyki
    # ---------------------------------------
    def filter_data(self):
        if self.df is None:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")
            return

        self.df = self.df.dropna(subset=["Age", "SystolicBP", "DiastolicBP", "HeartRate"])
        messagebox.showinfo("Filtracja", "Usunięto rekordy z brakującymi danymi.")

    def show_stats(self):
        if self.df is None:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")
            return
        stats = dp.compute_statistics(self.df)
        mean_str = stats["mean"].to_string()
        median_str = stats["median"].to_string()
        messagebox.showinfo("Statystyki", f"Średnie wartości:\n{mean_str}\n\nMediany:\n{median_str}")

    # ---------------------------------------
    # Podgląd danych z sortowaniem
    # ---------------------------------------
    def show_data_preview(self):
        if self.df is None:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")
            return

        win = tk.Toplevel(self.root)
        win.title("Podgląd danych")
        win.geometry("900x400")

        # Wyszukiwanie
        search_frame = tk.Frame(win)
        search_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(search_frame, text="Filtr tekstowy:").pack(side="left")
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Szukaj", command=lambda: self.filter_treeview(tree, search_entry.get())).pack(side="left")

        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        columns = list(self.df.columns)
        tree["columns"] = columns

        for col in columns:
            tree.heading(col, text=col, command=lambda _col=col: self.sort_treeview(tree, _col, False))
            tree.column(col, width=120, anchor="center")

        for _, row in self.df.head(100).iterrows():
            tree.insert("", "end", values=list(row))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree = tree
        self.tree_data = self.df.head(100)

    def sort_treeview(self, tree, col, reverse):
        try:
            data = [(tree.set(k, col), k) for k in tree.get_children("")]
            try:
                data = [(float(v), k) for v, k in data]
            except ValueError:
                pass
            data.sort(reverse=reverse)
            for index, (val, k) in enumerate(data):
                tree.move(k, "", index)
            tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))
        except Exception as e:
            messagebox.showerror("Błąd sortowania", str(e))

    def filter_treeview(self, tree, query):
        for row in tree.get_children():
            tree.delete(row)
        if not query:
            df_filtered = self.tree_data
        else:
            df_filtered = self.df[self.df.apply(lambda x: x.astype(str).str.contains(query, case=False).any(), axis=1)]
        for _, row in df_filtered.head(100).iterrows():
            tree.insert("", "end", values=list(row))

    # ---------------------------------------
    # Wykresy
    # ---------------------------------------
    def plot_age_hist(self):
        if self.df is not None:
            viz.plot_age_hist(self.df)
        else:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")

    def plot_heartrate_hist(self):
        if self.df is not None:
            viz.plot_heartrate_hist(self.df)
        else:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")

    def plot_systolic_hist(self):
        if self.df is not None:
            viz.plot_systolic_hist(self.df)
        else:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")

    def plot_diastolic_hist(self):
        if self.df is not None:
            viz.plot_diastolic_hist(self.df)
        else:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")

    def plot_scatter(self):
        if self.df is not None:
            viz.plot_scatter(self.df)
        else:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj dane!")


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalApp(root)
    root.mainloop()
