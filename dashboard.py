import flet as ft
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from db import get_expenses_by_category, get_expenses_grouped_by_date, get_categories
from statistics import mean


def dashboard_page(page: ft.Page):
    params = page.route_query
    selected_month = params.get("month")
    selected_category = params.get("cat")

    data_category = get_expenses_by_category()
    data_date = get_expenses_grouped_by_date()

    if selected_category:
        data_category = [(name, value) for name, value in data_category if name == selected_category]

    if selected_month:
        data_date = [(m, v) for m, v in data_date if m == selected_month]

    categories = [item[0] for item in data_category] if data_category else []
    totals = [float(item[1]) for item in data_category] if data_category else []
    total_expenses = sum(totals) if totals else 0

    months = [item[0] for item in data_date]
    monthly_totals = [item[1] for item in data_date]

    top_month = months[monthly_totals.index(max(monthly_totals))] if monthly_totals else "N/A"
    average_expense = mean(monthly_totals) if monthly_totals else 0

    fig_bar, ax_bar = plt.subplots(figsize=(12, 4))
    ax_bar.bar(months, monthly_totals, color="skyblue")
    ax_bar.set_title("Dépenses mensuelles")
    ax_bar.set_xlabel("Mois")
    ax_bar.set_ylabel("Total dépenses (€)")
    ax_bar.set_xticks(range(len(months)))
    ax_bar.set_xticklabels(months, rotation=45)
    ax_bar.set_ylim(bottom=0)
    for i, v in enumerate(monthly_totals):
        ax_bar.text(i, v + 5, str(int(v)), ha='center', va='bottom', fontsize=8)
    fig_bar.tight_layout()
    plt.close(fig_bar)

    fig_line, ax_line = plt.subplots(figsize=(12, 4))
    ax_line.plot(months, monthly_totals, color="blue", marker="o", linewidth=2)
    ax_line.set_title("Évolution des Dépenses")
    ax_line.set_xlabel("Mois")
    ax_line.set_ylabel("Montant (€)")
    ax_line.set_xticks(range(len(months)))
    ax_line.set_xticklabels(months, rotation=45)
    ax_line.grid(True, linestyle="--", alpha=0.5)
    fig_line.tight_layout()
    plt.close(fig_line)

    def on_month_change(e):
        page.go(f"/?month={e.control.value}&cat={selected_category or ''}")

    def on_category_change(e):
        page.go(f"/?month={selected_month or ''}&cat={e.control.value}")

    month_dropdown = ft.Dropdown(
        label="Filtrer par mois",
        options=[ft.dropdown.Option(m) for m in months],
        value=selected_month,
        width=200,
        on_change=on_month_change
    )

    category_dropdown = ft.Dropdown(
        label="Filtrer par catégorie",
        options=[ft.dropdown.Option(c) for c in categories],
        value=selected_category,
        width=200,
        on_change=on_category_change
    )

    return ft.Column([
        ft.Text("🏠 Tableau de Bord", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),

        ft.Row([
            month_dropdown,
            category_dropdown
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),

        ft.Text(f"💰 Total Dépenses : {total_expenses:.2f} €", size=24, color="red", weight=ft.FontWeight.W_700),

        ft.Row([
            ft.Card(content=ft.Container(ft.Column([
                ft.Text("📈 Max", size=18),
                ft.Text(f"{max(totals):.2f} €" if totals else "0 €", size=20, weight=ft.FontWeight.BOLD)
            ]), padding=10, bgcolor=ft.colors.TEAL_50)),

            ft.Card(content=ft.Container(ft.Column([
                ft.Text("📉 Moyenne", size=18),
                ft.Text(f"{average_expense:.2f} €", size=20, weight=ft.FontWeight.BOLD)
            ]), padding=10, bgcolor=ft.colors.TEAL_50)),

            ft.Card(content=ft.Container(ft.Column([
                ft.Text("🏆 Mois Top", size=18),
                ft.Text(top_month, size=20, weight=ft.FontWeight.BOLD)
            ]), padding=10, bgcolor=ft.colors.TEAL_50)),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),

        ft.Row([
            ft.Card(content=ft.Container(
                content=MatplotlibChart(fig_bar, expand=True),
                padding=10,
                width=420,
                bgcolor=ft.colors.BLUE_50,
                border_radius=10
            )),

            ft.Card(content=ft.Container(
                content=MatplotlibChart(fig_line, expand=True),
                padding=10,
                width=420,
                bgcolor=ft.colors.ORANGE_50,
                border_radius=10
            )),
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row([
            ft.ElevatedButton("➕ Ajouter Dépense", icon=ft.icons.ADD, on_click=lambda e: page.go("/add-expense")),
            ft.ElevatedButton("📂 Voir Catégories", icon=ft.icons.CATEGORY, on_click=lambda e: page.go("/categories")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, expand=True),

    ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS)
