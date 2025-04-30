import flet as ft
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from db import get_expenses_by_category, get_categories
from sqlmodel import Session, select
from db import engine, Category


def categories_page(page: ft.Page):
    selected_year = page.session.get("year")
    selected_week = page.session.get("week")

    import datetime
    from datetime import timedelta

    start_date = end_date = None
    if selected_week:
        monday = datetime.datetime.strptime(f"{selected_week}-1", "%G-W%V-%u").date()
        start_date = monday
        end_date = monday + timedelta(days=7)
    elif selected_year:
        start_date = datetime.date(int(selected_year), 1, 1)
        end_date = datetime.date(int(selected_year) + 1, 1, 1)

    data = get_expenses_by_category(start_date, end_date, None)
    categories = [item[0] for item in data]
    totals = [float(item[1]) for item in data]

    fig, ax = plt.subplots(figsize=(6, 6))
    if totals:
        ax.pie(totals, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        fig.suptitle("Répartition des Dépenses par Catégorie", fontsize=16)
    else:
        fig.text(0.5, 0.5, "Aucune dépense disponible", ha='center', va='center', fontsize=14)
    plt.tight_layout()
    plt.close(fig)

    with Session(engine) as session:
        all_categories = session.exec(select(Category)).all()

    category_rows = []
    for category in all_categories:
        category_rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(category.name)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Supprimer",
                            on_click=lambda e, id=category.id: delete_category_action(id, page)
                        )
                    ]))
                ]
            )
        )


    def delete_category_action(category_id, page):
        with Session(engine) as session:
            category = session.get(Category, category_id)
            if category:
                print(f"Suppression de la catégorie : {category.name}")
                session.delete(category)
                session.commit()
                page.snack_bar = ft.SnackBar(ft.Text(f"Catégorie '{category.name}' supprimée avec succès."))
                page.snack_bar.open = True
                page.go("/category")

    return ft.Column([
        ft.Text("📂 Catégories de Dépenses", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),

        MatplotlibChart(fig, expand=True),

        ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Nom de la Catégorie")),
                ft.DataColumn(label=ft.Text("Actions"))
            ],
            rows=category_rows
        ),

        ft.Row([
            ft.ElevatedButton("Ajouter Catégorie", icon=ft.icons.ADD, on_click=lambda e: page.go("/add-category")),
            ft.ElevatedButton("Retour", icon=ft.icons.HOME, on_click=lambda e: page.go("/"))
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS)
