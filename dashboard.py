import flet as ft
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from db import get_expenses_by_category, get_expenses_grouped_by_date, get_categories
from statistics import mean
import datetime
from datetime import timedelta
from layout import navigation_bar, show_with_nav


def dashboard_page(page: ft.Page):
    selected_category = page.session.get("cat")
    selected_year = page.session.get("year")
    selected_week = page.session.get("week")

    start_date = end_date = None
    if selected_week:
        monday = datetime.datetime.strptime(f"{selected_week}-1", "%G-W%V-%u").date()
        start_date = monday
        end_date = monday + timedelta(days=7)
    elif selected_year:
        start_date = datetime.date(int(selected_year), 1, 1)
        end_date = datetime.date(int(selected_year) + 1, 1, 1)

    data_category = get_expenses_by_category(start_date, end_date, selected_category)
    data_date = get_expenses_grouped_by_date(start_date, end_date, selected_category)

    categories = [item[0] for item in data_category] if data_category else []
    totals = [float(item[1]) for item in data_category] if data_category else []
    total_expenses = sum(totals) if totals else 0

    months = [item[0] for item in data_date]
    monthly_totals = [item[1] for item in data_date]

    top_month = months[monthly_totals.index(max(monthly_totals))] if monthly_totals else "N/A"
    average_expense = mean(monthly_totals) if monthly_totals else 0

    fig_bar, ax_bar = plt.subplots(figsize=(12, 4))
    ax_bar.bar(months, monthly_totals, color="skyblue")
    ax_bar.set_title("Dépenses")
    ax_bar.set_xlabel("Période")
    ax_bar.set_ylabel("Total dépenses (€)")
    ax_bar.set_xticks(range(len(months)))
    ax_bar.set_xticklabels(months, rotation=45)
    if monthly_totals:
        ax_bar.set_ylim(0, max(monthly_totals) * 1.2)
    for i, v in enumerate(monthly_totals):
        ax_bar.text(i, v + 1, str(int(v)), ha='center', va='bottom', fontsize=8)
    fig_bar.tight_layout()
    plt.close(fig_bar)

    fig_line, ax_line = plt.subplots(figsize=(12, 4))
    ax_line.plot(months, monthly_totals, color="blue", marker="o", linewidth=2)
    ax_line.set_title("Évolution des Dépenses")
    ax_line.set_xlabel("Période")
    ax_line.set_ylabel("Montant (€)")
    ax_line.set_xticks(range(len(months)))
    ax_line.set_xticklabels(months, rotation=45)
    if monthly_totals:
        ax_line.set_ylim(0, max(monthly_totals) * 1.2)
    ax_line.grid(True, linestyle="--", alpha=0.5)
    fig_line.tight_layout()
    plt.close(fig_line)

    def on_category_change(e):
        page.session.set("cat", e.control.value)
        page.clean()
        page.add(dashboard_page(page))
        page.update()

    def on_year_change(e):
        page.session.set("year", e.control.value)
        page.session.set("week", None)
        page.clean()
        page.add(dashboard_page(page))
        page.update()

    def on_week_change(e):
        page.session.set("week", e.control.value)
        page.session.set("year", None)
        page.clean()
        page.add(dashboard_page(page))
        page.update()

    def on_reset_filters(e):
        page.session.clear()
        page.clean()
        page.add(dashboard_page(page))
        page.update()

    all_categories = get_categories()
    category_dropdown = ft.Dropdown(
        label="Filtrer par catégorie",
        options=[ft.dropdown.Option(c.name) for c in all_categories],
        value=selected_category,
        width=200,
        on_change=on_category_change
    )

    all_months = sorted({item[0] for item in get_expenses_grouped_by_date()})
    all_years = sorted({m.split("-")[0] for m in all_months})
    year_dropdown = ft.Dropdown(
        label="Filtrer par année",
        options=[ft.dropdown.Option(y) for y in all_years],
        value=selected_year,
        width=200,
        on_change=on_year_change
    )

    all_weeks = sorted({datetime.datetime.strptime(m, "%Y-%m").date().isocalendar()[:2] for m in all_months})
    week_options = sorted({f"{y}-W{w:02d}" for y, w in all_weeks})
    week_dropdown = ft.Dropdown(
        label="Filtrer par semaine",
        options=[ft.dropdown.Option(w) for w in week_options],
        value=selected_week,
        width=200,
        on_change=on_week_change
    )

    return ft.Column([
        ft.Text("🏠 Tableau de Bord", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),

        ft.Row([
            year_dropdown,
            week_dropdown,
            category_dropdown,
            ft.TextButton("🔄 Réinitialiser", on_click=on_reset_filters)
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS),

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
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS),

        ft.Text(f"💰 Total Dépenses : {total_expenses:.2f} €", size=24, color="red", weight=ft.FontWeight.W_700),

        ft.Card(content=ft.Container(
            content=MatplotlibChart(fig_bar, expand=True),
            padding=10,
            bgcolor=ft.colors.BLUE_50,
            border_radius=10
        )),

        ft.Card(content=ft.Container(
            content=MatplotlibChart(fig_line, expand=True),
            padding=10,
            bgcolor=ft.colors.ORANGE_50,
            border_radius=10
        )),

        ft.Row([
            ft.ElevatedButton("Ajouter Dépense", icon=ft.icons.ADD, on_click=lambda e: page.go("/add-expense")),
            ft.ElevatedButton("Voir Catégories", icon=ft.icons.CATEGORY, on_click=lambda e: page.go("/category")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, expand=True),

    ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS)
