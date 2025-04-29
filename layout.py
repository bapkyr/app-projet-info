import flet as ft

def navigation_bar(page: ft.Page):
    return ft.Container(
        ft.Row([
            ft.ElevatedButton("🏠 Accueil", on_click=lambda e: page.go("/")),
            ft.ElevatedButton("📂 Catégories", on_click=lambda e: page.go("/category")),
            ft.ElevatedButton("💸 Dépenses", on_click=lambda e: page.go("/expenses")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.BLUE_100,
        border_radius=10,
        margin=10
    )

def show_with_nav(page: ft.Page, content):
    page.clean()
    page.add(
        ft.Column([
            navigation_bar(page),
            ft.Container(
                content,
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                expand=True
            )
        ], expand=True, scroll=ft.ScrollMode.AUTO)
    )
    page.update()

def styled_title(text):
    return ft.Text(text, size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)

def styled_button(text, icon=None, on_click=None):
    return ft.ElevatedButton(text, icon=icon, on_click=on_click, style=ft.ButtonStyle(padding=ft.padding.all(15)))

def styled_container(content):
    return ft.Container(
        content,
        padding=20,
        bgcolor=ft.colors.BLUE_50,
        border_radius=10,
        margin=10
    )
