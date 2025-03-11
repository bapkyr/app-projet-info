import flet as ft
import plotly.express as px
from db import get_expenses_by_category, get_expenses_grouped_by_date

def dashboard_page(page: ft.Page):
    data_category = get_expenses_by_category()
    categories = [item[0] for item in data_category] if data_category else []
    totals = [item[1] for item in data_category] if data_category else []
    total_expenses = sum(totals) if totals else 0
    data_date = get_expenses_grouped_by_date()
    months = [item[0] for item in data_date] if data_date else []
    monthly_totals = [item[1] for item in data_date] if data_date else []
    fig_category = px.pie(names=categories, values=totals, title="Dépenses par Catégorie") if categories else None
    fig_date = px.bar(x=months, y=monthly_totals, title="Évolution des Dépenses Mensuelles") if months else None

    return ft.Column([
        ft.Text("🏠 Tableau de Bord", size=32, weight=ft.FontWeight.BOLD),
        ft.Text(f"💰 Dépenses Totales : {total_expenses} €", size=24, color="red"),
        ft.PlotlyChart(fig_category, expand=True) if fig_category else ft.Text("Aucune dépense enregistrée"),
        ft.PlotlyChart(fig_date, expand=True) if fig_date else ft.Text("Pas de données sur l'évolution des dépenses"),
        ft.Row([
            ft.ElevatedButton("➕ Ajouter Dépense", on_click=lambda e: page.go("/add-expense")),
            ft.ElevatedButton("📂 Voir Catégories", on_click=lambda e: page.go("/categories")),
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
