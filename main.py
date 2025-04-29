import flet as ft
from dashboard import dashboard_page
from categories import categories_page
from expenses import expenses_page
from edit_expenses import add_expense_page, edit_expense_page, delete_expense_page
from layout import show_with_nav
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

    def toggle_dark_mode(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    navigation_bar = ft.Row([
        ft.ElevatedButton("🏠 Accueil", expand=1, on_click=lambda e: page.go("/")),
        ft.ElevatedButton("📂 Catégories", expand=1, on_click=lambda e: page.go("/category")),
        ft.ElevatedButton("💸 Dépenses", expand=1, on_click=lambda e: page.go("/expenses")),
        ft.IconButton(
            icon=ft.icons.DARK_MODE,
            selected_icon=ft.icons.LIGHT_MODE,
            on_click=toggle_dark_mode,
            tooltip="Changer Mode"
        )
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=10)

    page.session.set("navigation_bar", navigation_bar)

    def router(route):
        if route == "/":
            show_with_nav(page, dashboard_page(page))
        elif route == "/category":
            show_with_nav(page, categories_page(page))
        elif route == "/expenses":
            show_with_nav(page, expenses_page(page))
        elif route.startswith("/add-expense"):
            show_with_nav(page, add_expense_page(page))
        elif route.startswith("/edit-expense"):
            try:
                exp_id = int(route.split("/")[-1])
                show_with_nav(page, edit_expense_page(page, exp_id))
            except:
                page.go("/expenses")
        elif route.startswith("/delete-expense"):
            try:
                exp_id_del = int(route.split("/")[-1])
                show_with_nav(page, delete_expense_page(page, exp_id_del))
            except:
                page.go("/expenses")
        else:
            page.clean()
            page.add(navigation_bar)
            page.add(ft.Text("❌ Page non trouvée", size=32, color=ft.colors.RED))
            page.update()

    page.on_route_change = lambda e: router(e.route)
    router(page.route)

ft.app(target=main)
