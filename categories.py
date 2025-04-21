import flet as ft
from db import get_categories, add_category, del_category, get_expenses_by_category
import plotly.express as px

def categories_page(page: ft.Page):
    data = get_expenses_by_category()
    categories = [item[0] for item in data] if data else []
    totals = [float(item[1]) for item in data] if data else []

    # Pie chart
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

    return ft.Column([
        ft.Text("📂 Catégories", size=32, weight=ft.FontWeight.BOLD),
        pie_chart,
        ft.Row([
            ft.ElevatedButton("➕ Ajouter Catégorie", on_click=lambda e: page.go("/add-category")),
            ft.ElevatedButton("🗑️ Supprimer Catégorie", on_click=lambda e: page.go("/delete-category")),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.Text("Catégories existantes :"),
            ft.Dropdown(
                id="categories-dropdown",
                options=[ft.dropdown.Option(cat) for cat in categories],
                width=200
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)