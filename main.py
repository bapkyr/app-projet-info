import flet as ft
from db import create_db, populate_db
from dashboard import dashboard_page
from categories import categories_page
from expenses import expenses_page
from edit_expenses import add_expense_page, edit_expense_page, delete_expense_page


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS
    create_db()
    populate_db()
    page.title = "Gestion de budget"
    page.window_width = 900
    page.window_height = 600

    navigation_bar = ft.Row([
            ft.ElevatedButton("🏠 Accueil", on_click=lambda e: page.go('/')),
            ft.ElevatedButton("📂 Catégories", on_click=lambda e: page.go('/categories')),
            ft.ElevatedButton("💸 Dépenses", on_click=lambda e: page.go('/expenses')),
        ], alignment=ft.MainAxisAlignment.CENTER)

    def router(route):
        page.clean()
        page.add(navigation_bar)

        if route == '/':
            page.add(dashboard_page(page))
        elif route == '/categories':
            page.add(categories_page(page))
        elif route == '/expenses':
            page.add(expenses_page(page))
        elif route == '/add-expense':
            page.add(add_expense_page(page))

        elif route.startswith('/edit-expense/'):
            expense_id = int(route.split('/')[-1])
            page.add(edit_expense_page(page, expense_id))

        elif route.startswith('/delete-expense/'):
            expense_id = int(route.split('/')[-1])
            page.add(delete_expense_page(page, expense_id))

        else:
            page.add(ft.Text("Page non trouvée"))
        
        page.update()
    
    page.on_route_change = lambda e: router(e.route)
    router(page.route)

ft.app(target=main)