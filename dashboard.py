import flet as ft
from db import get_expenses_grouped_by_date

def dashboard_page(page: ft.Page):
    # Récupérer les données des dépenses
    data_date = get_expenses_grouped_by_date()
    months = [item[0] for item in data_date] if data_date else []
    monthly_totals = [item[1] for item in data_date] if data_date else []

    total_expenses = sum(monthly_totals) if monthly_totals else 0

    # Préparer les données pour le graphique
    data_points = [
        ft.LineChartDataPoint(x=i, y=monthly_totals[i])
        for i in range(len(months))
    ] if monthly_totals else []

    # Créer le line chart
    line_chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=data_points,
                stroke_width=4,
                color=ft.Colors.BLUE,
                curved=True,
                stroke_cap_round=True,
            )
        ],
        border=ft.Border(
            bottom=ft.BorderSide(2, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE))
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(f"{int(max(monthly_totals) * i / 5)} CHF", size=12)
                )
                for i in range(6)
            ] if monthly_totals else [],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(months[i], size=12)
                )
                for i in range(len(months))
            ] if months else [],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
        min_y=0,
        max_y=max(monthly_totals) if monthly_totals else 100,
        min_x=0,
        max_x=len(months) - 1 if months else 1,
        expand=True,
    )

    # Retourner la mise en page
    return ft.Column([
        ft.Text("🏠 Tableau de Bord", size=32, weight=ft.FontWeight.BOLD),
        ft.Text(f"💰 Dépenses Totales : {total_expenses} chf", size=24, color="red"),
        line_chart,
        ft.Row([
            ft.ElevatedButton("➕ Ajouter Dépense", on_click=lambda e: page.go("/add-expense")),
            ft.ElevatedButton("📂 Voir Catégories", on_click=lambda e: page.go("/categories")),
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
