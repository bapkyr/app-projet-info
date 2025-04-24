import flet as ft
from db import get_categories, add_expense, update_expense, del_expense
from sqlmodel import Session, select
from db import engine, Expense
import datetime


def add_expense_page(page: ft.Page):
    categories = get_categories()
    cat_options = [ft.dropdown.Option(str(c.id), text=c.name) for c in categories]

    date_picker = ft.TextField(label="Date", hint_text="YYYY-MM-DD")
    amount_field = ft.TextField(label="Montant", hint_text="Ex: 100.50")
    desc_field = ft.TextField(label="Description")
    category_dropdown = ft.Dropdown(label="Catégorie", options=cat_options)

    def on_submit(e):
        try:
            dt = datetime.datetime.strptime(date_picker.value, "%Y-%m-%d").date()
            amt = float(amount_field.value)
            cat = int(category_dropdown.value)
            add_expense(dt, amt, cat)
            page.go("/")
        except Exception as err:
            print("Erreur:", err)

    return ft.Column([
        ft.Text("➕ Ajouter une Dépense", size=28, weight=ft.FontWeight.BOLD),
        date_picker,
        amount_field,
        desc_field,
        category_dropdown,
        ft.ElevatedButton("Enregistrer", on_click=on_submit),
        ft.TextButton("Annuler", on_click=lambda e: page.go("/"))
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)


def edit_expense_page(page: ft.Page, expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
    categories = get_categories()
    cat_options = [ft.dropdown.Option(str(c.id), text=c.name) for c in categories]

    date_picker = ft.TextField(label="Date", value=str(expense.date))
    amount_field = ft.TextField(label="Montant", value=str(expense.amount))
    desc_field = ft.TextField(label="Description", value=expense.description or "")
    category_dropdown = ft.Dropdown(label="Catégorie", value=str(expense.cat_id), options=cat_options)

    def on_submit(e):
        try:
            dt = datetime.datetime.strptime(date_picker.value, "%Y-%m-%d").date()
            amt = float(amount_field.value)
            cat = int(category_dropdown.value)
            update_expense(expense_id, new_date=dt, new_amount=amt, new_cat=cat)
            page.go("/expenses")
        except Exception as err:
            print("Erreur:", err)

    return ft.Column([
        ft.Text("✏️ Modifier Dépense", size=28, weight=ft.FontWeight.BOLD),
        date_picker,
        amount_field,
        desc_field,
        category_dropdown,
        ft.ElevatedButton("Enregistrer", on_click=on_submit),
        ft.TextButton("Annuler", on_click=lambda e: page.go("/expenses"))
    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)


def delete_expense_page(page: ft.Page, expense_id: int):
    def on_confirm(e):
        del_expense(expense_id)
        page.go("/expenses")

    return ft.Column([
        ft.Text("❌ Supprimer Dépense", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
        ft.Text("Êtes-vous sûr de vouloir supprimer cette dépense ?"),
        ft.Row([
            ft.ElevatedButton("Oui, Supprimer", color=ft.colors.WHITE, bgcolor=ft.colors.RED, on_click=on_confirm),
            ft.TextButton("Annuler", on_click=lambda e: page.go("/expenses"))
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=30, alignment=ft.MainAxisAlignment.CENTER)
