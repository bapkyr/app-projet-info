import flet as ft
import plotly.express as px
from db import get_expenses_by_category, get_expenses_grouped_by_date

def dashboard_page(page: ft.Page):
    data_category = get_expenses_by_category()
    categories = [item[0] for item in data_category] if data_category else []
    

    totals = [float(item[1]) for item in data_category] if data_category else []
    total_expenses = sum(totals) if totals else 0
    
    data_date = get_expenses_grouped_by_date()
    months = [item[0] for item in data_date] if data_date else []
    monthly_totals = [item[1] for item in data_date] if data_date else []
    
    #Pie chart
    pie_chart = ft.PieChart(
        sections=[
            ft.PieChartSection(value=totals[i], title=categories[i])
            for i in range(len(categories))
        ] if categories else [
            ft.PieChartSection(value=1, title="Aucune donnée")
        ],
        width=400,
        height=400,
        sections_space=2,
        center_space_radius=40,
    )


    #Bar chart
    bar_chart = ft.BarChart(
        data=[
            ft.BarChartData(x=months[i], y=monthly_totals[i])
            for i in range(len(months))
        ] if months else [
            ft.BarChartData(x="Aucune donnée", y=0)
        ],
        width=600,
        height=400,
        bar_width=30,
    )

    return ft.Column([
        ft.Text("🏠 Tableau de Bord", size=32, weight=ft.FontWeight.BOLD),
        ft.Text(f"💰 Dépenses Totales : {total_expenses} chf", size=24, color="red"),
        pie_chart,
        bar_chart,
        ft.Row([
            ft.ElevatedButton("➕ Ajouter Dépense", on_click=lambda e: page.go("/add-expense")),
            ft.ElevatedButton("📂 Voir Catégories", on_click=lambda e: page.go("/categories")),
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
