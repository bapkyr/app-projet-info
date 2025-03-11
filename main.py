import flet as ft
from db import create_db
from dashboard import dashboard_page

def main(page: ft.Page):
    create_db()
    
    page.title = "Gestion de budget"
    page.window_width = 900
    page.window_height = 600

    navigation_bar = ft.Row([
            ft.ElevatedButton("🏠 Accueil", on_click=lambda e: page.go('/')),
            ft.ElevatedButton("📂 Catégories", on_click=lambda e: page.go('/category')),
            ft.ElevatedButton("💸 Dépenses", on_click=lambda e: page.go('/expenses')),
        ], alignment=ft.MainAxisAlignment.CENTER)

    def router(route):
        page.clean()
        page.add(navigation_bar)

        if route == '/':
            page.add(dashboard_page(page))
        elif route == '/category':
            pass
        elif route == '/expenses':
            pass
        else:
            page.add(ft.Text("Page non trouvée"))
        
        page.update()
    
    page.on_route_change = lambda e: router(e.route)
    router(page.route)

ft.app(target=main)