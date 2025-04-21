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


    #Bar chart
    bar_chart = ft.BarChart(bar_groups=[
        ft.BarChartGroup(
            x=months[i],
            bar_rods=[
                ft.BarChartRod(
                    from_y=0,
                    to_y=monthly_totals[i],
                    width=40
                ) for i in range(len(months))
            ]
        ) for i in range(len(months))
    ])

    return ft.Column([
        ft.Text("🏠 Tableau de Bord", size=32, weight=ft.FontWeight.BOLD),
        ft.Text(f"💰 Dépenses Totales : {total_expenses} chf", size=24, color="red"),
        bar_chart,
        ft.Row([
            ft.ElevatedButton("➕ Ajouter Dépense", on_click=lambda e: page.go("/add-expense")),
            ft.ElevatedButton("📂 Voir Catégories", on_click=lambda e: page.go("/categories")),
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
