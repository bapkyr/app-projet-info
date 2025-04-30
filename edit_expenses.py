import flet as ft
from sqlmodel import Session, select
from db import engine, Expense, Category
import datetime


def get_categories():
    with Session(engine) as session:
        return session.exec(select(Category)).all()

def add_expense_page(page: ft.Page):
    categories = get_categories()

    date_field = ft.TextField(label="Date (YYYY-MM-DD)")
    amount_field = ft.TextField(label="Montant")
    description_field = ft.TextField(label="Description", multiline=True)
    category_dropdown = ft.Dropdown(
        label="Catégorie existante",
        options=[ft.dropdown.Option("Aucune")] + [ft.dropdown.Option(c.name) for c in categories]
    )
    new_category_field = ft.TextField(label="Nouvelle catégorie (optionnel)")

    def submit(e):
        if not date_field.value or not amount_field.value:
            page.snack_bar = ft.SnackBar(ft.Text("Veuillez remplir tous les champs obligatoires."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            with Session(engine) as session:
                cat_name = new_category_field.value.strip() or category_dropdown.value
                selected_cat = None
                if cat_name and cat_name != "Aucune":
                    selected_cat = session.exec(select(Category).where(Category.name == cat_name)).first()
                    if not selected_cat:
                        selected_cat = Category(name=cat_name)
                        session.add(selected_cat)
                        session.commit()
                        session.refresh(selected_cat)

                expense = Expense(
                    date=datetime.datetime.strptime(date_field.value, "%Y-%m-%d").date(),
                    amount=float(amount_field.value),
                    description=description_field.value,
                    cat_id=selected_cat.id if selected_cat else None
                )
                session.add(expense)
                session.commit()

            page.go("/expenses")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erreur lors de l'ajout de la dépense : {ex}"))
            page.snack_bar.open = True
            page.update()

    return ft.Column([
        ft.Text("➕ Ajouter une Dépense", size=32, weight=ft.FontWeight.BOLD),
        date_field,
        amount_field,
        description_field,
        category_dropdown,
        new_category_field,
        ft.ElevatedButton("Valider", on_click=submit)
    ], spacing=20)

def edit_expense_page(page: ft.Page, expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        categories = get_categories()

    date_field = ft.TextField(label="Date", value=str(expense.date))
    amount_field = ft.TextField(label="Montant", value=str(expense.amount))
    description_field = ft.TextField(label="Description", value=expense.description or "", multiline=True)
    category_dropdown = ft.Dropdown(
        label="Catégorie existante",
        value=session.get(Category, expense.cat_id).name if expense.cat_id else None,
        options=[ft.dropdown.Option(c.name) for c in categories]
    )
    new_category_field = ft.TextField(label="Nouvelle catégorie (optionnel)")

    def submit(e):
        with Session(engine) as session:
            cat_name = new_category_field.value.strip() or category_dropdown.value
            selected_cat = session.exec(select(Category).where(Category.name == cat_name)).first()
            if not selected_cat:
                selected_cat = Category(name=cat_name)
                session.add(selected_cat)
                session.commit()
                session.refresh(selected_cat)

            expense.date = date_field.value
            expense.amount = float(amount_field.value)
            expense.description = description_field.value
            expense.cat_id = selected_cat.id
            session.add(expense)
            session.commit()
        page.go("/expenses")

    return ft.Column([
        ft.Text("✏️ Modifier la Dépense", size=32, weight=ft.FontWeight.BOLD),
        date_field,
        amount_field,
        description_field,
        category_dropdown,
        new_category_field,
        ft.ElevatedButton("Valider", on_click=submit)
    ], spacing=20)

def delete_expense_page(page: ft.Page, expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)

    def confirm_delete(e):
        with Session(engine) as session:
            session.delete(expense)
            session.commit()
        page.go("/expenses")

    return ft.Column([
        ft.Text(f"🗑️ Supprimer la Dépense {expense.description}", size=32, weight=ft.FontWeight.BOLD),
        ft.ElevatedButton("Confirmer la suppression", on_click=confirm_delete),
        ft.ElevatedButton("Annuler", on_click=lambda e: page.go("/expenses"))
    ], spacing=20)
