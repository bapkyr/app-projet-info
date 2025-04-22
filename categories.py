import flet as ft

def categories_page(page: ft.Page):
    return ft.Column(
        [
            ft.Text("📂 Catégories", size=32, weight=ft.FontWeight.BOLD),
            ft.Text("Liste des catégories ici..."),
            ft.ElevatedButton("Retour à l'accueil", on_click=lambda e: page.go("/")),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )