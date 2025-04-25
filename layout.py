import flet as ft

navigation_bar = ft.Row([
    ft.ElevatedButton("🏠 Accueil", on_click=lambda e: e.page.go("/")),
    ft.ElevatedButton("📂 Catégories", on_click=lambda e: e.page.go("/category")),
    ft.ElevatedButton("💸 Dépenses", on_click=lambda e: e.page.go("/expenses")),
], alignment=ft.MainAxisAlignment.CENTER)

def show_with_nav(page, content):
    page.clean()
    page.add(navigation_bar)
    page.add(content)
    page.update()
