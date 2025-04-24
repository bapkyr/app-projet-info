import flet as ft
from db import get_categories, get_expenses_grouped_by_date
from sqlmodel import Session, select
from db import engine, Expense, Category
import datetime
from datetime import timedelta


def expenses_page(page: ft.Page):
    selected_year = page.session.get("year")
    selected_week = page.session.get("week")
    selected_category = page.session.get("cat")

    start_date = end_date = None
    if selected_week:
        monday = datetime.datetime.strptime(f"{selected_week}-1", "%G-W%V-%u").date()
        start_date = monday
        end_date = monday + timedelta(days=7)
    elif selected_year:
        start_date = datetime.date(int(selected_year), 1, 1)
        end_date = datetime.date(int(selected_year) + 1, 1, 1)

    def on_year_change(e):
        page.session.set("year", e.control.value)
        page.session.set("week", None)
        page.clean()
        page.add(expenses_page(page))
        page.update()

    def on_week_change(e):
        page.session.set("week", e.control.value)
        page.session.set("year", None)
        page.clean()
        page.add(expenses_page(page))
        page.update()

    def on_category_change(e):
        page.session.set("cat", e.control.value)
        page.clean()
        page.add(expenses_page(page))
        page.update()

    def on_reset_filters(e):
        page.session.clear()
        page.clean()
        page.add(expenses_page(page))
        page.update()

    with Session(engine) as session:
        query = select(Expense, Category).join(Category)
        if start_date and end_date:
            query = query.where(Expense.date.between(start_date, end_date))
        if selected_category:
            query = query.where(Category.name == selected_category)
        results = session.exec(query).all()

    rows = []
    for exp, cat in results:
        rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(exp.date.strftime("%Y-%m-%d"))),
                ft.DataCell(ft.Text(cat.name)),
                ft.DataCell(ft.Text(f"{exp.amount:.2f} €")),
                ft.DataCell(ft.Text(exp.description or "-")),
                ft.DataCell(ft.Row([
                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Modifier", on_click=lambda e, id=exp.id: page.go(f"/edit-expense/{id}")),
                    ft.IconButton(icon=ft.icons.DELETE, tooltip="Supprimer", on_click=lambda e, id=exp.id: page.go(f"/delete-expense/{id}"))
                ]))
            ])
        )

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
        ft.Text("💸 Liste des Dépenses Individuelles", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),

        ft.Row([
            year_dropdown,
            week_dropdown,
            category_dropdown,
            ft.TextButton("🔄 Réinitialiser", on_click=on_reset_filters)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),

        ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Date")),
                ft.DataColumn(label=ft.Text("Catégorie")),
                ft.DataColumn(label=ft.Text("Montant")),
                ft.DataColumn(label=ft.Text("Description")),
                ft.DataColumn(label=ft.Text("Actions"))
            ],
            rows=rows
        ),

        ft.Row([
            ft.ElevatedButton("➕ Ajouter Dépense", icon=ft.icons.ADD, on_click=lambda e: page.go("/add-expense")),
            ft.ElevatedButton("🔙 Retour", icon=ft.icons.HOME, on_click=lambda e: page.go("/"))
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS)
