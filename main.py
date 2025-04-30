import flet as ft
from dashboard import dashboard_page
from categories import categories_page
from expenses import expenses_page
from edit_expenses import add_expense_page, edit_expense_page, delete_expense_page
from db import create_db, populate_db


def main(page: ft.Page):
    create_db()
    populate_db()

    page.title = "Gestion de budget"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_min_width = 350
    page.window_min_height = 600
    page.window_max_width = None
    page.window_max_height = None
    page.scroll = ft.ScrollMode.ALWAYS
    page.padding = 10

    navigation_bar = ft.Row([
        ft.ElevatedButton("🏠 Accueil", expand=1, on_click=lambda e: page.go("/")),
        ft.ElevatedButton("📂 Catégories", expand=1, on_click=lambda e: page.go("/category")),
        ft.ElevatedButton("💸 Dépenses", expand=1, on_click=lambda e: page.go("/expenses")),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=10)

    page.session.set("navigation_bar", navigation_bar)

    def router(route):
        page.clean()
        page.add(navigation_bar)  # Ajouter la barre de navigation à chaque page

        if route == "/":
            page.add(dashboard_page(page))  # Appel direct à la fonction de la page
        elif route == "/category":
            page.add(categories_page(page))  # Appel direct à la fonction de la page
        elif route == "/expenses":
            page.add(expenses_page(page))  # Appel direct à la fonction de la page
        elif route.startswith("/add-expense"):
            page.add(add_expense_page(page))  # Appel direct à la fonction de la page
        elif route.startswith("/edit-expense"):
            try:
                exp_id = int(route.split("/")[-1])
                page.add(edit_expense_page(page, exp_id))  # Appel direct à la fonction de la page
            except:
                page.go("/expenses")
        elif route.startswith("/delete-expense"):
            try:
                exp_id_del = int(route.split("/")[-1])
                page.add(delete_expense_page(page, exp_id_del))  # Appel direct à la fonction de la page
            except:
                page.go("/expenses")
        else:
            page.add(ft.Text("❌ Page non trouvée", size=32, color=ft.colors.RED))
        page.update()

    page.on_route_change = lambda e: router(e.route)
    router(page.route)

ft.app(target=main)
