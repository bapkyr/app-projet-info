import flet as ft
from db import get_expenses_grouped_by_date
import matplotlib.pyplot as plt
import matplotlib
from flet.matplotlib_chart import MatplotlibChart

matplotlib.use('svg')

def dashboard_page(page: ft.Page):
    # Récupérer les données des dépenses
    data_date = get_expenses_grouped_by_date()
    print("Données récupérées :", data_date)  # Debug : Afficher les données récupérées
    months = [item[0] for item in data_date] if data_date else []
    monthly_totals = [item[1] for item in data_date] if data_date else []

    total_expenses = sum(monthly_totals) if monthly_totals else 0

    # Créer un graphique à barres
    fig, ax = plt.subplots(figsize=(8, 4))  # Taille initiale du graphique
    for i, month in enumerate(months):
        ax.bar(month, monthly_totals[i], label=month)
    ax.set_xlabel('Mois')
    ax.set_ylabel('Total Dépenses (chf)')
    ax.set_title('Dépenses Mensuelles')
    ax.legend()

    # Retourner la mise en page
    return ft.Column(
        [
            ft.Text("🏠 Tableau de Bord", size=32, weight=ft.FontWeight.BOLD),
            ft.Text(f"💰 Dépenses Totales : {total_expenses} chf", size=24, color="red"),
            MatplotlibChart(fig, expand=True),  # Le graphique s'adapte à l'espace disponible
            ft.ElevatedButton("Ajouter une Dépense", on_click=lambda e: page.go("/add_expense")),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

