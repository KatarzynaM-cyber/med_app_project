import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
import viz


def create_pdf_report(df, folder):
    """
    Tworzy elegancki raport PDF z danymi medycznymi, tabelą statystyk i wykresami.
    """
    pdf_path = os.path.join(folder, "raport_medyczny.pdf")

    # Tworzenie folderu na wykresy
    plots_dir = os.path.join(folder, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    # Zapis wykresów do plików PNG
    age_plot = viz.save_hist(df, "Age", "hist_age.png", plots_dir)
    hr_plot = viz.save_hist(df, "HeartRate", "hist_hr.png", plots_dir)
    sbp_plot = viz.save_hist(df, "SystolicBP", "hist_sbp.png", plots_dir)
    dbp_plot = viz.save_hist(df, "DiastolicBP", "hist_dbp.png", plots_dir)
    scatter_plot = viz.save_scatter(df, "scatter_age_sbp.png", plots_dir)

    # Tworzenie dokumentu PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Nagłówek raportu
    story.append(Paragraph("<b>Raport medyczny - analiza danych pacjentów</b>", styles["Title"]))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Raport automatycznie wygenerowany z aplikacji Python.", styles["Normal"]))
    story.append(Spacer(1, 20))

    # Statystyki tabelaryczne
    story.append(Paragraph("<b>Podstawowe statystyki danych:</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    stats = df.describe().round(2).reset_index()

    # Przygotowanie danych do tabeli
    data = [list(stats.columns)] + stats.values.tolist()

    # Styl tabeli
    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3E7CB1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F5F7FA")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.gray)
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # Wykresy
    story.append(Paragraph("<b>Wizualizacje danych:</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    images = [
        ("Histogram wieku", age_plot),
        ("Histogram tętna", hr_plot),
        ("Histogram ciśnienia skurczowego", sbp_plot),
        ("Histogram ciśnienia rozkurczowego", dbp_plot),
        ("Wiek vs SystolicBP (rozrzut)", scatter_plot),
    ]

    for title, img_path in images:
        if os.path.exists(img_path):
            story.append(Paragraph(title, styles["Heading3"]))
            story.append(Image(img_path, width=400, height=250))
            story.append(Spacer(1, 15))

    # Zakończenie raportu
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Wygenerowano automatycznie przy użyciu aplikacji med_app_project.</b>", styles["Normal"]))

    # Zapis do PDF
    doc.build(story)

    return pdf_path
